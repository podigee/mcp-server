import os
import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock

import httpx
from mcp.server.fastmcp import FastMCP

# Import our server module
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main
from podigee.api import PodigeeAPIClient


@pytest.fixture
def mock_podigee_response():
    """Provides mock Podigee API responses for testing"""
    
    # Mock podcasts response
    podcasts_response = [
        {
            "id": 42,
            "title": "Test Podcast",
            "language": "en",
            "created_at": "2023-01-01T00:00:00Z",
        }
    ]
    
    # Mock analytics response
    analytics_response = {
        "meta": {
            "timerange": {
                "start_datetime": "2023-01-01T00:00:00Z",
                "end_datetime": "2023-01-31T00:00:00Z"
            },
            "aggregation_granularity": "day"
        },
        "objects": [
            {
                "downloaded_on": "2023-01-15T00:00:00Z",
                "downloads": {
                    "complete": 100
                },
                "formats": {
                    "mp3": 80,
                    "aac": 20
                },
                "platforms": {
                    "Web": 50,
                    "iOS": 30,
                    "Android": 20
                },
                "countries": {
                    "US": 40,
                    "DE": 30,
                    "GB": 10,
                    "CA": 5,
                    "FR": 5,
                    "Other": 10
                },
                "clients": {
                    "Podcast Addict": 25,
                    "Apple Podcasts": 20,
                    "Spotify": 15,
                    "Overcast": 10,
                    "Unknown": 30
                },
                "clients_on_platforms": {
                    "Apple Podcasts / iOS": 20,
                    "Spotify / Android": 10,
                    "Podcast Addict / Android": 15,
                    "Overcast / iOS": 10,
                    "Web / Chrome": 25,
                    "Web / Firefox": 15,
                    "Web / Safari": 5,
                    "Unknown / Unknown": 5
                },
                "sources": {}
            },
            {
                "downloaded_on": "2023-01-16T00:00:00Z",
                "downloads": {
                    "complete": 50
                },
                "formats": {
                    "mp3": 40,
                    "aac": 10
                },
                "platforms": {
                    "Web": 20,
                    "iOS": 20,
                    "Android": 10
                },
                "countries": {
                    "US": 20,
                    "DE": 15,
                    "GB": 5,
                    "Other": 10
                },
                "clients": {
                    "Podcast Addict": 10,
                    "Apple Podcasts": 15,
                    "Spotify": 5,
                    "Unknown": 20
                },
                "clients_on_platforms": {
                    "Apple Podcasts / iOS": 15,
                    "Spotify / Android": 5,
                    "Podcast Addict / Android": 10,
                    "Web / Chrome": 10,
                    "Web / Firefox": 10
                },
                "sources": {}
            }
        ]
    }
    
    # Mock overview response
    overview_response = {
        "meta": {
            "from": "2023-01-01T00:00:00Z",
            "to": "2023-01-31T00:00:00Z"
        },
        "published_episodes_count": 10,
        "audio_published_minutes": 300,
        "unique_listeners_number": 500,
        "unique_subscribers_number": 200,
        "mean_audio_published_minutes": 30,
        "mean_episode_download": 75,
        "total_downloads": 750,
        "top_episodes": [
            {
                "id": 1,
                "downloads": 150,
                "title": "Top Episode 1",
                "slug": "top-episode-1",
                "number": 1,
                "published_at": "2023-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "downloads": 120,
                "title": "Top Episode 2",
                "slug": "top-episode-2",
                "number": 2,
                "published_at": "2023-01-10T00:00:00Z"
            }
        ]
    }

    # Mock episode analytics response
    episode_analytics_response = {
        "meta": {
            "timerange": {
                "start_datetime": "2023-02-01T00:00:00Z",
                "end_datetime": "2023-02-28T00:00:00Z"
            },
            "aggregation_granularity": "day"
        },
        "objects": [
            {
                "downloaded_on": "2023-02-10T00:00:00Z",
                "downloads": { "complete": 50 },
                "platforms": { "iOS": 30, "Web": 20 },
                # ... other episode analytics fields ...
            },
            {
                "downloaded_on": "2023-02-11T00:00:00Z",
                "downloads": { "complete": 30 },
                "platforms": { "Android": 15, "Web": 15 },
                # ... other episode analytics fields ...
            }
        ]
    }
    
    # Mock episodes list response
    episodes_list_response = [
        {
            "id": 101,
            "podcast_id": 42,
            "title": "First Episode",
            "published_at": "2023-02-15T10:00:00Z",
            "slug": "first-episode"
        },
        {
            "id": 102,
            "podcast_id": 42,
            "title": "Second Episode Special",
            "published_at": None, # Unpublished
            "slug": "second-episode-special"
        },
        {
            "id": 103,
            "podcast_id": 42,
            "title": "Third Episode",
            "published_at": "2023-03-01T10:00:00Z",
            "slug": "third-episode"
        }
    ]
    
    # Mock podcast episodes batch analytics response
    podcast_episodes_batch_response = {
        "objects": [
            {
                "id": 101,
                "title": "First Episode",
                "downloads": 250,
                "published_at": "2023-02-15T10:00:00Z",
                "slug": "first-episode",
                "number": 1,
                "analytics_episodes_cover_image": "https://example.com/cover1.jpg"
            },
            {
                "id": 103,
                "title": "Third Episode",
                "downloads": 175,
                "published_at": "2023-03-01T10:00:00Z",
                "slug": "third-episode",
                "number": 3,
                "analytics_episodes_cover_image": "https://example.com/cover3.jpg"
            },
            {
                "id": 104,
                "title": "Fourth Episode",
                "downloads": 120,
                "published_at": "2023-03-15T10:00:00Z", 
                "slug": "fourth-episode",
                "number": 4,
                "analytics_episodes_cover_image": "https://example.com/cover4.jpg"
            }
        ]
    }

    return {
        "podcasts": podcasts_response,
        "analytics": analytics_response,
        "overview": overview_response,
        "episode_analytics": episode_analytics_response,
        "episodes_list": episodes_list_response,
        "podcast_episodes_batch": podcast_episodes_batch_response
    }


