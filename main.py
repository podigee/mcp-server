#!/usr/bin/env python3
"""
Podigee MCP Server - MVP

A Model Context Protocol server that interfaces with the Podigee API to provide
podcast analytics data to MCP client hosts like Claude Desktop or other MCP-compatible
applications.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from datetime import datetime, timedelta
from collections import defaultdict

from podigee.api import PodigeeAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("podigee-mcp")

# Load environment variables from .env file
load_dotenv()

# Initialize the MCP server with a name
mcp = FastMCP("Podigee")

# Initialize the Podigee API client
podigee_client = PodigeeAPIClient()

# Helper function for backward compatibility with tests
async def podigee_api_request(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make an authenticated request to the Podigee API.
    
    Args:
        endpoint: API endpoint path (without the base URL)
        params: Optional query parameters
        
    Returns:
        JSON response from the API
    """
    return await podigee_client.get(endpoint, params)

# Helper function to generate attribution footer
def get_attribution_footer() -> str:
    """
    Generate standardized attribution footer for all analytics reports.
    Required for all free MCP server users who host with Podigee on Advanced or Business Pro plans.
    
    Returns:
        Formatted attribution footer string
    """
    current_date = datetime.now().strftime("%B %d, %Y")
    
    return f"\n\n---\n*Data Source: Podigee Analytics API | Generated on {current_date}*"

# Tool implementations
@mcp.tool()
async def get_podcast_analytics_summary(podcast_id = None, days_offset = 30, from_date = None, to_date = None) -> str:
    """
    Get a summary of podcast analytics for the specified podcast.
    
    Args:
        podcast_id: The ID of the podcast to fetch analytics for. If not provided, 
                  will fetch analytics for the first podcast associated with the API key.
        days_offset: Number of days to look back for analytics data (default: 30)
        from_date: Start date in YYYY-MM-DD format. If provided with to_date, overrides days_offset.
        to_date: End date in YYYY-MM-DD format. If provided with from_date, overrides days_offset.
        
    Returns:
        A formatted summary of podcast analytics
        
    Note:
        All reports generated through this MCP Server include attribution to Podigee Analytics API in the footer.
    """
    try:
        # Check if explicit date range is provided
        if from_date and to_date:
            # Use explicit date range
            calculated_from_date = from_date
            calculated_to_date = to_date
        else:
            # Calculate default date range based on days_offset
            calculated_to_date = datetime.now().strftime("%Y-%m-%d")
            calculated_from_date = (datetime.now() - timedelta(days=days_offset)).strftime("%Y-%m-%d")
            
        # Fetch analytics and overview data using the client
        analytics_data, overview_data = await podigee_client.get_podcast_analytics_summary(
            podcast_id, calculated_from_date, calculated_to_date
        )
        
        # Format the analytics data into a readable summary
        return format_analytics_summary(analytics_data, overview_data)
    except ValueError as e:
        return f"Error fetching podcast analytics: {str(e)}"

