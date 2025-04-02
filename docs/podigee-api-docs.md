API Getting Started

Description

The Podigee API allows the automation of publishing processes that would otherwise require manual intervention.

A Word of Caution

Our API provides flexible access to Podigee's data structures and workflows but is not meant to be a listener-facing interface. Please, use the API with care and do not expose it directly to your listeners. Also, do not use it on high-traffic websites without a caching layer. We enforce a rate limit, measured in requests per minute. The rate limit depends directly on the selected plan. If you exceed the rate limit, our API responds with an HTTP 429 status code and some additional information in the headers. In case of doubt, please contact us so that we can discuss further details and give you advice on this matter.

Authentication

Simple API key version

You can find your API key in the account settings if your account allows for it. The key needs to be passed in an HTTP header called "Token" like this:

curl -H "Token: $apiKey" -H "Content-Type: application/json" https://app.podigee.com/api/v1/podcasts
OAuth version

To use OAuth you need to contact Podigee to receive an App/Client ID, secret and redirect info to use. Please note that we do not provide OAuth Apps for every use case and may request additional workflow descriptions first.

In your application you will need to provide a button/link that leads to this URL (replace $my-client-id and $redirect-uri):

https://app.podigee.com/oauth/authorize?client_id=$my-client-id&redirect_uri=$redirect-uri&response_type=code

Depending on the type of application the user will be redirected back to your site or be presented a temporary authorization code to copy and paste into your application. After that, you need to fetch the actual access token using the authorization code:

curl -X POST -d "client_id=$client_id&client_secret=$client_secret&code=$authorization_code&grant_type=authorization_code&redirect_uri=$redirect_uri" https://app.podigee.com/oauth/token
This returns the actual access token, which then can be used for API calls like this:

curl -H "Authorization: Bearer $access_token" -H "Content-Type: application/json" https://app.podigee.com/api/v1/podcasts
API playground

https://app.podigee.com/api-docs provides interactive documentation of the API to try out.

Examples

Fetch all podcasts

# Request
curl -H "Token: mytoken" -H "Content-Type: application/json" https://app.podigee.com/api/v1/podcasts

# Response
[
  {
    "id": 42,
    "category_id": 1,
    "title": "Test",
    "subtitle": null,
    "description": null,
    "quality": "low",
    "language": "en",
    "authors": null,
    "cover_image": null,
    "published_at": null,
    "created_at": "2015-03-20T19:33:14Z",
    "updated_at": "2016-06-05T12:25:25Z",
    "feeds": [
      {
        "format": "mp3",
        "url": "http://podcast31889f.podigee.io/feed/mp3"
      },
      {
        "format": "aac",
        "url": "http://podcast31889f.podigee.io/feed/aac"
      },
      {
        "format": "opus",
        "url": "http://podcast31889f.podigee.io/feed/opus"
      },
      {
        "format": "vorbis",
        "url": "http://podcast31889f.podigee.io/feed/vorbis"
      }
    ],
    "explicit": null,
    "flattr_id": null,
    "twitter": null,
    "facebook": null,
    "copyright_text": null,
    "feed_items": 10
  },
  ...
]
Fetch all episodes of a podcast with ID 42

Please note that this only returns a maximum of 50 episodes. To retrieve more episodes please use the limit and offset parameters as documented here.

# Request
curl -H "Token: mytoken" -H "Content-Type: application/json" https://app.podigee.com/api/v1/episodes?podcast_id=42

# Response

[
  {
    "id": 1,
    "guid": "020a3e890ccd0dd99c3e71d61319814f",
    "podcast_id": 1,
    "production_id": 1,
    "title": "New Episode",
    "subtitle": "\"Bla\" Blupp Hallo",
    "description": null,
    "published_at": "2015-03-23T12:20:00Z",
    "created_at": "2015-03-20T19:34:05Z",
    "updated_at": "2015-03-29T02:12:25Z",
    "chapter_marks": [],
    "media_clips": [],
    "show_notes": null,
    "authors": "Test",
    "explicit": false,
    "cover_image": null
  },
  ...
]
Create a podcast

# Request
curl -H "Token: 123" -H "Content-Type: application/json" -X POST http://www.podigee.dev:4000/api/v1/podcasts -d '{"title": "Test podcast"}'

# Response
{
  "id": 42,
  "category_id": 1,
  "title": "Test",
  "subtitle": null,
  "description": null,
  "quality": "low",
  "language": "en",
  "authors": null,
  "cover_image": null,
  "published_at": null,
  "created_at": "2015-03-20T19:33:14Z",
  "updated_at": "2016-06-05T12:25:25Z",
  "feeds": [
    {
      "format": "mp3",
      "url": "http://podcast31889f.podigee.io/feed/mp3"
    },
    {
      "format": "aac",
      "url": "http://podcast31889f.podigee.io/feed/aac"
    },
    {
      "format": "opus",
      "url": "http://podcast31889f.podigee.io/feed/opus"
    },
    {
      "format": "vorbis",
      "url": "http://podcast31889f.podigee.io/feed/vorbis"
    }
  ],
  "explicit": null,
  "flattr_id": null,
  "twitter": null,
  "facebook": null,
  "copyright_text": null,
  "feed_items": 10
}
Create an episode for a podcast with ID 42

# Request
curl -H "Token: mytoken" -H "Content-Type: application/json" -X POST https://app.podigee.com/api/v1/episodes -d '{"title": "Test episode", "podcast_id": 42}'

# Response
{
  "id": 1,
  "guid": null,
  "podcast_id": 42,
  "production_id": null,
  "title": "Test episode",
  "subtitle": null,
  "description": null,
  "published_at": null,
  "created_at": "2016-06-07T16:58:05Z",
  "updated_at": "2016-06-07T16:58:05Z",
  "chapter_marks": [],
  "media_clips": [],
  "show_notes": null,
  "authors": null,
  "explicit": false,
  "cover_image": null
}
Upload the audio file

Generate an upload URL

# Request
curl -H "Token: mytoken" -H "Content-Type: application/json" -X POST https://app.podigee.com/api/v1/uploads?filename=episode001.flac

# Response

{
  "upload_url": "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u4/test1465315360d448.flac?AWSAccessKeyId=keyId&Expires=1465318879&Signature=sig",
  "content_type": "audio/flac",
  "file_url": "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u4/test1465315360d448.flac"
}
Use upload_url and content_type to upload the file to our media storage

curl "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u4/test1465315360d448.flac?AWSAccessKeyId=keyId&Expires=1465318879&Signature=sig" --upload-file episode001.flac -H "Content-Type: audio/flac"
Create a production

Use the   file_url provided in the step before and the episode's id to create a production.

# Request
curl -H "Token: mytoken" -H "Content-Type: application/json" -X POST https://app.podigee.com/api/v1/productions -d '{"episode_id": 1, "files": [{"url": "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u4/test1465315360d448.flac"}]}'