@pytest.mark.asyncio
@patch("main.podigee_client.list_podcasts")
async def test_list_podcasts(mock_list_podcasts, mock_podigee_response):
    """Test the list_podcasts tool"""
    # Configure the mock to return a predefined response
    mock_list_podcasts.return_value = mock_podigee_response["podcasts"]
    
    # Call the function
    result = await main.list_podcasts()
    
    # Verify that the request was made correctly
    mock_list_podcasts.assert_called_once()
    
    # Check that the result contains expected information
    assert "Test Podcast" in result
    assert "ID: 42" in result
    assert "Language: en" in result


@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_analytics_summary")
async def test_get_podcast_analytics_summary(mock_analytics_summary, mock_podigee_response):
    """Test the get_podcast_analytics_summary tool"""
    # Configure the mock to return analytics and overview data
    mock_analytics_summary.return_value = (
        mock_podigee_response["analytics"],
        mock_podigee_response["overview"]
    )
    
    # Call the function with a specific podcast ID
    result = await main.get_podcast_analytics_summary(podcast_id=42)
    
    # Check that the API was called with the correct parameters
    # Should call with podcast_id and calculated from_date and to_date
    # We don't check exact date values as they depend on current date
    mock_analytics_summary.assert_called_once()
    args, _ = mock_analytics_summary.call_args
    assert args[0] == 42
    assert isinstance(args[1], str)
    assert isinstance(args[2], str)
    
    # Check that the result contains expected information
    assert "Podcast Analytics Summary" in result
    assert "**Time Period:** 2023-01-01 to 2023-01-31" in result
    assert "Total Downloads: 150" in result
    assert "Unique Listeners: 500" in result
    assert "Top Episode 1: 150 downloads" in result
    assert "## Top Formats" in result
    assert "1. mp3: 120 downloads" in result
    assert "2. aac: 30 downloads" in result
    assert "## Top Platforms" in result
    assert "1. Web: 70 downloads" in result
    assert "## Top Countries" in result
    assert "1. US: 60 downloads" in result
    assert "5. CA: 5 downloads" in result
    assert "## Top Clients" in result
    assert "1. Unknown: 50 downloads" in result
    assert "## Top Clients on Platforms" in result
    assert "1. Apple Podcasts / iOS: 35 downloads" in result