def format_analytics_summary(analytics_data: Dict[str, Any], overview_data: Dict[str, Any]) -> str:
    """
    Format analytics data into a readable summary, including detailed breakdowns.
    
    Args:
        analytics_data: Raw analytics data from the Podigee API
        overview_data: Raw overview data from the Podigee API
        
    Returns:
        Formatted analytics summary as string
    """
    meta = analytics_data.get("meta", {})
    timerange = meta.get("timerange", {})
    
    # Safely extract and format dates
    start_datetime_raw = timerange.get("start_datetime")
    end_datetime_raw = timerange.get("end_datetime")

    start_date = "unknown"
    if isinstance(start_datetime_raw, str):
        try:
            start_date = start_datetime_raw.split('T')[0]
        except IndexError:
            start_date = start_datetime_raw # Handle cases where 'T' might be missing
    elif start_datetime_raw is not None:
        logger.warning(f"Unexpected type for start_datetime: {type(start_datetime_raw)}, value: {start_datetime_raw}")
        start_date = str(start_datetime_raw) # Fallback to string conversion

    end_date = "unknown"
    if isinstance(end_datetime_raw, str):
        try:
            end_date = end_datetime_raw.split('T')[0]
        except IndexError:
            end_date = end_datetime_raw
    elif end_datetime_raw is not None:
        logger.warning(f"Unexpected type for end_datetime: {type(end_datetime_raw)}, value: {end_datetime_raw}")
        end_date = str(end_datetime_raw)
        
    # Initialize aggregators
    total_downloads = 0
    download_by_day = {}
    formats_agg = defaultdict(int)
    platforms_agg = defaultdict(int)
    countries_agg = defaultdict(int)
    clients_agg = defaultdict(int)
    clients_on_platforms_agg = defaultdict(int)

    # Aggregate data from daily objects
    for obj in analytics_data.get("objects", []):
        daily_downloads = obj.get("downloads", {}).get("complete", 0)
        total_downloads += daily_downloads
        
        # Safely extract and format date
        downloaded_on_raw = obj.get("downloaded_on")
        date = "unknown"
        if isinstance(downloaded_on_raw, str):
            try:
                date = downloaded_on_raw.split('T')[0]
            except IndexError:
                date = downloaded_on_raw
        elif downloaded_on_raw is not None:
            logger.warning(f"Unexpected type for downloaded_on: {type(downloaded_on_raw)}, value: {downloaded_on_raw}")
            date = str(downloaded_on_raw)
            
        download_by_day[date] = daily_downloads
        
        # Aggregate detailed breakdowns - expecting integer counts directly
        for key, count in obj.get("formats", {}).items():
            if isinstance(count, int):
                formats_agg[key] += count
            else:
                 logger.warning(f"Unexpected value type for formats key '{key}': {type(count)}, value: {count}")
                 
        for key, count in obj.get("platforms", {}).items():
            if isinstance(count, int):
                platforms_agg[key] += count
            else:
                 logger.warning(f"Unexpected value type for platforms key '{key}': {type(count)}, value: {count}")
                 
        for key, count in obj.get("countries", {}).items():
            if isinstance(count, int):
                countries_agg[key] += count
            else:
                 logger.warning(f"Unexpected value type for countries key '{key}': {type(count)}, value: {count}")
                 
        for key, count in obj.get("clients", {}).items():
            if isinstance(count, int):
                clients_agg[key] += count
            else:
                 logger.warning(f"Unexpected value type for clients key '{key}': {type(count)}, value: {count}")
                 
        for key, count in obj.get("clients_on_platforms", {}).items():
             if isinstance(count, int):
                clients_on_platforms_agg[key] += count
             else:
                 logger.warning(f"Unexpected value type for clients_on_platforms key '{key}': {type(count)}, value: {count}")

    # Get overview stats
    unique_listeners = overview_data.get("unique_listeners_number", "N/A")
    unique_subscribers = overview_data.get("unique_subscribers_number", "N/A")
    episodes_count = overview_data.get("published_episodes_count", "N/A")
    mean_downloads = overview_data.get("mean_episode_download", "N/A")
    
    # Format top episodes
    top_episodes = ""
    for idx, episode in enumerate(overview_data.get("top_episodes", [])[:5], 1):
        title = episode.get("title", "Unknown")
        downloads = episode.get("downloads", 0)
        top_episodes += f"{idx}. {title}: {downloads} downloads\n"
    
    # Helper function to format top items
    def format_top_items(agg_dict: Dict[str, int], title: str, top_n: int = 5) -> str:
        if not agg_dict:
            return f"## Top {title}\nNo data available.\n\n"
        
        sorted_items = sorted(agg_dict.items(), key=lambda item: item[1], reverse=True)
        formatted_list = f"## Top {title}\n"
        for i, (item, count) in enumerate(sorted_items[:top_n], 1):
            formatted_list += f"{i}. {item}: {count} downloads\n"
        return formatted_list + "\n"

    # Format aggregated data
    top_formats = format_top_items(formats_agg, "Formats")
    top_platforms = format_top_items(platforms_agg, "Platforms")
    top_countries = format_top_items(countries_agg, "Countries")
    top_clients = format_top_items(clients_agg, "Clients")
    top_clients_on_platforms = format_top_items(clients_on_platforms_agg, "Clients on Platforms", top_n=10) # Show more for this breakdown

    # Create the formatted summary
    summary = f"""
# Podcast Analytics Summary
**Time Period:** {start_date} to {end_date}

## Overview Stats
- Total Downloads: {total_downloads}
- Unique Listeners: {unique_listeners}
- Unique Subscribers: {unique_subscribers}
- Published Episodes: {episodes_count}
- Average Downloads per Episode: {mean_downloads}

## Top Episodes
{top_episodes}
{top_formats}{top_platforms}{top_countries}{top_clients}{top_clients_on_platforms}
"""
    # Add attribution footer
    summary += get_attribution_footer()
    
    return summary

