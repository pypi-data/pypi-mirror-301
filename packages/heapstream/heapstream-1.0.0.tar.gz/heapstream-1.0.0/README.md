# Heapstream Python SDK 1.0.0

Welcome to the Heapstream SDK documentation. This guide will help you get started with integrating and using the Heapstream SDK in your project.

## Versions

- API version: `1.0`
- SDK version: `1.0.0`

## About the API

Explore the API documentation for [Heapstream.com](//heapstream.com)! ## Authentication API authentication is done using Basic Authentication [wikipedia](https://en.wikipedia.org/wiki/Basic_access_authentication) [RFC7617](https://datatracker.ietf.org/doc/html/rfc7617). For `username` you should use the `id` of the ApiKey. For `password` you should use the `password` of the ApiKey.

## Table of Contents

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Authentication](#authentication)
  - [Basic Authentication](#basic-authentication)
- [Setting a Custom Timeout](#setting-a-custom-timeout)
- [Sample Usage](#sample-usage)
- [Services](#services)
- [Models](#models)
- [License](#license)

## Setup & Configuration

### Supported Language Versions

This SDK is compatible with the following versions: `Python >= 3.7`

### Installation

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install heapstream
```

## Authentication

### Basic Authentication

The Heapstream API uses Basic Authentication.

You need to provide your username and password when initializing the SDK.

#### Setting the Username and Password

When you initialize the SDK, you can set the username and password as follows:

```py
Heapstream(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    timeout=10000
)
```

If you need to set or update the username and password after initializing the SDK, you can use:

```py
sdk.set_basic_auth("YOUR_USERNAME", "YOUR_PASSWORD")
```

## Setting a Custom Timeout

You can set a custom timeout for the SDK's HTTP requests as follows:

```py
from heapstream import Heapstream

sdk = Heapstream(timeout=10000)
```

# Sample Usage

Below is a comprehensive example demonstrating how to authenticate and call a simple endpoint:

```py
from heapstream import Heapstream, Environment

sdk = Heapstream(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.project.list_projects()

print(result)

```

## Services

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services with links to their detailed documentation:</summary>

| Name                                                                 |
| :------------------------------------------------------------------- |
| [ProjectService](documentation/services/ProjectService.md)           |
| [DirectUploadService](documentation/services/DirectUploadService.md) |
| [PlayerService](documentation/services/PlayerService.md)             |
| [StatsService](documentation/services/StatsService.md)               |
| [VideoService](documentation/services/VideoService.md)               |
| [AudioTrackService](documentation/services/AudioTrackService.md)     |
| [PosterService](documentation/services/PosterService.md)             |
| [TextTrackService](documentation/services/TextTrackService.md)       |
| [WatermarkService](documentation/services/WatermarkService.md)       |
| [WebhookService](documentation/services/WebhookService.md)           |

</details>

## Models

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models with links to their detailed documentation:</summary>

| Name                                                                         | Description |
| :--------------------------------------------------------------------------- | :---------- |
| [ProjectList](documentation/models/ProjectList.md)                           |             |
| [ProjectCreate](documentation/models/ProjectCreate.md)                       |             |
| [Project](documentation/models/Project.md)                                   |             |
| [ProjectEdit](documentation/models/ProjectEdit.md)                           |             |
| [DirectUploadStart](documentation/models/DirectUploadStart.md)               |             |
| [DirectUploadResponse](documentation/models/DirectUploadResponse.md)         |             |
| [DirectUploadListResponse](documentation/models/DirectUploadListResponse.md) |             |
| [DirectUploadCompleteArgs](documentation/models/DirectUploadCompleteArgs.md) |             |
| [PartIdResponse](documentation/models/PartIdResponse.md)                     |             |
| [PlayerList](documentation/models/PlayerList.md)                             |             |
| [PlayerCreate](documentation/models/PlayerCreate.md)                         |             |
| [Player](documentation/models/Player.md)                                     |             |
| [PlayerEdit](documentation/models/PlayerEdit.md)                             |             |
| [EngagementStats](documentation/models/EngagementStats.md)                   |             |
| [PerformanceStatsResponse](documentation/models/PerformanceStatsResponse.md) |             |
| [VideoList](documentation/models/VideoList.md)                               |             |
| [ListVideosStatus](documentation/models/ListVideosStatus.md)                 |             |
| [VideoFetch](documentation/models/VideoFetch.md)                             |             |
| [Video](documentation/models/Video.md)                                       |             |
| [VideoEdit](documentation/models/VideoEdit.md)                               |             |
| [PresetList](documentation/models/PresetList.md)                             |             |
| [AudioTrackList](documentation/models/AudioTrackList.md)                     |             |
| [AudioTrackCreate](documentation/models/AudioTrackCreate.md)                 |             |
| [AudioTrack](documentation/models/AudioTrack.md)                             |             |
| [AudioTrackEdit](documentation/models/AudioTrackEdit.md)                     |             |
| [PosterList](documentation/models/PosterList.md)                             |             |
| [MultipartFile](documentation/models/MultipartFile.md)                       |             |
| [Poster](documentation/models/Poster.md)                                     |             |
| [PosterEdit](documentation/models/PosterEdit.md)                             |             |
| [TextTrackList](documentation/models/TextTrackList.md)                       |             |
| [TextTrackCreate](documentation/models/TextTrackCreate.md)                   |             |
| [TextTrack](documentation/models/TextTrack.md)                               |             |
| [TextTrackGenerate](documentation/models/TextTrackGenerate.md)               |             |
| [TextTrackEdit](documentation/models/TextTrackEdit.md)                       |             |
| [WatermarkList](documentation/models/WatermarkList.md)                       |             |
| [WatermarkCreate](documentation/models/WatermarkCreate.md)                   |             |
| [Watermark](documentation/models/Watermark.md)                               |             |
| [WebhookList](documentation/models/WebhookList.md)                           |             |
| [WebhookCreate](documentation/models/WebhookCreate.md)                       |             |
| [Webhook](documentation/models/Webhook.md)                                   |             |
| [UploadMetadata](documentation/models/UploadMetadata.md)                     |             |
| [Asset](documentation/models/Asset.md)                                       |             |
| [AssetError](documentation/models/AssetError.md)                             |             |
| [DirectUploadPart](documentation/models/DirectUploadPart.md)                 |             |
| [EngagementStatsRow](documentation/models/EngagementStatsRow.md)             |             |
| [PerformanceStatsRow](documentation/models/PerformanceStatsRow.md)           |             |
| [Pagination](documentation/models/Pagination.md)                             |             |
| [Preset](documentation/models/Preset.md)                                     |             |
| [AutoCaption](documentation/models/AutoCaption.md)                           |             |

</details>

## License

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.

<!-- This file was generated by liblab | https://liblab.com/ -->