@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_analytics_summary")
async def test_get_podcast_analytics_summary_no_id(mock_analytics_summary, mock_podigee_response):
    """Test the get_podcast_analytics_summary tool when no podcast ID is provided"""
    # Configure the mock to return analytics and overview data
    mock_analytics_summary.return_value = (
        mock_podigee_response["analytics"],
        mock_podigee_response["overview"]
    )
    
    # Call the function without a podcast ID
    result = await main.get_podcast_analytics_summary()
    
    # Check that it was called without a podcast ID
    mock_analytics_summary.assert_called_once()
    args, _ = mock_analytics_summary.call_args
    assert args[0] is None
    assert isinstance(args[1], str)
    assert isinstance(args[2], str)
    
    # Check that the result contains expected information
    assert "Podcast Analytics Summary" in result


@pytest.mark.asyncio
async def test_podigee_api_client_error():
    """Test error handling in the PodigeeAPIClient get method"""
    # Mock an HTTP error response
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=MagicMock()
    )
    
    # Create a mock client that returns the error response
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response
    
    # Create a client instance
    client = PodigeeAPIClient("test_key")
    
    # Patch httpx.AsyncClient with our mock
    with patch("httpx.AsyncClient", return_value=mock_client):
        # Call the function and expect a ValueError
        with pytest.raises(ValueError) as excinfo:
            await client.get("test-endpoint")
        
        # Check that the error message contains the expected text
        assert "Failed to fetch data from Podigee API" in str(excinfo.value)


@pytest.mark.asyncio
@patch("podigee.api.PodigeeAPIClient.get", new_callable=AsyncMock)
async def test_get_episode_analytics_success_dates(mock_get, mock_podigee_response):
    """Test successful call to get_episode_analytics with date range."""
    client = PodigeeAPIClient(api_key="dummy_key")
    mock_get.return_value = mock_podigee_response["episode_analytics"]
    
    episode_id = 123
    from_date = "2023-02-01"
    to_date = "2023-02-28"
    granularity = "day"
    
    result = await client.get_episode_analytics(
        episode_id=episode_id, 
        from_date=from_date, 
        to_date=to_date,
        granularity=granularity
    )
    
    expected_endpoint = f"episodes/{episode_id}/analytics"
    expected_params = {
        "from": from_date,
        "to": to_date,
        "granularity": granularity
    }
    
    mock_get.assert_called_once_with(expected_endpoint, expected_params)
    assert result == mock_podigee_response["episode_analytics"]


@pytest.mark.asyncio
@patch("podigee.api.PodigeeAPIClient.get", new_callable=AsyncMock)
async def test_get_episode_analytics_success_days(mock_get, mock_podigee_response):
    """Test successful call to get_episode_analytics with days_since_published."""
    client = PodigeeAPIClient(api_key="dummy_key")
    mock_get.return_value = mock_podigee_response["episode_analytics"] # Use same mock data for simplicity
    
    episode_id = 456
    days_since_published = 14
    
    result = await client.get_episode_analytics(
        episode_id=episode_id, 
        days_since_published=days_since_published
    )
    
    expected_endpoint = f"episodes/{episode_id}/analytics"
    expected_params = {
        "days_since_published": days_since_published
    }
    
    mock_get.assert_called_once_with(expected_endpoint, expected_params)
    assert result == mock_podigee_response["episode_analytics"]


@pytest.mark.asyncio
async def test_get_episode_analytics_invalid_params():
    """Test get_episode_analytics raises ValueError for invalid parameters."""
    client = PodigeeAPIClient(api_key="dummy_key")
    
    with pytest.raises(ValueError, match="Cannot use 'from_date'/'to_date' and 'days_since_published' together."):
        await client.get_episode_analytics(
            episode_id=789, 
            from_date="2023-03-01",
            to_date="2023-03-10",
            days_since_published=7 
        ) 

@pytest.mark.asyncio
@patch("podigee.api.PodigeeAPIClient.get", new_callable=AsyncMock)
async def test_list_episodes_api_client(mock_get, mock_podigee_response):
    """Test PodigeeAPIClient.list_episodes calls the get method correctly."""
    client = PodigeeAPIClient(api_key="dummy_key")
    mock_get.return_value = mock_podigee_response["episodes_list"]
    
    podcast_id = 42
    limit = 20
    search = "Special"
    published = False
    
    result = await client.list_episodes(
        podcast_id=podcast_id, 
        limit=limit,
        search=search,
        published=published
    )
    
    expected_endpoint = "episodes"
    expected_params = {
        "podcast_id": podcast_id,
        "limit": limit,
        "search": search,
        "published": published
    }
    
    mock_get.assert_called_once_with(expected_endpoint, expected_params)
    assert result == mock_podigee_response["episodes_list"]