@mcp.tool()
async def list_podcasts(random_string = "") -> str:
    """
    List all podcasts associated with the Podigee API key.
    
    Returns:
        A formatted list of podcasts
    """
    try:
        podcasts = await podigee_client.list_podcasts()
        
        if not podcasts or len(podcasts) == 0:
            return "No podcasts found associated with this API key."
        
        # Format podcast info into a readable list
        result = "# Your Podcasts\n\n"
        for podcast in podcasts:
            podcast_id = podcast.get("id", "Unknown")
            title = podcast.get("title", "Untitled")
            language = podcast.get("language", "Unknown")
            created_at = podcast.get("created_at", "Unknown")
            
            result += f"## {title}\n"
            result += f"- ID: {podcast_id}\n"
            result += f"- Language: {language}\n"
            result += f"- Created: {created_at}\n\n"
        
        return result
    except ValueError as e:
        return f"Error fetching podcasts: {str(e)}"

@mcp.tool()
async def list_episodes(
    podcast_id = None,
    limit = 10, # Default limit to avoid overly long responses
    offset = None,
    published = None,
    publication_type = None, # 'full', 'trailer', 'bonus'
    sort_by = None,
    sort_direction = None, # 'asc', 'desc'
    search = None
) -> str:
    """
    List episodes, optionally filtering by podcast ID, publication status, 
    type, sorting, and searching by title.

    Args:
        podcast_id: Filter episodes by this podcast ID.
        limit: Maximum number of episodes to return (default 10, max 50).
        offset: Skip the first N episodes (for pagination).
        published: Set to true to only get published episodes, false for unpublished.
        publication_type: Filter by type ('full', 'trailer', 'bonus').
        sort_by: Field to sort by (e.g., 'published_at', 'created_at', 'title').
        sort_direction: Sort order ('asc' for ascending, 'desc' for descending).
        search: Search term to filter episodes by title.

    Returns:
        A formatted string listing the episodes found.
    """
    try:
        # Validate limit
        if limit is not None and limit > 50:
            limit = 50
            logger.warning("Limit parameter capped at 50.")
            
        episodes = await podigee_client.list_episodes(
            podcast_id=podcast_id,
            limit=limit,
            offset=offset,
            published=published,
            publication_type=publication_type,
            sort_by=sort_by,
            sort_direction=sort_direction,
            search=search
        )
        
        if not episodes:
            return "No episodes found matching the criteria."
            
        result = f"# Episodes Found (showing up to {limit or 'all'})\n\n"
        for episode in episodes:
            ep_id = episode.get("id", "N/A")
            title = episode.get("title", "Untitled")
            pub_status = "Published" if episode.get("published_at") else "Unpublished"
            pub_date = episode.get("published_at", "N/A")
            if pub_date and 'T' in pub_date:
                pub_date = pub_date.split('T')[0] # Just show date
            
            result += f"## {title} (ID: {ep_id})\n"
            result += f"- Status: {pub_status}\n"
            result += f"- Published Date: {pub_date}\n\n"
            
        return result
    except ValueError as e:
        return f"Error listing episodes: {str(e)}"

