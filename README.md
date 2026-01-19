# Podigee MCP Server

A Model Context Protocol (MCP) server that connects AI agents and MCP hosts like Claude Desktop to the Podigee podcast hosting platform.

## Overview

The Podigee MCP Server acts as a bridge between AI assistants and the Podigee podcast platform, enabling AI assistants to retrieve podcast analytics data through a standardized protocol. This server makes podcast data accessible to AI agents without requiring them to understand the specifics of the Podigee API.

## Features

- **Authentication**: Securely authenticate with the Podigee API using an API token
- **Podcast Analytics**: Retrieve comprehensive analytics for podcasts
- **Podcast Listing**: List all podcasts associated with your Podigee account

## Requirements

- Python 3.10 or higher
- A Podigee account with an API token

## What is Podigee?

[Podigee](https://www.podigee.com/en/) is a great podcast hosting platform with global presence that provides tools for publishing, analyzing, and monetizing podcasts. Podigee is perfect for businesses of all sizes, as well as marketing and communications agencies and independent podcast creators that want a solution that is intuitive, yet powerful, robust and elegant.

This MCP server allows AI agents to interact with data from your Podigee account via the [Podigee API](https://app.podigee.com/api-docs).

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/XXX/pod-mcp.git
   cd pod-mcp
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up your Podigee API token in a `.env` file:
   ```
   PODIGEE_API_KEY=your_api_key_here
   ```

## Usage

### Running the server directly

```
python main.py
```

### Installing in Claude Desktop

1. Make sure you have [Claude Desktop](https://claude.ai/desktop) installed
2. Edit the Claude Desktop config file at `~/Library/Application Support/Claude/claude_desktop_config.json` (create it if it doesn't exist):

```json
{
    "mcpServers": {
        "podigee": {
            "command": "python",
            "args": [
                "/path/to/pod-mcp/main.py"
            ],
            "env": {
                "PODIGEE_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

3. Restart Claude Desktop




### Follow logs in real-time
Review detailed MCP logs from Claude Desktop:

```
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

The logs capture:

- Server connection events
- Configuration issues
- Runtime errors
- Message exchanges​


### Installing in Cursor

1.  Open Cursor settings:
    *   On macOS: `Cursor` -> `Settings`
    *   On Windows/Linux: `File` -> `Preferences` -> `Settings`
2.  Navigate to the `Cursor Settings` section in the left sidebar.
3.  Find the `MCP Servers` configuration setting. Click `Add new global MCP server` and update the configuration for the `podigee` server, similar to the Claude Desktop setup.


## Available Tools

The Podigee MCP Server exposes the following tools:

1. `get_podcast_analytics_summary` - Get a summary of podcast analytics
   - Parameters:
     - `podcast_id` (optional): The ID of the podcast to analyze. If not provided, uses the first podcast.
     - `days_offset` (optional, default: 30): Number of days to look back.
     - `from_date` (optional): Start date in YYYY-MM-DD format.
     - `to_date` (optional): End date in YYYY-MM-DD format.
   - Returns: Comprehensive analytics including downloads, unique listeners, top episodes, and breakdowns by format, platform, country, and client.

2. `list_podcasts` - List all podcasts associated with your Podigee account
   - Returns: A formatted list of podcasts with their IDs, titles, languages, and creation dates.

3. `list_episodes` - List episodes with flexible filtering options
   - Parameters:
     - `podcast_id` (optional): Filter episodes by podcast ID.
     - `limit` (optional, default: 10, max: 50): Maximum number of episodes to return.
     - `offset` (optional): Skip the first N episodes for pagination.
     - `published` (optional): Filter by publication status (true/false).
     - `publication_type` (optional): Filter by type ('full', 'trailer', 'bonus').
     - `sort_by` (optional): Field to sort by (e.g., 'published_at', 'created_at', 'title').
     - `sort_direction` (optional): Sort order ('asc'/'desc').
     - `search` (optional): Search term to filter episodes by title.
   - Returns: A formatted list of episodes with their IDs, titles, and publication status.

4. `get_episode_analytics` - Get detailed analytics for a specific episode
   - Parameters:
     - `episode_id` (required): ID of the episode to analyze.
     - `from_date` (optional): Start date in YYYY-MM-DD format.
     - `to_date` (optional): End date in YYYY-MM-DD format.
     - `days_since_published` (optional): Number of days since publication to analyze.
     - `granularity` (optional): Data aggregation level ('hour', 'day', 'week', 'month').
   - Returns: Comprehensive episode analytics including downloads and breakdowns by format, platform, country, and client.

5. `get_podcast_details` - Get detailed metadata for a podcast
   - Parameters:
     - `podcast_id` (required): ID of the podcast to fetch details for.
     - `fields_filter` (optional): List of specific fields to include.
   - Returns: Detailed podcast information including title, description, cover art, feeds, keywords, and social media links.

6. `get_podcast_episodes_batch_analytics` - Get lightweight analytics for multiple episodes
   - Parameters:
     - `podcast_id` (required): ID of the podcast to analyze.
     - `from_date` (optional, default: 30 days ago): Start date in YYYY-MM-DD format.
     - `to_date` (optional, default: today): End date in YYYY-MM-DD format.
     - `limit` (optional, max: 50): Maximum number of episodes to return.
     - `offset` (optional): Skip the first N episodes for pagination.
   - Returns: A table of episode download statistics, optimized for quick comparison across episodes.

### Tool Selection Guide

- For **overall podcast performance**: Use `get_podcast_analytics_summary` to get aggregate statistics and breakdowns for an entire podcast.
- For **episode comparison**: Use `get_podcast_episodes_batch_analytics` to efficiently compare download numbers across multiple episodes at once.
- For **detailed episode analysis**: Use `get_episode_analytics` to get comprehensive breakdowns (by country, platform, etc.) for a single episode.
- For **podcast management**: Use `list_podcasts` and `list_episodes` to browse and search your content.
- For **podcast metadata**: Use `get_podcast_details` to access comprehensive podcast information and settings.

## Attribution Requirements

This MCP server is offered free to podcasters who host with Podigee on Advanced or Business Pro plans. All analytics reports generated through this MCP Server include a standardized attribution footer:

```
Data Source: Podigee Analytics API | Generated on [Current Date]
```

This attribution footer serves to:
1. Acknowledge the data source (Podigee Analytics API)
2. Provide transparency about when the report was generated

## Example Queries (for Claude Desktop)

Once connected, you can ask Claude questions like:

- "Show me the analytics for my podcast"
- "What are my top performing episodes?"
- "List all my podcasts in Podigee"
- "Show me the analytics for episode ID 123"
- "What are the download trends for episode 456 in the last 7 days?"
- "Compare download numbers for all episodes in my podcast during March 2024"

## Development

### Running tests

```
pytest
```

## License

Podigee proprietary license. Fair usage available for Podigee customers under the Podigee ToS.

## Contributions

Contributions are welcome! Please feel free to submit a Pull Request. 
