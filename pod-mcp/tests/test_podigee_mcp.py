import json
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from podigee.api import PodigeeAPIClient
import main

# Test podcast data
test_podcast_data = {
    "id": 1234,
    "title": "Test Podcast",
    "subtitle": "A test podcast",
    "description": "This is a test podcast description.",
    "language": "en",
    "episodes_count": 10,
    "publication_type": "episodic",
    "explicit": False,
    "created_at": "2023-01-01T00:00:00Z",
    "published_at": "2023-01-02T00:00:00Z",
    "keywords": ["test", "podcast", "API"],
    "feeds": [
        {"format": "mp3", "url": "https://example.com/feed.mp3"},
        {"format": "aac", "url": "https://example.com/feed.aac"}
    ],
    "twitter": "testpodcast",
    "website_url": "https://example.com/podcast"
}

# ... existing test code ...

@pytest.mark.asyncio
async def test_get_podcast_details_api_client():
    """Test the get_podcast_details method in the PodigeeAPIClient class."""
    client = PodigeeAPIClient("test_api_key")
    
    # Mock the get method
    with patch.object(client, "get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = test_podcast_data
        
        # Call the method
        result = await client.get_podcast_details(1234)
        
        # Verify the API call was made correctly
        mock_get.assert_called_once_with("podcasts/1234", {})
        
        # Verify the result is the expected data
        assert result == test_podcast_data
        assert result["title"] == "Test Podcast"
        assert len(result["feeds"]) == 2
        
        # Test with fields filter
        await client.get_podcast_details(1234, fields_filter=["title", "description"])
        mock_get.assert_called_with("podcasts/1234", {"fields_filter[]": ["title", "description"]})

@pytest.mark.asyncio
async def test_get_podcast_details_tool_success():
    """Test the get_podcast_details MCP tool with successful API response."""
    # Mock the client method
    with patch.object(main.podigee_client, "get_podcast_details", new_callable=AsyncMock) as mock_method:
        mock_method.return_value = test_podcast_data
        
        # Call the tool
        result = await main.get_podcast_details(1234)
        
        # Verify the API client was called correctly
        mock_method.assert_called_once_with(podcast_id=1234, fields_filter=None)
        
        # Verify the formatted output contains expected data
        assert "# Podcast Details: Test Podcast" in result
        assert "ID: 1234" in result
        assert "Language: en" in result
        assert "Episodes Count: 10" in result
        assert "Publication Type: episodic" in result
        assert "Explicit Content: No" in result
        assert "This is a test podcast description." in result
        assert "## Keywords" in result
        assert "test, podcast, API" in result
        assert "MP3: https://example.com/feed.mp3" in result
        assert "AAC: https://example.com/feed.aac" in result
        assert "Twitter: testpodcast" in result
        assert "Website: https://example.com/podcast" in result

@pytest.mark.asyncio
async def test_get_podcast_details_tool_fallback_to_first_podcast():
    """Test the get_podcast_details MCP tool with no podcast ID provided."""
    # Mock the list_podcasts and get_podcast_details methods
    with patch.object(main.podigee_client, "list_podcasts", new_callable=AsyncMock) as mock_list, \
         patch.object(main.podigee_client, "get_podcast_details", new_callable=AsyncMock) as mock_details:
        
        mock_list.return_value = [{"id": 5678, "title": "First Podcast"}]
        mock_details.return_value = test_podcast_data
        
        # Call the tool without providing a podcast ID
        result = await main.get_podcast_details(None)
        
        # Verify list_podcasts was called to get the first podcast
        mock_list.assert_called_once()
        
        # Verify get_podcast_details was called with the first podcast's ID
        mock_details.assert_called_once_with(podcast_id=5678, fields_filter=None)
        
        # Verify the formatted output contains expected data
        assert "# Podcast Details: Test Podcast" in result

@pytest.mark.asyncio
async def test_get_podcast_details_tool_api_error():
    """Test the get_podcast_details MCP tool with API error."""
    # Mock the client method to raise an error
    with patch.object(main.podigee_client, "get_podcast_details", new_callable=AsyncMock) as mock_method:
        mock_method.side_effect = ValueError("API connection error")
        
        # Call the tool
        result = await main.get_podcast_details(1234)
        
        # Verify error is handled gracefully
        assert "Error fetching podcast details: API connection error" in result 