@mcp.tool()
async def get_episode_analytics(
    episode_id,
    from_date = None,
    to_date = None,
    days_since_published = None,
    granularity = None
) -> str:
    """
    Get analytics data for a specific episode.
    
    Args:
        episode_id: ID of the episode to fetch analytics for
        from_date: Start date in YYYY-MM-DD format (e.g., "2024-01-01"). Must be used with 'to_date'.
        to_date: End date in YYYY-MM-DD format (e.g., "2024-01-31"). Must be used with 'from_date'.
        days_since_published: Number of days since the episode was published to include in analytics.
                            Cannot be used together with 'from_date'/'to_date'.
        granularity: Aggregation granularity ('hour', 'day', 'week', 'month').
                    If not given, will be calculated based on the time interval.
                    
    Returns:
        A formatted summary of episode analytics
        
    Note:
        All reports generated through this MCP Server include attribution to Podigee Analytics API in the footer.
    """
    try:
        analytics_data = await podigee_client.get_episode_analytics(
            episode_id=episode_id,
            from_date=from_date,
            to_date=to_date,
            days_since_published=days_since_published,
            granularity=granularity
        )
        
        # Extract metadata
        meta = analytics_data.get("meta", {})
        timerange = meta.get("timerange", {})
        start_date = timerange.get("start_datetime", "N/A")
        end_date = timerange.get("end_datetime", "N/A")
        granularity = meta.get("aggregation_granularity", "N/A")
        
        # Initialize aggregators for different metrics
        total_downloads = 0
        formats_agg = defaultdict(int)
        platforms_agg = defaultdict(int)
        countries_agg = defaultdict(int)
        clients_agg = defaultdict(int)
        clients_on_platforms_agg = defaultdict(int)
        
        # Aggregate data across all time periods
        for obj in analytics_data.get("objects", []):
            # Sum up total downloads
            if "downloads" in obj and "complete" in obj["downloads"]:
                if isinstance(obj["downloads"]["complete"], (int, float)):
                    total_downloads += obj["downloads"]["complete"]
                else:
                    logger.warning(f"Unexpected type for downloads.complete: {type(obj['downloads']['complete'])}")
            
            # Aggregate formats
            for format_name, count in obj.get("formats", {}).items():
                if isinstance(count, (int, float)):
                    formats_agg[format_name] += count
                else:
                    logger.warning(f"Unexpected type for formats value: {type(count)}")
            
            # Aggregate platforms
            for platform, count in obj.get("platforms", {}).items():
                if isinstance(count, (int, float)):
                    platforms_agg[platform] += count
                else:
                    logger.warning(f"Unexpected type for platforms value: {type(count)}")
            
            # Aggregate countries
            for country, count in obj.get("countries", {}).items():
                if isinstance(count, (int, float)):
                    countries_agg[country] += count
                else:
                    logger.warning(f"Unexpected type for countries value: {type(count)}")
            
            # Aggregate clients
            for client, count in obj.get("clients", {}).items():
                if isinstance(count, (int, float)):
                    clients_agg[client] += count
                else:
                    logger.warning(f"Unexpected type for clients value: {type(count)}")
            
            # Aggregate clients on platforms
            for key, count in obj.get("clients_on_platforms", {}).items():
                if isinstance(count, (int, float)):
                    clients_on_platforms_agg[key] += count
                else:
                    logger.warning(f"Unexpected type for clients_on_platforms value: {type(count)}")
        
        # Helper function to format top items
        def format_top_items(agg_dict: Dict[str, int], title: str, top_n: int = 5) -> str:
            if not agg_dict:
                return f"## Top {title}\nNo data available.\n\n"
            
            sorted_items = sorted(agg_dict.items(), key=lambda item: item[1], reverse=True)
            formatted_list = f"## Top {title}\n"
            for i, (item, count) in enumerate(sorted_items[:top_n], 1):
                formatted_list += f"{i}. {item}: {count} downloads\n"
            return formatted_list + "\n"
        
        # Format aggregated data
        top_formats = format_top_items(formats_agg, "Formats")
        top_platforms = format_top_items(platforms_agg, "Platforms")
        top_countries = format_top_items(countries_agg, "Countries")
        top_clients = format_top_items(clients_agg, "Clients")
        top_clients_on_platforms = format_top_items(clients_on_platforms_agg, "Clients on Platforms", top_n=10)
        
        # Create the formatted summary
        summary = f"""
# Episode Analytics Summary
**Time Period:** {start_date} to {end_date}
**Granularity:** {granularity}

## Overview Stats
- Total Downloads: {total_downloads}

{top_formats}{top_platforms}{top_countries}{top_clients}{top_clients_on_platforms}
"""
        # Add attribution footer
        summary += get_attribution_footer()
        
        return summary
    except ValueError as e:
        return f"Error fetching episode analytics: {str(e)}"