# Response
{
  "id": 1,
  "episode_id": 1,
  "file_url": "https://podigee.s3-eu-west-1.amazonaws.com/uploads/u4/test1465315360d448.flac",
  "state": "initial",
  "created_at": "2016-06-07T17:04:33Z",
  "updated_at": "2016-06-07T17:04:33Z"
}
Start the production to encode the audio file

curl -H "Token: mytoken" -H "Content-Type: application/json" -X POST https://app.podigee.com/api/v1/productions/1/start
If you want the episode to be published after the encoding is done, you can provide the URL parameter "publish_episode=true".


---

# Podigee Pro API V1 docs

## Podigee Pro API V1 official documentation
Created by Podigee Team (hello@podigee.com)

AdsCollection Show/Hide List Operations Expand Operations
GET /ads/collections
POST /ads/collections
PUT /ads/collections/{ads_collection_id}
AnalyticsReports Show/Hide List Operations Expand Operations
GET /analytics/reports
AnalyticsReportsArchives Show/Hide List Operations Expand Operations
GET /analytics/reports_archives
BatchEncodings Show/Hide List Operations Expand Operations
GET /batch_encodings
POST /batch_encodings
GET /batch_encodings/state
ChapterMarks Show/Hide List Operations Expand Operations
POST /chapter_marks
DELETE /chapter_marks/{chapter_mark_id}
PUT /chapter_marks/{chapter_mark_id}
Contributors Show/Hide List Operations Expand Operations
GET /contributors
POST /contributors
DELETE /contributors/{contributor_id}
GET /contributors/{contributor_id}
PUT /contributors/{contributor_id}
Episodes Show/Hide List Operations Expand Operations
GET /episodes
POST /episodes
DELETE /episodes/{episode_id}
GET /episodes/{episode_id}
PUT /episodes/{episode_id}
Analytics Show/Hide List Operations Expand Operations
GET /episodes/{episode_id}/analytics
GET /podcasts/{podcast_id}/analytics
GET /podcasts/{podcast_id}/analytics/episodes
GET /podcasts/{podcast_id}/overview
GET /podcasts/{podcast_id}/analytics/listeners
GET /podcasts/{podcast_id}/insights/listeners_over_time
GET /podcasts/{podcast_id}/insights/podcasts_categories
ExtraAudios Show/Hide List Operations Expand Operations
GET /extra_audios
POST /extra_audios
DELETE /extra_audios/{extra_audio_id}
GET /extra_audios/{extra_audio_id}
PUT /extra_audios/{extra_audio_id}
POST /extra_audios/{extra_audio_id}/deactivate
Listeners Show/Hide List Operations Expand Operations
GET /listeners
POST /listeners
DELETE /listeners/{listener_id}
GET /listeners/{listener_id}
POST /listeners/{listener_id}/activate
POST /listeners/{listener_id}/deactivate
POST /listeners/{listener_id}/password_reset
POST /listeners/{listener_id}/resend_invitation
POST /listeners/{listener_id}/authorize
Me Show/Hide List Operations Expand Operations
GET /me
PUT /me
MediaClips Show/Hide List Operations Expand Operations
GET /media_clips
POST /media_clips
DELETE /media_clips/{media_clip_id}
GET /media_clips/{media_clip_id}
Podcasts Show/Hide List Operations Expand Operations
GET /podcasts
POST /podcasts
DELETE /podcasts/{podcast_id}
GET /podcasts/{podcast_id}
PUT /podcasts/{podcast_id}
Productions Show/Hide List Operations Expand Operations
POST /productions
POST /productions/{production_id}/start
POST /productions/{production_id}/stop
DELETE /productions/{production_id}
GET /productions/{production_id}
PUT /productions/{production_id}
TextSnippets Show/Hide List Operations Expand Operations
GET /text_snippets
POST /text_snippets
DELETE /text_snippets/{text_snippet_id}
GET /text_snippets/{text_snippet_id}
PUT /text_snippets/{text_snippet_id}
TranscriptionImports Show/Hide List Operations Expand Operations
POST /transcription_imports
Uploads Show/Hide List Operations Expand Operations
POST /uploads
POST /uploads/part_url
POST /uploads/complete_multipart_url


swagger  
Authorize
 
Explore
Podigee Pro API V1 docs
Podigee Pro API V1 official documentation
Created by Podigee Team (hello@podigee.com)
AdsCollection Show/Hide List Operations Expand Operations
GET /ads/collections
Response Class (Status 200)
ads collections response
ModelExample Value
[
  {
    "id": 0,
    "collection_id": "string",
    "created_at": "2025-03-29T13:54:35.414Z",
    "updated_at": "2025-03-29T13:54:35.414Z",
    "state": "generated",
    "podcast_name": "string"
  }
]