@pytest.mark.asyncio
@patch("main.podigee_client.list_episodes", new_callable=AsyncMock)
async def test_list_episodes_tool_success(mock_list_episodes_api, mock_podigee_response):
    """Test the main.list_episodes tool formats output correctly."""
    mock_list_episodes_api.return_value = mock_podigee_response["episodes_list"]
    
    podcast_id = 42
    limit = 10 # Default limit in main
    search = "Episode"

    result = await main.list_episodes(podcast_id=podcast_id, search=search)
    
    # Check API call arguments
    mock_list_episodes_api.assert_called_once()
    call_args = mock_list_episodes_api.call_args[1]
    assert call_args['podcast_id'] == podcast_id
    assert call_args['limit'] == limit
    assert call_args['search'] == search
    assert call_args['offset'] is None
    assert call_args['published'] is None
    
    # Check formatted output string
    assert f"# Episodes Found (showing up to {limit})" in result
    assert "## First Episode (ID: 101)" in result
    assert "- Status: Published" in result
    assert "- Published Date: 2023-02-15" in result
    assert "## Second Episode Special (ID: 102)" in result
    assert "- Status: Unpublished" in result
    assert "- Published Date: None" in result
    assert "## Third Episode (ID: 103)" in result
    assert "- Status: Published" in result
    assert "- Published Date: 2023-03-01" in result

@pytest.mark.asyncio
@patch("main.podigee_client.list_episodes", new_callable=AsyncMock)
async def test_list_episodes_tool_limit_cap(mock_list_episodes_api):
    """Test the main.list_episodes tool caps the limit at 50."""
    mock_list_episodes_api.return_value = [] # Return empty list for simplicity
    
    await main.list_episodes(limit=100)
    
    mock_list_episodes_api.assert_called_once()
    call_args = mock_list_episodes_api.call_args[1]
    assert call_args['limit'] == 50 # Should be capped

@pytest.mark.asyncio
@patch("main.podigee_client.list_episodes", new_callable=AsyncMock)
async def test_list_episodes_tool_no_results(mock_list_episodes_api):
    """Test the main.list_episodes tool handles no results found."""
    mock_list_episodes_api.return_value = []
    
    result = await main.list_episodes(search="NonExistent")
    
    mock_list_episodes_api.assert_called_once()
    assert result == "No episodes found matching the criteria."

@pytest.mark.asyncio
@patch("main.podigee_client.list_episodes", new_callable=AsyncMock)
async def test_list_episodes_tool_api_error(mock_list_episodes_api):
    """Test the main.list_episodes tool handles API errors gracefully."""
    error_message = "Podigee API down"
    mock_list_episodes_api.side_effect = ValueError(error_message)
    
    result = await main.list_episodes()
    
    mock_list_episodes_api.assert_called_once()
    assert f"Error listing episodes: {error_message}" in result 

@pytest.mark.asyncio
@patch("podigee.api.PodigeeAPIClient.get", new_callable=AsyncMock)
async def test_get_podcast_details_api_client(mock_get):
    """Test the get_podcast_details method in the PodigeeAPIClient class."""
    # Setup mock podcast data
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
        "website_url": "https://example.com/podcast",
        "cover_image": "https://example.com/images/podcast-cover.jpg",
        "analytics_cover_image": "https://example.com/images/podcast-cover-small.jpg"
    }
    
    mock_get.return_value = test_podcast_data
    client = PodigeeAPIClient("test_api_key")
    
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
@patch("main.podigee_client.get_podcast_details", new_callable=AsyncMock)
async def test_get_podcast_details_tool_success(mock_get_details):
    """Test the get_podcast_details MCP tool with successful API response."""
    # Setup mock podcast data
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
        "website_url": "https://example.com/podcast",
        "cover_image": "https://example.com/images/podcast-cover.jpg",
        "analytics_cover_image": "https://example.com/images/podcast-cover-small.jpg"
    }
    
    mock_get_details.return_value = test_podcast_data
    
    # Call the tool
    result = await main.get_podcast_details(1234)
    
    # Verify the API client was called correctly
    mock_get_details.assert_called_once_with(podcast_id=1234, fields_filter=None)
    
    # Verify the formatted output contains expected data
    assert "# Podcast Details: Test Podcast" in result
    assert "ID: 1234" in result
    assert "Language: en" in result
    assert "Episodes Count: 10" in result
    assert "Publication Type: episodic" in result
    assert "Explicit Content: No" in result
    assert "This is a test podcast description." in result
    assert "test, podcast, API" in result
    assert "MP3: https://example.com/feed.mp3" in result
    assert "AAC: https://example.com/feed.aac" in result
    assert "Twitter: testpodcast" in result
    assert "Website: https://example.com/podcast" in result
    assert "Full Cover Image: https://example.com/images/podcast-cover.jpg" in result
    assert "Analytics Cover Image (128x128): https://example.com/images/podcast-cover-small.jpg" in result