@mcp.tool()
async def get_podcast_details(
    podcast_id,
    fields_filter = None
) -> str:
    """
    Get detailed metadata for a podcast.
    
    Args:
        podcast_id: ID of the podcast to fetch details for
        fields_filter: Optional list of specific fields to include in the response
        
    Returns:
        A formatted summary of podcast metadata
        
    Note:
        All reports generated through this MCP Server include attribution to Podigee Analytics API in the footer.
    """
    try:
        if not podcast_id:
            # If podcast_id is not provided, attempt to use the first podcast
            podcasts = await podigee_client.list_podcasts()
            if not podcasts or len(podcasts) == 0:
                return "Error: No podcast ID provided and no podcasts found in your account."
            podcast_id = podcasts[0]["id"]
            logger.info(f"No podcast ID provided, using first podcast: {podcast_id}")
        
        podcast_data = await podigee_client.get_podcast_details(
            podcast_id=podcast_id,
            fields_filter=fields_filter
        )
        
        if not podcast_data:
            return f"No podcast found with ID {podcast_id}."
            
        # Extract important metadata
        title = podcast_data.get("title", "Untitled")
        subtitle = podcast_data.get("subtitle", "")
        description = podcast_data.get("description", "No description available.")
        language = podcast_data.get("language", "Not specified")
        episodes_count = podcast_data.get("episodes_count", "N/A")
        category_id = podcast_data.get("category_id", None)
        publication_type = podcast_data.get("publication_type", "Not specified")
        explicit = "Yes" if podcast_data.get("explicit", False) else "No"
        created_at = podcast_data.get("created_at", "Unknown")
        published_at = podcast_data.get("published_at", "Not published")
        
        # Extract cover art URLs - prominently featured
        cover_image_url = podcast_data.get("cover_image", "Not available")
        analytics_cover_image_url = podcast_data.get("analytics_cover_image", "Not available")
        
        # Format feed information if available
        feeds_info = ""
        feeds = podcast_data.get("feeds", [])
        if feeds:
            feeds_info = "\n## Feed Information\n"
            for i, feed in enumerate(feeds, 1):
                format_type = feed.get("format", "Unknown")
                url = feed.get("url", "No URL available")
                feeds_info += f"{i}. {format_type.upper()}: {url}\n"
        
        # Format keywords if available
        keywords_info = ""
        keywords = podcast_data.get("keywords", [])
        if keywords:
            keywords_info = "\n## Keywords\n"
            keywords_info += ", ".join(keywords)
            keywords_info += "\n"
        
        # Format social media information if available
        social_info = "\n## Social Media\n"
        if podcast_data.get("twitter"):
            social_info += f"- Twitter: {podcast_data.get('twitter')}\n"
        if podcast_data.get("facebook"):
            social_info += f"- Facebook: {podcast_data.get('facebook')}\n"
        if podcast_data.get("website_url"):
            social_info += f"- Website: {podcast_data.get('website_url')}\n"
        if podcast_data.get("spotify_url"):
            social_info += f"- Spotify: {podcast_data.get('spotify_url')}\n"
        if podcast_data.get("deezer_url"):
            social_info += f"- Deezer: {podcast_data.get('deezer_url')}\n"
        if podcast_data.get("alexa_url"):
            social_info += f"- Amazon/Alexa: {podcast_data.get('alexa_url')}\n"
        if podcast_data.get("itunes_id"):
            social_info += f"- iTunes ID: {podcast_data.get('itunes_id')}\n"
        
        if social_info == "\n## Social Media\n":
            social_info = ""
        
        # Create the formatted summary
        summary = f"""
# Podcast Details: {title}

## Cover Artwork
- Full Cover Image: {cover_image_url}
- Analytics Cover Image (128x128): {analytics_cover_image_url}

## General Information
- ID: {podcast_id}
- Subtitle: {subtitle}
- Language: {language}
- Episodes Count: {episodes_count}
- Publication Type: {publication_type}
- Explicit Content: {explicit}
- Created: {created_at}
- Published: {published_at}

## Description
{description}
{keywords_info}{feeds_info}{social_info}
"""
        # Add attribution footer
        summary += get_attribution_footer()
        
        return summary
    except ValueError as e:
        return f"Error fetching podcast details: {str(e)}"