Response Content Type 
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /ads/collections
Response Class (Status 200)
ads collection created
ModelExample Value
{
  "id": 0,
  "collection_id": "string",
  "created_at": "2025-03-29T13:54:35.416Z",
  "updated_at": "2025-03-29T13:54:35.416Z",
  "state": "generated",
  "podcast_name": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
ads_collection	

Parameter content type: 
New ads collection to create
body	
ModelExample Value
{}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
ads collection not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
ads collection could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /ads/collections/{ads_collection_id}
Response Class (Status 200)
ads collection updated
ModelExample Value
{
  "id": 0,
  "collection_id": "string",
  "created_at": "2025-03-29T13:54:35.417Z",
  "updated_at": "2025-03-29T13:54:35.417Z",
  "state": "generated",
  "podcast_name": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
ads_collection_id		
Ads Collection id
path	long
ads_collection	

Parameter content type: 
Ads Collection to update
body	
ModelExample Value
{
  "state": "generated"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
ads collection not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
ads collection could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

AnalyticsReports Show/Hide List Operations Expand Operations
GET /analytics/reports
Response Class (Status 200)
reports response
ModelExample Value
[
  {
    "id": 0,
    "podcast_id": 0,
    "file_urls": [
      null
    ],
    "start_date": "2025-03-29T13:54:35.419Z",
    "end_date": "2025-03-29T13:54:35.419Z"
  }
]

Response Content Type 
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

AnalyticsReportsArchives Show/Hide List Operations Expand Operations
GET /analytics/reports_archives
Response Class (Status 200)
archives response
ModelExample Value
[
  {
    "id": 0,
    "user_id": 0,
    "file_url": "string",
    "start_date": "2025-03-29T13:54:35.420Z",
    "end_date": "2025-03-29T13:54:35.420Z"
  }
]

Response Content Type 
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

BatchEncodings Show/Hide List Operations Expand Operations
GET /batch_encodings
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Podcast to fetch progress from
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
progress response
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /batch_encodings
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Podcast to encode
query	long
initiator		
Allows to set initiator for batch encoding
query	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
encoding started
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /batch_encodings/state
Response Class (Status 200)
information response
ModelExample Value
{
  "state": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Podcast to fetch information from
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

ChapterMarks Show/Hide List Operations Expand Operations
POST /chapter_marks
Response Class (Status 200)
chapter mark created
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "title": "string",
  "start_time": "string",
  "url": "string",
  "created_at": "2025-03-29T13:54:35.422Z",
  "updated_at": "2025-03-29T13:54:35.422Z",
  "image": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
chapter_mark	

Parameter content type: 
New chapter mark to create
body	
ModelExample Value
{
  "episode_id": 0,
  "title": "string",
  "start_time": "string",
  "url": "string",
  "image": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
chapter mark could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /chapter_marks/{chapter_mark_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
chapter_mark_id		
ChapterMark id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
chapter_mark destroyed
404	
chapter_mark not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
chapter_mark could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /chapter_marks/{chapter_mark_id}
Response Class (Status 200)
chapter_mark updated
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "title": "string",
  "start_time": "string",
  "url": "string",
  "created_at": "2025-03-29T13:54:35.424Z",
  "updated_at": "2025-03-29T13:54:35.424Z",
  "image": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
chapter_mark_id		
ChapterMark id
path	long
chapter_mark	

Parameter content type: 
ChapterMark to update
body	
ModelExample Value
{
  "title": "string",
  "start_time": "string",
  "url": "string",
  "image": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
chapter_mark not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
chapter_mark could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Contributors Show/Hide List Operations Expand Operations
GET /contributors
Response Class (Status 200)
contributor list response
ModelExample Value
[
  {
    "id": 0,
    "podcast_id": 0,
    "user_id": 0,
    "name": "string",
    "email": "string",
    "biography": "string",
    "avatar_url": "string",
    "links": [
      {
        "icon": "string",
        "url": "string",
        "text": "string"
      }
    ],
    "created_at": "2025-03-29T13:54:35.426Z",
    "updated_at": "2025-03-29T13:54:35.426Z"
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
ID of podcast to filter
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /contributors
Response Class (Status 200)
contributor created
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "user_id": 0,
  "name": "string",
  "email": "string",
  "biography": "string",
  "avatar_url": "string",
  "links": [
    {
      "icon": "string",
      "url": "string",
      "text": "string"
    }
  ],
  "created_at": "2025-03-29T13:54:35.426Z",
  "updated_at": "2025-03-29T13:54:35.426Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
contributor	

Parameter content type: 
New contributor to create
body	
ModelExample Value
{
  "podcast_id": 0,
  "name": "string",
  "email": "string",
  "biography": "string",
  "avatar_url": "string",
  "links": [
    {
      "icon": "string",
      "url": "string",
      "text": "string"
    }
  ]
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
contributor could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /contributors/{contributor_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
contributor_id		
Contributor id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
contributor destroyed
404	
contributor not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
contributor could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /contributors/{contributor_id}
Response Class (Status 200)
contributor response
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "user_id": 0,
  "name": "string",
  "email": "string",
  "biography": "string",
  "avatar_url": "string",
  "links": [
    {
      "icon": "string",
      "url": "string",
      "text": "string"
    }
  ],
  "created_at": "2025-03-29T13:54:35.428Z",
  "updated_at": "2025-03-29T13:54:35.428Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
contributor_id		
ID of contributor to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
contributor not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /contributors/{contributor_id}
Response Class (Status 200)
contributor updated
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "user_id": 0,
  "name": "string",
  "email": "string",
  "biography": "string",
  "avatar_url": "string",
  "links": [
    {
      "icon": "string",
      "url": "string",
      "text": "string"
    }
  ],
  "created_at": "2025-03-29T13:54:35.429Z",
  "updated_at": "2025-03-29T13:54:35.429Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
contributor_id		
Contributor id
path	long
contributor	

Parameter content type: 
Contributor to update
body	
ModelExample Value
{
  "name": "string",
  "email": "string",
  "biography": "string",
  "avatar_url": "string",
  "links": [
    {
      "icon": "string",
      "url": "string",
      "text": "string"
    }
  ]
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
contributor not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
contributor could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Episodes Show/Hide List Operations Expand Operations
GET /episodes
Response Class (Status 200)
episode list response
ModelExample Value
[
  {
    "id": 0,
    "guid": "string",
    "podcast_id": 0,
    "production_id": 0,
    "title": "string",
    "subtitle": "string",
    "description": "string",
    "slug": "string",
    "external_url": "string",
    "number": 0,
    "season": 0,
    "permalink": "string",
    "published_at": "2025-03-29T13:54:35.430Z",
    "created_at": "2025-03-29T13:54:35.430Z",
    "updated_at": "2025-03-29T13:54:35.430Z",
    "keywords": [
      null
    ],
    "labels": [
      null
    ],
    "chapter_marks": [
      {
        "id": 0,
        "title": "string",
        "start_time": "string",
        "url": "string",
        "created_at": "2025-03-29T13:54:35.430Z",
        "updated_at": "2025-03-29T13:54:35.430Z",
        "image": "string"
      }
    ],
    "show_notes": "string",
    "show_notes_md": "string",
    "authors": "string",
    "explicit": true,
    "cover_image": "string",
    "facebook_image": "string",
    "transcription": [
      {
        "text": "string",
        "speaker_id": 0
      }
    ],
    "transcription_url": "string",
    "automatic_transcription": true,
    "contributor_ids": [
      null
    ],
    "publication_type": "full",
    "bypass_ad_insertion": true,
    "duration": 0,
    "duration_ms": 0,
    "dropbox_source": true,
    "ad_provider": "string",
    "podcast_ad_provider": "string",
    "intro_outro_include": true
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
ID of podcast to filter
query	long
podcast_ids[]		
array of IDs of podcasts to get episodes from
query	Array[double]
limit_per_podcast		
How many episodes should be returned per podcast. Max: 10Available only when podcast_ids are specified
query	long
limit		
How many episodes should be returned. Max: 50
query	long
offset		
Skip the given amount of episodes in the query (can be used for pagination)
query	long
published		
Return published episodes only
query	boolean
publication_type		
Publication type (all, full, trial, or bonus). Default: null (= all)
query	string
sort_by		
Sort by given field. Default: newest episodes first, (if unpublished, latest updated first)
query	string
sort_direction		
Sorting direction (asc, desc). Default: asc
query	string
search		
Full-text search. Currently searches in title only
query	string
fields_filter[]		
array of fields to get
query	Array[string]
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast_id could not be found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /episodes
Response Class (Status 200)
episode created
ModelExample Value
{
  "id": 0,
  "guid": "string",
  "podcast_id": 0,
  "production_id": 0,
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "slug": "string",
  "external_url": "string",
  "number": 0,
  "season": 0,
  "permalink": "string",
  "published_at": "2025-03-29T13:54:35.432Z",
  "created_at": "2025-03-29T13:54:35.432Z",
  "updated_at": "2025-03-29T13:54:35.432Z",
  "keywords": [
    null
  ],
  "labels": [
    null
  ],
  "chapter_marks": [
    {
      "id": 0,
      "title": "string",
      "start_time": "string",
      "url": "string",
      "created_at": "2025-03-29T13:54:35.432Z",
      "updated_at": "2025-03-29T13:54:35.432Z",
      "image": "string"
    }
  ],
  "show_notes": "string",
  "show_notes_md": "string",
  "authors": "string",
  "explicit": true,
  "cover_image": "string",
  "facebook_image": "string",
  "transcription": [
    {
      "text": "string",
      "speaker_id": 0
    }
  ],
  "transcription_url": "string",
  "automatic_transcription": true,
  "contributor_ids": [
    null
  ],
  "publication_type": "full",
  "bypass_ad_insertion": true,
  "duration": 0,
  "duration_ms": 0,
  "dropbox_source": true,
  "ad_provider": "string",
  "podcast_ad_provider": "string",
  "intro_outro_include": true
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode	

Parameter content type: 
New episode to create
body	
ModelExample Value
{
  "guid": "string",
  "podcast_id": 0,
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "slug": "string",
  "external_url": "string",
  "number": 0,
  "season": 0,
  "keywords": [
    null
  ],
  "labels": [
    null
  ],
  "chapter_marks": [
    {
      "id": 0,
      "title": "string",
      "start_time": "string",
      "url": "string",
      "created_at": "2025-03-29T13:54:35.433Z",
      "updated_at": "2025-03-29T13:54:35.433Z",
      "image": "string"
    }
  ],
  "show_notes": "string",
  "show_notes_md": "string",
  "authors": "string",
  "explicit": true,
  "cover_image": "string",
  "facebook_image": "string",
  "transcription": [
    {
      "text": "string",
      "speaker_id": 0
    }
  ],
  "contributor_ids": [
    null
  ],
  "publication_type": "full",
  "bypass_ad_insertion": true,
  "ad_provider": "string",
  "intro_outro_include": true
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
episode could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /episodes/{episode_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode_id		
Episode id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
episode destroyed
404	
episode not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
episode could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /episodes/{episode_id}
Response Class (Status 200)
episode response
ModelExample Value
{
  "id": 0,
  "guid": "string",
  "podcast_id": 0,
  "production_id": 0,
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "slug": "string",
  "external_url": "string",
  "number": 0,
  "season": 0,
  "permalink": "string",
  "published_at": "2025-03-29T13:54:35.435Z",
  "created_at": "2025-03-29T13:54:35.435Z",
  "updated_at": "2025-03-29T13:54:35.435Z",
  "keywords": [
    null
  ],
  "labels": [
    null
  ],
  "chapter_marks": [
    {
      "id": 0,
      "title": "string",
      "start_time": "string",
      "url": "string",
      "created_at": "2025-03-29T13:54:35.435Z",
      "updated_at": "2025-03-29T13:54:35.435Z",
      "image": "string"
    }
  ],
  "show_notes": "string",
  "show_notes_md": "string",
  "authors": "string",
  "explicit": true,
  "cover_image": "string",
  "facebook_image": "string",
  "transcription": [
    {
      "text": "string",
      "speaker_id": 0
    }
  ],
  "transcription_url": "string",
  "automatic_transcription": true,
  "contributor_ids": [
    null
  ],
  "publication_type": "full",
  "bypass_ad_insertion": true,
  "duration": 0,
  "duration_ms": 0,
  "dropbox_source": true,
  "ad_provider": "string",
  "podcast_ad_provider": "string",
  "intro_outro_include": true
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode_id		
ID of episode to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
episode not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /episodes/{episode_id}
Response Class (Status 200)
episode updated
ModelExample Value
{
  "id": 0,
  "guid": "string",
  "podcast_id": 0,
  "production_id": 0,
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "slug": "string",
  "external_url": "string",
  "number": 0,
  "season": 0,
  "permalink": "string",
  "published_at": "2025-03-29T13:54:35.436Z",
  "created_at": "2025-03-29T13:54:35.436Z",
  "updated_at": "2025-03-29T13:54:35.436Z",
  "keywords": [
    null
  ],
  "labels": [
    null
  ],
  "chapter_marks": [
    {
      "id": 0,
      "title": "string",
      "start_time": "string",
      "url": "string",
      "created_at": "2025-03-29T13:54:35.436Z",
      "updated_at": "2025-03-29T13:54:35.436Z",
      "image": "string"
    }
  ],
  "show_notes": "string",
  "show_notes_md": "string",
  "authors": "string",
  "explicit": true,
  "cover_image": "string",
  "facebook_image": "string",
  "transcription": [
    {
      "text": "string",
      "speaker_id": 0
    }
  ],
  "transcription_url": "string",
  "automatic_transcription": true,
  "contributor_ids": [
    null
  ],
  "publication_type": "full",
  "bypass_ad_insertion": true,
  "duration": 0,
  "duration_ms": 0,
  "dropbox_source": true,
  "ad_provider": "string",
  "podcast_ad_provider": "string",
  "intro_outro_include": true
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode_id		
Episode id
path	long
episode	

Parameter content type: 
Episode to update
body	
ModelExample Value
{
  "guid": "string",
  "podcast_id": 0,
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "slug": "string",
  "external_url": "string",
  "number": 0,
  "season": 0,
  "published_at": "2025-03-29T13:54:35.437Z",
  "keywords": [
    null
  ],
  "labels": [
    null
  ],
  "chapter_marks": [
    {
      "id": 0,
      "title": "string",
      "start_time": "string",
      "url": "string",
      "created_at": "2025-03-29T13:54:35.437Z",
      "updated_at": "2025-03-29T13:54:35.437Z",
      "image": "string"
    }
  ],
  "show_notes": "string",
  "show_notes_md": "string",
  "authors": "string",
  "explicit": true,
  "cover_image": "string",
  "facebook_image": "string",
  "transcription": [
    {
      "text": "string",
      "speaker_id": 0
    }
  ],
  "contributor_ids": [
    null
  ],
  "publication_type": "full",
  "bypass_ad_insertion": true,
  "ad_provider": "string",
  "intro_outro_include": true
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
episode not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
episode could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Analytics Show/Hide List Operations Expand Operations
GET /episodes/{episode_id}/analytics
Response Class (Status 200)
analytics response
ModelExample Value
{
  "meta": {
    "timerange": {
      "start_datetime": "string",
      "end_datetime": "string"
    },
    "aggregation_granularity": "hour"
  },
  "objects": [
    {
      "downloaded_on": "2025-03-29T13:54:35.438Z",
      "downloads": {
        "complete": 0
      },
      "formats": {},
      "platforms": {},
      "countries": {},
      "clients": {},
      "clients_on_platforms": {},
      "sources": {}
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode_id		
Id of an episode to fetch.
path	long
from		
Beginning of the analytics date interval. Need to be used together with "to" parameter.
query	date
to		
End of the analytics date interval. Need to be used together with "from" parameter.
query	date
days_since_published		
Can be used instead "from/to" parameters. It calculates analytics in time interval from published date to a number of days specified in the param.
query	long
granularity		
Determines a granularity of data. If not given, will be calculated based on time interval.
query	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/analytics
Response Class (Status 200)
analytics response
ModelExample Value
{
  "meta": {
    "timerange": {
      "start_datetime": "string",
      "end_datetime": "string"
    },
    "aggregation_granularity": "hour"
  },
  "objects": [
    {
      "downloaded_on": "2025-03-29T13:54:35.443Z",
      "downloads": {
        "complete": 0
      },
      "formats": {},
      "platforms": {},
      "countries": {},
      "clients": {},
      "clients_on_platforms": {},
      "sources": {}
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
from		
Beginning of the analytics date interval. Need to be used together with "to" parameter.
query	date
to		
End of the analytics date interval. Need to be used together with "from" parameter.
query	date
days_offset		
Can be used instead "from/to" parameters. It calculates analytics from last number of days specified in the param.
query	long
granularity		
Determines a granularity of data. If not given, will be calculated based on time interval.
query	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/analytics/episodes
Response Class (Status 200)
analytics response
ModelExample Value
{
  "objects": [
    {
      "id": 0,
      "downloads": 0,
      "analytics_episodes_cover_image": "string",
      "title": "string",
      "slug": "string",
      "number": 0,
      "published_at": "2025-03-29T13:54:35.444Z"
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of a podcast to fetch
path	long
from		
Beginning of the analytics date interval. Need to be used together with "to" parameter.
query	date
to		
End of the analytics date interval. Need to be used together with "from" parameter.
query	date
limit		
How many episodes should be returned.
query	long
offset		
Skip the given amount of episodes (can be used for pagination)
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/overview
Response Class (Status 200)
analytics response
ModelExample Value
{
  "meta": {
    "from": "2025-03-29T13:54:35.445Z",
    "to": "2025-03-29T13:54:35.445Z"
  },
  "published_episodes_count": 0,
  "audio_published_minutes": 0,
  "unique_listeners_number": 0,
  "unique_subscribers_number": 0,
  "mean_audio_published_minutes": 0,
  "mean_episode_download": 0,
  "total_downloads": 0,
  "top_episodes": [
    {
      "id": 0,
      "downloads": 0,
      "analytics_episodes_cover_image": "string",
      "title": "string",
      "slug": "string",
      "number": 0,
      "published_at": "2025-03-29T13:54:35.445Z"
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
from		
Beginning of the analytics date interval. Need to be used together with "to" parameter.
query	date
to		
End of the analytics date interval. Need to be used together with "from" parameter.
query	date
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/analytics/listeners
Response Class (Status 200)
listeners response
ModelExample Value
{
  "objects": [
    {
      "podcast_id": 0,
      "downloaded_on": "2025-03-29T13:54:35.446Z",
      "listeners": 0,
      "subscribers": 0
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
from		
Beginning of the listeners date interval. Default is beginning of the current month.
query	date
to		
End of the listeners date interval. Default is end of the current month.
query	date
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/insights/listeners_over_time
Response Class (Status 200)
listener over time insights response
ModelExample Value
{
  "over_time": {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0
  }
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}/insights/podcasts_categories
Response Class (Status 200)
podcasts and categories insights response
ModelExample Value
{
  "by_podcast": [
    {
      "pct": 0,
      "count": 0,
      "title": "string"
    }
  ],
  "by_category": [
    {
      "pct": 0,
      "count": 0,
      "name": "string"
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

ExtraAudios Show/Hide List Operations Expand Operations
GET /extra_audios
Response Class (Status 200)
extra audios list
ModelExample Value
[
  {
    "id": 0,
    "title": "string",
    "podcast_id": 0,
    "user_id": 0,
    "url": "string",
    "position": 0,
    "planned_ad_id": 0,
    "deactivated_at": "2025-03-29T13:54:35.448Z"
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
ID of podcast
query	long
used_as_ad		
If set to true request will return records thathave been used as ads
query	boolean
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /extra_audios
Implementation Notes
omit podcast_id parameter to create extra audio under user
Response Class (Status 200)
Extra audio created
ModelExample Value
{
  "id": 0,
  "title": "string",
  "podcast_id": 0,
  "user_id": 0,
  "url": "string",
  "position": 0,
  "planned_ad_id": 0,
  "deactivated_at": "2025-03-29T13:54:35.449Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
extra_audio	

Parameter content type: 
New extra audio to create
body	
ModelExample Value
{
  "title": "string",
  "podcast_id": 0,
  "url": "string",
  "position": 0,
  "planned_ad_id": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast or user not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
extra audio could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /extra_audios/{extra_audio_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
extra_audio_id		
Extra audio id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Extra audio destroyed
404	
Extra audio not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
Extra audio could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /extra_audios/{extra_audio_id}
Response Class (Status 200)
extra audio response
ModelExample Value
{
  "id": 0,
  "title": "string",
  "podcast_id": 0,
  "user_id": 0,
  "url": "string",
  "position": 0,
  "planned_ad_id": 0,
  "deactivated_at": "2025-03-29T13:54:35.450Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
extra_audio_id		
ID of extra audio to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
extra audio not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /extra_audios/{extra_audio_id}
Response Class (Status 200)
extra audio updated
ModelExample Value
{
  "id": 0,
  "title": "string",
  "podcast_id": 0,
  "user_id": 0,
  "url": "string",
  "position": 0,
  "planned_ad_id": 0,
  "deactivated_at": "2025-03-29T13:54:35.451Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
extra_audio_id		
Extra audio id
path	long
extra_audio	

Parameter content type: 
Extra audio to update
body	
ModelExample Value
{
  "title": "string",
  "url": "string",
  "position": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
Extra audio not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
Extra audio could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /extra_audios/{extra_audio_id}/deactivate
Parameters
Parameter	Value	Description	Parameter Type	Data Type
extra_audio_id		
Extra audio id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Extra audio deactivated
404	
Extra audio not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
Extra audio could not be deactivated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Listeners Show/Hide List Operations Expand Operations
GET /listeners
Response Class (Status 200)
listeners of a podcast response
ModelExample Value
[
  {
    "id": 0,
    "podcast_id": 0,
    "username": "string",
    "email": "string",
    "status": "string",
    "token": "string",
    "password": "string",
    "created_at": "2025-03-29T13:54:35.452Z",
    "updated_at": "2025-03-29T13:54:35.452Z"
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
ID of podcast
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast_id could not be found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners
Response Class (Status 200)
listener created
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.453Z",
  "updated_at": "2025-03-29T13:54:35.453Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener	

Parameter content type: 
New listener to create
body	
ModelExample Value
{
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "password": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
listener could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /listeners/{listener_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Listener id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
listener destroyed
404	
listener not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
listener could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /listeners/{listener_id}
Response Class (Status 200)
listener response
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.454Z",
  "updated_at": "2025-03-29T13:54:35.454Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Id of listener to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
listener not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners/{listener_id}/activate
Response Class (Status 200)
listener activated
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.454Z",
  "updated_at": "2025-03-29T13:54:35.454Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Listener id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
listener could not be activated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners/{listener_id}/deactivate
Response Class (Status 200)
listener deactivated
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.455Z",
  "updated_at": "2025-03-29T13:54:35.455Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Listener id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
listener could not be deactivated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners/{listener_id}/password_reset
Response Class (Status 200)
reset password email sent to listener
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.455Z",
  "updated_at": "2025-03-29T13:54:35.455Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Listener id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
listener not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
reset password email could not be sent
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners/{listener_id}/resend_invitation
Response Class (Status 200)
listener's invitation sent
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.456Z",
  "updated_at": "2025-03-29T13:54:35.456Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Listener id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
listener not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
invitation could not be sent
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /listeners/{listener_id}/authorize
Response Class (Status 200)
listener authorized
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "status": "string",
  "token": "string",
  "password": "string",
  "created_at": "2025-03-29T13:54:35.456Z",
  "updated_at": "2025-03-29T13:54:35.456Z"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
listener_id		
Id of a listener to authorize.
path	long
listener	

Parameter content type: 
Listener auth data
body	
ModelExample Value
{
  "podcast_id": 0,
  "username": "string",
  "email": "string",
  "password": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
401	
listener could not be authorized
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Me Show/Hide List Operations Expand Operations
GET /me
Response Class (Status 200)
User response
ModelExample Value
{
  "id": 0,
  "email": "string",
  "subscribed_to_reports": true,
  "locale": "string",
  "country": "string",
  "plan": {
    "id": 0,
    "code": "string",
    "kind": "string",
    "kind_name": "string",
    "name": "string",
    "currency": "string",
    "price": 0,
    "frequency": "string",
    "formatted_price": "string",
    "monthly_price": 0,
    "formatted_monthly_price": "string",
    "formatted_impressions_price": "string",
    "tax_excluded": true,
    "discounted_price": 0,
    "discounted_monthly_price": 0,
    "discounted_formatted_price": "string",
    "discounted_formatted_monthly_price": "string",
    "discount_duration_type": "string",
    "discount_period": 0,
    "discount_period_unit": "string",
    "accepted_discounted_price": 0,
    "accepted_discounted_monthly_price": 0,
    "accepted_discounted_formatted_price": "string",
    "accepted_discounted_formatted_monthly_price": "string",
    "accepted_discount_duration_type": "string",
    "accepted_discount_period": 0,
    "accepted_discount_period_unit": "string",
    "accepted_discount_title": "string"
  },
  "packages": [
    null
  ],
  "impression_balance": 0,
  "impression_alert_threshold": 0,
  "impression_cpm_info": {},
  "ad_planner_email_notifications_enabled": true,
  "trial_expired": true,
  "discount_available": true
}

Response Content Type 
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /me
Response Class (Status 200)
User updated
ModelExample Value
{
  "subscribed_to_reports": true,
  "locale": "string",
  "impression_alert_threshold": 0,
  "ad_planner_email_notifications_enabled": true
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
user	

Parameter content type: 
User updates?
body	
ModelExample Value
{
  "subscribed_to_reports": true,
  "locale": "string",
  "impression_alert_threshold": 0,
  "ad_planner_email_notifications_enabled": true
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
User could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

MediaClips Show/Hide List Operations Expand Operations
GET /media_clips
Response Class (Status 200)
media_clip list response
ModelExample Value
[
  {
    "id": 0,
    "episode_id": 0,
    "file_format": "mp3",
    "url": "string",
    "created_at": "2025-03-29T13:54:35.458Z",
    "size": 0,
    "duration": 0
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
episode_id		
ID of episode to filter
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
episode_id could not be found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /media_clips
Response Class (Status 200)
media_clip created
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "file_format": "mp3",
  "url": "string",
  "created_at": "2025-03-29T13:54:35.459Z",
  "size": 0,
  "duration": 0
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
media_clip	

Parameter content type: 
New media_clip to create
body	
ModelExample Value
{
  "episode_id": 0,
  "file_format": "mp3",
  "url": "string",
  "size": 0,
  "duration": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
episode not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
media_clip could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /media_clips/{media_clip_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
media_clip_id		
MediaClip id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
media_clip destroyed
404	
media_clip not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
media_clip could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /media_clips/{media_clip_id}
Response Class (Status 200)
media_clip response
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "file_format": "mp3",
  "url": "string",
  "created_at": "2025-03-29T13:54:35.460Z",
  "size": 0,
  "duration": 0
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
media_clip_id		
ID of media_clip to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
media_clip not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Podcasts Show/Hide List Operations Expand Operations
GET /podcasts
Response Class (Status 200)
podcast response
ModelExample Value
[
  {
    "id": 0,
    "subdomain": "string",
    "episodes_count": 0,
    "slug": "string",
    "category_id": 0,
    "category_ids": [
      null
    ],
    "title": "string",
    "subtitle": "string",
    "description": "string",
    "custom_alias": "string",
    "quality": "low",
    "language": "string",
    "last_episode_publication_date": "2025-03-29T13:54:35.461Z",
    "authors": "string",
    "cover_image": "string",
    "analytics_cover_image": "string",
    "website_url": "string",
    "user_id": 0,
    "owner_email": "string",
    "user_email": "string",
    "published_at": "2025-03-29T13:54:35.461Z",
    "created_at": "2025-03-29T13:54:35.461Z",
    "updated_at": "2025-03-29T13:54:35.461Z",
    "keywords": [
      null
    ],
    "feeds": [
      {
        "format": "mp3",
        "url": "string"
      }
    ],
    "preview_token": {
      "token": "string",
      "valid_until": "2025-03-29T13:54:35.461Z"
    },
    "publication_type": "episodic",
    "explicit": true,
    "external": true,
    "flattr_id": "string",
    "twitter": "string",
    "facebook": "string",
    "itunes_id": "string",
    "spotify_url": "string",
    "spotify_connection": {},
    "deezer_url": "string",
    "alexa_url": "string",
    "copyright_text": "string",
    "feed_items": 0,
    "transcriptions_enabled": true,
    "create_stats_reports": true,
    "external_site_url": "string",
    "domain": "string",
    "analytics_package": "string",
    "analytics_csv_export": true,
    "protected": true,
    "ad_provider": "string",
    "see_podcast_analytics": true,
    "podcast_namespace_guid": "string"
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
fields_filter[]		
array of fields to get
query	Array[string]
collaborator		
get podcasts that user is collaborator of
query	boolean
partner		
get podcasts that user is partner of
query	boolean
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /podcasts
Response Class (Status 200)
podcast created
ModelExample Value
{
  "id": 0,
  "subdomain": "string",
  "episodes_count": 0,
  "slug": "string",
  "category_id": 0,
  "category_ids": [
    null
  ],
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "custom_alias": "string",
  "quality": "low",
  "language": "string",
  "last_episode_publication_date": "2025-03-29T13:54:35.462Z",
  "authors": "string",
  "cover_image": "string",
  "analytics_cover_image": "string",
  "website_url": "string",
  "user_id": 0,
  "owner_email": "string",
  "user_email": "string",
  "published_at": "2025-03-29T13:54:35.462Z",
  "created_at": "2025-03-29T13:54:35.462Z",
  "updated_at": "2025-03-29T13:54:35.462Z",
  "keywords": [
    null
  ],
  "feeds": [
    {
      "format": "mp3",
      "url": "string"
    }
  ],
  "preview_token": {
    "token": "string",
    "valid_until": "2025-03-29T13:54:35.462Z"
  },
  "publication_type": "episodic",
  "explicit": true,
  "external": true,
  "flattr_id": "string",
  "twitter": "string",
  "facebook": "string",
  "itunes_id": "string",
  "spotify_url": "string",
  "spotify_connection": {},
  "deezer_url": "string",
  "alexa_url": "string",
  "copyright_text": "string",
  "feed_items": 0,
  "transcriptions_enabled": true,
  "create_stats_reports": true,
  "external_site_url": "string",
  "domain": "string",
  "analytics_package": "string",
  "analytics_csv_export": true,
  "protected": true,
  "ad_provider": "string",
  "see_podcast_analytics": true,
  "podcast_namespace_guid": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast	

Parameter content type: 
New podcast to create
body	
ModelExample Value
{
  "subdomain": "string",
  "category_id": 0,
  "category_ids": [
    null
  ],
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "quality": "low",
  "language": "string",
  "authors": "string",
  "cover_image": "string",
  "website_url": "string",
  "owner_email": "string",
  "keywords": [
    null
  ],
  "publication_type": "episodic",
  "explicit": true,
  "external": true,
  "flattr_id": "string",
  "twitter": "string",
  "facebook": "string",
  "copyright_text": "string",
  "feed_items": 0,
  "transcriptions_enabled": true,
  "create_stats_reports": true,
  "external_site_url": "string",
  "domain": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
podcast could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /podcasts/{podcast_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Podcast id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
podcast destroyed
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
podcast could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /podcasts/{podcast_id}
Response Class (Status 200)
podcast response
ModelExample Value
{
  "id": 0,
  "subdomain": "string",
  "episodes_count": 0,
  "slug": "string",
  "category_id": 0,
  "category_ids": [
    null
  ],
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "custom_alias": "string",
  "quality": "low",
  "language": "string",
  "last_episode_publication_date": "2025-03-29T13:54:35.464Z",
  "authors": "string",
  "cover_image": "string",
  "analytics_cover_image": "string",
  "website_url": "string",
  "user_id": 0,
  "owner_email": "string",
  "user_email": "string",
  "published_at": "2025-03-29T13:54:35.464Z",
  "created_at": "2025-03-29T13:54:35.464Z",
  "updated_at": "2025-03-29T13:54:35.464Z",
  "keywords": [
    null
  ],
  "feeds": [
    {
      "format": "mp3",
      "url": "string"
    }
  ],
  "preview_token": {
    "token": "string",
    "valid_until": "2025-03-29T13:54:35.464Z"
  },
  "publication_type": "episodic",
  "explicit": true,
  "external": true,
  "flattr_id": "string",
  "twitter": "string",
  "facebook": "string",
  "itunes_id": "string",
  "spotify_url": "string",
  "spotify_connection": {},
  "deezer_url": "string",
  "alexa_url": "string",
  "copyright_text": "string",
  "feed_items": 0,
  "transcriptions_enabled": true,
  "create_stats_reports": true,
  "external_site_url": "string",
  "domain": "string",
  "analytics_package": "string",
  "analytics_csv_export": true,
  "protected": true,
  "ad_provider": "string",
  "see_podcast_analytics": true,
  "podcast_namespace_guid": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Id of podcast to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /podcasts/{podcast_id}
Response Class (Status 200)
podcast updated
ModelExample Value
{
  "id": 0,
  "subdomain": "string",
  "episodes_count": 0,
  "slug": "string",
  "category_id": 0,
  "category_ids": [
    null
  ],
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "custom_alias": "string",
  "quality": "low",
  "language": "string",
  "last_episode_publication_date": "2025-03-29T13:54:35.465Z",
  "authors": "string",
  "cover_image": "string",
  "analytics_cover_image": "string",
  "website_url": "string",
  "user_id": 0,
  "owner_email": "string",
  "user_email": "string",
  "published_at": "2025-03-29T13:54:35.465Z",
  "created_at": "2025-03-29T13:54:35.465Z",
  "updated_at": "2025-03-29T13:54:35.465Z",
  "keywords": [
    null
  ],
  "feeds": [
    {
      "format": "mp3",
      "url": "string"
    }
  ],
  "preview_token": {
    "token": "string",
    "valid_until": "2025-03-29T13:54:35.465Z"
  },
  "publication_type": "episodic",
  "explicit": true,
  "external": true,
  "flattr_id": "string",
  "twitter": "string",
  "facebook": "string",
  "itunes_id": "string",
  "spotify_url": "string",
  "spotify_connection": {},
  "deezer_url": "string",
  "alexa_url": "string",
  "copyright_text": "string",
  "feed_items": 0,
  "transcriptions_enabled": true,
  "create_stats_reports": true,
  "external_site_url": "string",
  "domain": "string",
  "analytics_package": "string",
  "analytics_csv_export": true,
  "protected": true,
  "ad_provider": "string",
  "see_podcast_analytics": true,
  "podcast_namespace_guid": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
Podcast id
path	long
podcast	

Parameter content type: 
Podcast to update
body	
ModelExample Value
{
  "subdomain": "string",
  "category_id": 0,
  "category_ids": [
    null
  ],
  "title": "string",
  "subtitle": "string",
  "description": "string",
  "quality": "low",
  "language": "string",
  "authors": "string",
  "cover_image": "string",
  "website_url": "string",
  "owner_email": "string",
  "published_at": "2025-03-29T13:54:35.466Z",
  "keywords": [
    null
  ],
  "publication_type": "episodic",
  "explicit": true,
  "flattr_id": "string",
  "twitter": "string",
  "facebook": "string",
  "copyright_text": "string",
  "feed_items": 0,
  "transcriptions_enabled": true,
  "create_stats_reports": true,
  "external_site_url": "string",
  "domain": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
podcast could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Productions Show/Hide List Operations Expand Operations
POST /productions
Response Class (Status 200)
production created
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "files": [
    {
      "url": "string",
      "contributor_id": 0,
      "custom_name": "string",
      "type": "multitrack",
      "original_filename": "string"
    }
  ],
  "state": "initial",
  "publication_flag": true,
  "created_at": "2025-03-29T13:54:35.467Z",
  "updated_at": "2025-03-29T13:54:35.467Z",
  "audio_duration_ms": 0,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production	

Parameter content type: 
New production to create
body	
ModelExample Value
{
  "episode_id": 0,
  "files": [
    {
      "url": "string",
      "contributor_id": 0,
      "custom_name": "string",
      "type": "multitrack",
      "original_filename": "string"
    }
  ],
  "state": "initial",
  "publication_flag": true,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
episode not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
production could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /productions/{production_id}/start
Response Class (Status 200)
production encoding started
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "files": [
    {
      "url": "string",
      "contributor_id": 0,
      "custom_name": "string",
      "type": "multitrack",
      "original_filename": "string"
    }
  ],
  "state": "initial",
  "publication_flag": true,
  "created_at": "2025-03-29T13:54:35.468Z",
  "updated_at": "2025-03-29T13:54:35.468Z",
  "audio_duration_ms": 0,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production_id		
ID of production to encode
path	long
publish_episode		
Publish episode after encoding
query	boolean
Response Messages
HTTP Status Code	Reason	Response Model	Headers
402	
encoding could not be started because user has insufficient encoding minutes left
ModelExample Value
{
  "code": 0,
  "message": "string"
}
404	
production not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
encoding could not be started, probably because of incorrect data in the episode or production
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /productions/{production_id}/stop
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production_id		
Production id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
production stopped
404	
production not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
production could not be stopped
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /productions/{production_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production_id		
Production id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
production destroyed
404	
production not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
production could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /productions/{production_id}
Response Class (Status 200)
production response
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "files": [
    {
      "url": "string",
      "contributor_id": 0,
      "custom_name": "string",
      "type": "multitrack",
      "original_filename": "string"
    }
  ],
  "state": "initial",
  "publication_flag": true,
  "created_at": "2025-03-29T13:54:35.469Z",
  "updated_at": "2025-03-29T13:54:35.469Z",
  "audio_duration_ms": 0,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production_id		
ID of production to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
production not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /productions/{production_id}
Response Class (Status 200)
production updated
ModelExample Value
{
  "id": 0,
  "episode_id": 0,
  "files": [
    {
      "url": "string",
      "contributor_id": 0,
      "custom_name": "string",
      "type": "multitrack",
      "original_filename": "string"
    }
  ],
  "state": "initial",
  "publication_flag": true,
  "created_at": "2025-03-29T13:54:35.470Z",
  "updated_at": "2025-03-29T13:54:35.470Z",
  "audio_duration_ms": 0,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
production_id		
Production id
path	long
production	

Parameter content type: 
Production to update
body	
ModelExample Value
{
  "state": "initial",
  "publication_flag": true,
  "inserts": [
    {
      "title": "string",
      "time": 0
    }
  ]
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
production not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
production could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

TextSnippets Show/Hide List Operations Expand Operations
GET /text_snippets
Response Class (Status 200)
text snippets list
ModelExample Value
[
  {
    "id": 0,
    "podcast_id": 0,
    "title": "string",
    "content": "string"
  }
]

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
podcast_id		
ID of podcast
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
default	
unexpected error
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /text_snippets
Response Class (Status 200)
Text snippet created
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "title": "string",
  "content": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
text_snippet	

Parameter content type: 
New text snippet to create
body	
ModelExample Value
{
  "podcast_id": 0,
  "title": "string",
  "content": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
podcast not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
text snippet could not be created
ModelExample Value
{
  "code": 0,
  "message": "string"
}

DELETE /text_snippets/{text_snippet_id}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
text_snippet_id		
Text snippet id
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Text snippet destroyed
404	
Text snippet not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
Text snippet could not be destroyed
ModelExample Value
{
  "code": 0,
  "message": "string"
}

GET /text_snippets/{text_snippet_id}
Response Class (Status 200)
text snippet response
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "title": "string",
  "content": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
text_snippet_id		
ID of text snippet to fetch
path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
text snippet not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}

PUT /text_snippets/{text_snippet_id}
Response Class (Status 200)
Text snippet updated
ModelExample Value
{
  "id": 0,
  "podcast_id": 0,
  "title": "string",
  "content": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
text_snippet_id		
Text snippet id
path	long
text_snippet	

Parameter content type: 
Text snippet to update
body	
ModelExample Value
{
  "podcast_id": 0,
  "title": "string",
  "content": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
Text snippet not found
ModelExample Value
{
  "code": 0,
  "message": "string"
}
422	
Text snippet could not be updated
ModelExample Value
{
  "code": 0,
  "message": "string"
}

TranscriptionImports Show/Hide List Operations Expand Operations
POST /transcription_imports
Response Class (Status 200)
transcription imported into episode
ModelExample Value
{
  "episode_id": 0,
  "transcription": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
file_url		
URL of the file to be converted. Currently supported formats are: docx, srt, txt, vtt
query	string
episode_id		
Episode id
query	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
unsupported content type
ModelExample Value
{
  "code": 0,
  "message": "string"
}

Uploads Show/Hide List Operations Expand Operations
POST /uploads
Response Class (Status 200)
upload created
ModelExample Value
{
  "upload_url": "string",
  "content_type": "string",
  "file_url": "string",
  "multipart_upload": true,
  "upload_part_urls": [
    "string"
  ],
  "upload_key": "string",
  "part_size": 0,
  "multipart_upload_id": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filename		
Name of the file to be uploaded.
query	string
filesize		
Size of uploaded file.
query	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
422	
unsupported content type
ModelExample Value
{
  "code": 0,
  "message": "string"
}

POST /uploads/part_url
Response Class (Status 200)
generated URL
ModelExample Value
{
  "upload_part_url": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
upload_key		
Upload key for the episode
query	string
multipart_upload_id		
Multipart upload ID
query	string
part_number		
Number of the uploaded part
query	string

POST /uploads/complete_multipart_url
Response Class (Status 200)
generated URL
ModelExample Value
{
  "complete_multipart_upload_url": "string"
}

Response Content Type 
Parameters
Parameter	Value	Description	Parameter Type	Data Type
upload_key		
Upload key for the episode
query	string
multipart_upload_id		
Multipart upload ID
query	string

[ base url: /api/v1 , api version: 1.0.0 ] 