@pytest.mark.asyncio
@patch("main.podigee_client.list_podcasts", new_callable=AsyncMock)
@patch("main.podigee_client.get_podcast_details", new_callable=AsyncMock)
async def test_get_podcast_details_tool_fallback_to_first_podcast(mock_get_details, mock_list_podcasts):
    """Test the get_podcast_details MCP tool with no podcast ID provided."""
    # Setup mock data
    mock_list_podcasts.return_value = [{"id": 5678, "title": "First Podcast"}]
    
    mock_get_details.return_value = {
        "id": 5678,
        "title": "First Podcast",
        "subtitle": "Auto-selected podcast",
        "description": "This podcast was auto-selected.",
        "language": "en",
        "publication_type": "episodic",
        "created_at": "2023-01-01T00:00:00Z",
        "cover_image": "https://example.com/images/first-podcast-cover.jpg",
        "analytics_cover_image": "https://example.com/images/first-podcast-cover-small.jpg"
    }
    
    # Call the tool without providing a podcast ID
    result = await main.get_podcast_details(None)
    
    # Verify list_podcasts was called to get the first podcast
    mock_list_podcasts.assert_called_once()
    
    # Verify get_podcast_details was called with the first podcast's ID
    mock_get_details.assert_called_once_with(podcast_id=5678, fields_filter=None)
    
    # Verify the formatted output contains expected data
    assert "# Podcast Details: First Podcast" in result
    assert "ID: 5678" in result
    assert "This podcast was auto-selected." in result

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_details", new_callable=AsyncMock)
async def test_get_podcast_details_tool_api_error(mock_get_details):
    """Test the get_podcast_details MCP tool with API error."""
    # Mock the client method to raise an error
    mock_get_details.side_effect = ValueError("API connection error")
    
    # Call the tool
    result = await main.get_podcast_details(1234)
    
    # Verify error is handled gracefully
    assert "Error fetching podcast details: API connection error" in result 

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_analytics_summary")
async def test_get_podcast_analytics_summary_explicit_dates(mock_analytics_summary, mock_podigee_response):
    """Test the get_podcast_analytics_summary tool with explicit date parameters"""
    # Configure the mock to return analytics and overview data
    mock_analytics_summary.return_value = (
        mock_podigee_response["analytics"],
        mock_podigee_response["overview"]
    )
    
    # Define explicit date range
    explicit_from_date = "2024-01-01"
    explicit_to_date = "2024-01-31"
    
    # Call the function with a specific podcast ID and explicit dates
    result = await main.get_podcast_analytics_summary(
        podcast_id=42,
        from_date=explicit_from_date,
        to_date=explicit_to_date
    )
    
    # Check that the API was called with the correct parameters
    mock_analytics_summary.assert_called_once()
    args, _ = mock_analytics_summary.call_args
    assert args[0] == 42
    assert args[1] == explicit_from_date
    assert args[2] == explicit_to_date
    
    # Verify result contains expected information
    assert "Podcast Analytics Summary" in result
    assert "Total Downloads: 150" in result
    assert "Unique Listeners: 500" in result

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_analytics_summary")
async def test_get_podcast_analytics_summary_days_offset_and_explicit_dates(mock_analytics_summary, mock_podigee_response):
    """Test that explicit dates override days_offset parameter"""
    # Configure the mock to return analytics and overview data
    mock_analytics_summary.return_value = (
        mock_podigee_response["analytics"],
        mock_podigee_response["overview"]
    )
    
    # Define explicit date range
    explicit_from_date = "2024-02-01"
    explicit_to_date = "2024-02-29"
    
    # Call the function with both days_offset and explicit dates (explicit dates should take precedence)
    result = await main.get_podcast_analytics_summary(
        podcast_id=42,
        days_offset=60,  # This should be ignored when explicit dates are provided
        from_date=explicit_from_date,
        to_date=explicit_to_date
    )
    
    # Check that the API was called with the explicit dates
    mock_analytics_summary.assert_called_once()
    args, _ = mock_analytics_summary.call_args
    assert args[0] == 42
    assert args[1] == explicit_from_date
    assert args[2] == explicit_to_date
    
    # Verify result contains expected information
    assert "Podcast Analytics Summary" in result
    assert "Total Downloads: 150" in result
    assert "Unique Listeners: 500" in result 

