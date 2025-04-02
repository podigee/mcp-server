"""
Podigee API client module for interacting with the Podigee API.
"""

import os
import logging
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timedelta

import httpx

logger = logging.getLogger(__name__)

# Constants
PODIGEE_API_BASE_URL = "https://app.podigee.com/api/v1"


class PodigeeAPIClient:
    """
    Client for interacting with the Podigee API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Podigee API client.
        
        Args:
            api_key: Podigee API key (if not provided, will be read from PODIGEE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("PODIGEE_API_KEY")
        
        if not self.api_key:
            logger.warning("No Podigee API key provided. API calls will fail.")
        
        self.headers = {
            "Token": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the Podigee API.
        
        Args:
            endpoint: API endpoint path (without the base URL)
            params: Optional query parameters
            
        Returns:
            JSON response from the API
            
        Raises:
            ValueError: If the API request fails
        """
        url = f"{PODIGEE_API_BASE_URL}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {str(e)}")
                raise ValueError(f"Failed to fetch data from Podigee API: {str(e)}")
            except Exception as e:
                logger.error(f"Error during Podigee API request: {str(e)}")
                raise ValueError(f"Error during API request: {str(e)}")
    
    async def list_podcasts(self) -> Dict[str, Any]:
        """
        Get a list of all podcasts associated with the API key.
        
        Returns:
            List of podcasts
        """
        return await self.get("podcasts")
    
    def _get_default_date_range(self, days: int = 30) -> Tuple[str, str]:
        """
        Helper method to get default date range.
        
        Args:
            days: Number of days to look back (default 30)
            
        Returns:
            Tuple of (from_date, to_date) in YYYY-MM-DD format
        """
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return from_date, to_date
    
    async def get_podcast_analytics(self, podcast_id: int, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get analytics data for a podcast.
        
        Args:
            podcast_id: ID of the podcast to fetch analytics for
            from_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            to_date: End date in YYYY-MM-DD format (default: today)
            
        Returns:
            Analytics data
        """
        if not from_date or not to_date:
            from_date, to_date = self._get_default_date_range()
        
        params = {
            "from": from_date,
            "to": to_date
        }
        
        return await self.get(f"podcasts/{podcast_id}/analytics", params)
    
    async def get_podcast_overview(self, podcast_id: int, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get overview data for a podcast.
        
        Args:
            podcast_id: ID of the podcast to fetch overview for
            from_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            to_date: End date in YYYY-MM-DD format (default: today)
            
        Returns:
            Overview data
        """
        if not from_date or not to_date:
            from_date, to_date = self._get_default_date_range()
        
        params = {
            "from": from_date,
            "to": to_date
        }
        
        return await self.get(f"podcasts/{podcast_id}/overview", params)
    
    async def get_podcast_listeners(self, podcast_id: int) -> Dict[str, Any]:
        """
        Get listeners data for a podcast.
        
        Args:
            podcast_id: ID of the podcast to fetch listeners for
            
        Returns:
            Listeners data
        """
        return await self.get(f"podcasts/{podcast_id}/analytics/listeners")
    
    async def get_podcast_analytics_summary(
        self, 
        podcast_id: Optional[int] = None, 
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get a summary of podcast analytics and overview data.
        
        Args:
            podcast_id: ID of the podcast to fetch analytics for. If not provided, 
                      will fetch analytics for the first podcast associated with the API key.
            from_date: Start date in YYYY-MM-DD format (default: 30 days ago)
            to_date: End date in YYYY-MM-DD format (default: today)
            
        Returns:
            Tuple of (analytics_data, overview_data)
            
        Raises:
            ValueError: If no podcast ID is provided and no podcasts are found
        """
        # If podcast_id is not provided, fetch the first podcast
        if not podcast_id:
            podcasts = await self.list_podcasts()
            if not podcasts or len(podcasts) == 0:
                raise ValueError("No podcasts found associated with this API key")
            podcast_id = podcasts[0]["id"]
            logger.info(f"No podcast ID provided, using first podcast from account: {podcast_id}")
        
        # Fetch analytics and overview data
        analytics_data = await self.get_podcast_analytics(podcast_id, from_date, to_date)
        overview_data = await self.get_podcast_overview(podcast_id, from_date, to_date)
        
        return analytics_data, overview_data

    async def get_episode_analytics(
        self, 
        episode_id: int, 
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None,
        days_since_published: Optional[int] = None,
        granularity: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get analytics data for a specific episode.

        Args:
            episode_id: ID of the episode to fetch analytics for.
            from_date: Start date in YYYY-MM-DD format. Must be used with 'to_date'.
            to_date: End date in YYYY-MM-DD format. Must be used with 'from_date'.
            days_since_published: Number of days since the episode was published 
                                   to include in the analytics calculation. 
                                   Cannot be used with 'from_date'/'to_date'.
            granularity: Aggregation granularity ('hour', 'day', 'week', 'month'). 
                         If not given, it will be calculated based on the time interval.

        Returns:
            Episode analytics data.

        Raises:
            ValueError: If 'from_date'/'to_date' and 'days_since_published' are used together,
                      or if the API request fails.
        """
        if (from_date or to_date) and days_since_published:
            raise ValueError("Cannot use 'from_date'/'to_date' and 'days_since_published' together.")

        params: Dict[str, Any] = {}
        if from_date and to_date:
            params["from"] = from_date
            params["to"] = to_date
        elif days_since_published is not None:
            params["days_since_published"] = days_since_published
        
        if granularity:
            params["granularity"] = granularity

        endpoint = f"episodes/{episode_id}/analytics"
        return await self.get(endpoint, params)

    async def list_episodes(
        self,
        podcast_id: Optional[int] = None,
        podcast_ids: Optional[List[int]] = None,
        limit_per_podcast: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        published: Optional[bool] = None,
        publication_type: Optional[str] = None, # full, trailer, bonus
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None, # asc, desc
        search: Optional[str] = None,
        fields_filter: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get a list of episodes, optionally filtered and sorted.

        Args:
            podcast_id: ID of a single podcast to filter by.
            podcast_ids: List of podcast IDs to filter by.
            limit_per_podcast: Max episodes per podcast (requires podcast_ids).
            limit: Max total episodes to return (max 50).
            offset: Skip episodes for pagination.
            published: Filter by published status.
            publication_type: Filter by publication type ('full', 'trailer', 'bonus').
            sort_by: Field to sort by.
            sort_direction: Sort direction ('asc', 'desc').
            search: Full-text search string (searches title only).
            fields_filter: List of fields to include in the response.

        Returns:
            List of episode dictionaries.

        Raises:
            ValueError: If the API request fails.
        """
        params: Dict[str, Any] = {}
        if podcast_id is not None:
            params["podcast_id"] = podcast_id
        if podcast_ids is not None:
            # httpx handles list parameters correctly
            params["podcast_ids[]"] = podcast_ids 
        if limit_per_podcast is not None:
            params["limit_per_podcast"] = limit_per_podcast
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if published is not None:
            params["published"] = published
        if publication_type is not None:
            params["publication_type"] = publication_type
        if sort_by is not None:
            params["sort_by"] = sort_by
        if sort_direction is not None:
            params["sort_direction"] = sort_direction
        if search is not None:
            params["search"] = search
        if fields_filter is not None:
            params["fields_filter[]"] = fields_filter

        # The API returns the list directly, not nested in a dict
        return await self.get("episodes", params)
        
    async def get_podcast_details(
        self, 
        podcast_id: int,
        fields_filter: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get detailed metadata for a specific podcast.
        
        Args:
            podcast_id: ID of the podcast to fetch details for.
            fields_filter: Optional list of fields to include in the response.
            
        Returns:
            Detailed podcast metadata dictionary.
            
        Raises:
            ValueError: If the API request fails.
        """
        params: Dict[str, Any] = {}
        if fields_filter is not None:
            params["fields_filter[]"] = fields_filter
            
        response = await self.get(f"podcasts/{podcast_id}", params)
        # The API returns the podcast data directly, not in a list
        return response 
        
    async def get_podcast_episodes_analytics(
        self,
        podcast_id: int,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get batch analytics data for multiple episodes of a podcast.
        
        This endpoint provides a lightweight alternative to fetching full analytics
        for multiple episodes individually. It returns only the download count and
        basic episode metadata for each episode.
        
        Args:
            podcast_id: ID of the podcast to fetch episode analytics for.
            from_date: Start date in YYYY-MM-DD format. Must be used with 'to_date'.
            to_date: End date in YYYY-MM-DD format. Must be used with 'from_date'.
            limit: Maximum number of episodes to return (default defined by API, max 50).
            offset: Skip the first N episodes (for pagination).
            
        Returns:
            Dictionary containing an 'objects' array with episode analytics data.
            
        Raises:
            ValueError: If the API request fails.
        """
        if not from_date or not to_date:
            from_date, to_date = self._get_default_date_range()
            
        params: Dict[str, Any] = {
            "from": from_date,
            "to": to_date
        }
        
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
            
        endpoint = f"podcasts/{podcast_id}/analytics/episodes"
        return await self.get(endpoint, params) 