@mcp.tool()
async def get_podcast_episodes_batch_analytics(
    podcast_id,
    from_date = None,
    to_date = None,
    limit = None,
    offset = None
) -> str:
    """
    Get download analytics for multiple episodes of a podcast in a single batch.
    
    This tool provides a lightweight alternative to fetching full analytics for each episode
    individually. It returns only download counts with basic episode metadata for multiple episodes
    at once, which is much faster and more efficient than individual episode analytics requests.
    
    Args:
        podcast_id: ID of the podcast to fetch episode analytics for.
        from_date: Start date in YYYY-MM-DD format (default: 30 days ago).
        to_date: End date in YYYY-MM-DD format (default: today).
        limit: Maximum number of episodes to return (max 50).
        offset: Skip the first N episodes (for pagination).
        
    Returns:
        A formatted summary of episode download analytics.
        
    Note:
        All reports generated through this MCP Server include attribution to Podigee Analytics API in the footer.
    """
    try:
        # Set default date range if not provided
        if not from_date or not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Fetch batch episode analytics
        batch_analytics = await podigee_client.get_podcast_episodes_analytics(
            podcast_id=podcast_id,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset
        )
        
        # Extract episodes data
        episodes = batch_analytics.get("objects", [])
        
        if not episodes:
            return f"No episode analytics data found for podcast ID {podcast_id} in the specified time range."
        
        # Format the analytics data into a readable summary
        summary = f"""
# Batch Episode Analytics Summary
**Time Period:** {from_date} to {to_date}
**Podcast ID:** {podcast_id}

## Episode Downloads
| ID | Title | Published Date | Downloads |
|---|---|---|---|
"""
        # Add a row for each episode
        for episode in episodes:
            ep_id = episode.get("id", "N/A")
            title = episode.get("title", "Untitled")
            published_at = episode.get("published_at", "N/A")
            if published_at and 'T' in published_at:
                published_at = published_at.split('T')[0]  # Just show date
            downloads = episode.get("downloads", 0)
            
            summary += f"| {ep_id} | {title} | {published_at} | {downloads} |\n"
        
        # Add note about the lightweight nature of this data
        summary += """
## Note
This is lightweight download data intended for quick comparison across multiple episodes.
For detailed analytics breakdowns (e.g., by country, client, platform), use the `get_episode_analytics` 
tool on individual episodes.
"""
        # Add attribution footer
        summary += get_attribution_footer()
        
        return summary
    except ValueError as e:
        return f"Error fetching batch episode analytics: {str(e)}"

# Run the server if executed directly
if __name__ == "__main__":
    mcp.run()