@pytest.mark.asyncio
@patch("podigee.api.PodigeeAPIClient.get", new_callable=AsyncMock)
async def test_get_podcast_episodes_analytics_api_client(mock_get, mock_podigee_response):
    """Test get_podcast_episodes_analytics API client method"""
    # Arrange
    mock_get.return_value = mock_podigee_response["podcast_episodes_batch"]
    client = PodigeeAPIClient("test_key")
    
    # Act
    podcast_id = 42
    from_date = "2023-03-01"
    to_date = "2023-03-31"
    limit = 10
    offset = 0
    result = await client.get_podcast_episodes_analytics(
        podcast_id=podcast_id,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset
    )
    
    # Assert
    mock_get.assert_called_once_with(
        f"podcasts/{podcast_id}/analytics/episodes", 
        {
            "from": from_date,
            "to": to_date,
            "limit": limit,
            "offset": offset
        }
    )
    assert result == mock_podigee_response["podcast_episodes_batch"]
    assert "objects" in result
    assert len(result["objects"]) == 3

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_episodes_analytics", new_callable=AsyncMock)
async def test_get_podcast_episodes_batch_analytics_tool_success(mock_batch_analytics, mock_podigee_response):
    """Test get_podcast_episodes_batch_analytics MCP tool with successful API response"""
    # Arrange
    mock_batch_analytics.return_value = mock_podigee_response["podcast_episodes_batch"]
    
    # Act
    podcast_id = 42
    from_date = "2023-03-01"
    to_date = "2023-03-31"
    result = await main.get_podcast_episodes_batch_analytics(
        podcast_id=podcast_id,
        from_date=from_date,
        to_date=to_date,
        limit=10
    )
    
    # Assert
    mock_batch_analytics.assert_called_once_with(
        podcast_id=podcast_id,
        from_date=from_date,
        to_date=to_date,
        limit=10,
        offset=None
    )
    
    # Check if the result contains key information
    assert "Batch Episode Analytics Summary" in result
    assert f"**Time Period:** {from_date} to {to_date}" in result
    assert f"**Podcast ID:** {podcast_id}" in result
    assert "## Episode Downloads" in result
    assert "First Episode" in result
    assert "Third Episode" in result
    assert "Fourth Episode" in result
    assert "250" in result  # Download count for First Episode
    assert "175" in result  # Download count for Third Episode
    assert "120" in result  # Download count for Fourth Episode
    
    # Check if the table format is correct
    assert "| ID | Title | Published Date | Downloads |" in result
    assert "lightweight download data" in result  # Check the note is included

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_episodes_analytics", new_callable=AsyncMock)
async def test_get_podcast_episodes_batch_analytics_tool_no_results(mock_batch_analytics):
    """Test get_podcast_episodes_batch_analytics MCP tool with no episodes found"""
    # Arrange
    mock_batch_analytics.return_value = {"objects": []}
    
    # Act
    podcast_id = 42
    result = await main.get_podcast_episodes_batch_analytics(podcast_id=podcast_id)
    
    # Assert
    assert f"No episode analytics data found for podcast ID {podcast_id}" in result

@pytest.mark.asyncio
@patch("main.podigee_client.get_podcast_episodes_analytics", new_callable=AsyncMock)
async def test_get_podcast_episodes_batch_analytics_tool_api_error(mock_batch_analytics):
    """Test get_podcast_episodes_batch_analytics MCP tool with API error"""
    # Arrange
    error_message = "API connection error"
    mock_batch_analytics.side_effect = ValueError(error_message)
    
    # Act
    podcast_id = 42
    result = await main.get_podcast_episodes_batch_analytics(podcast_id=podcast_id)
    
    # Assert
    assert "Error fetching batch episode analytics" in result
    assert error_message in result 