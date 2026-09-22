# File

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/files/{id}/content` | `downloadFile` | Download a file |
| GET | `/public-api/v1/files/{id}` | `getFile` | Get file metadata |

## GET /public-api/v1/files/{id}/content

**Download a file** — `downloadFile`

Streams the file's bytes as an attachment, named as it was uploaded. Visibility is
identical to `getFile`. Counts against the ordinary request rate limit.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

| Status | Description |
| --- | --- |
| `200` | The file, as an attachment. |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | File not found |
| `429` | Rate limit exceeded |

## GET /public-api/v1/files/{id}

**Get file metadata** — `getFile`

Returns a file's metadata and the attachments of it you may see. There is no top-level
`category`: the category belongs to the attachment, and one file can be attached to
several owners with a different category on each.

A file whose only owners are outside your scope, or of a kind this API does not expose,
is indistinguishable from one that does not exist. Use `downloadFile` for the binary.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [FileDetailApiResponse](#filedetailapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | File not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "name": "Hausordnung.pdf",
  "mimeType": "application/pdf",
  "fileSize": 184320,
  "uploadedAt": "2026-03-14T09:12:00+01:00",
  "owners": [
    {
      "type": "property",
      "id": 12,
      "category": "finance"
    }
  ]
}
```

## Schemas

### FileDetailApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `name` | string | yes | File name as uploaded. |
| `mimeType` | string | yes | Stored content type. |
| `fileSize` | integer | yes | Size in bytes. |
| `uploadedAt` | string (date-time) | yes | When the file was uploaded, ISO 8601. |
| `owners` | [FileOwnerResponse](#fileownerresponse)[] | yes | The visible attachments of this file. Never empty — a file with no visible owner returns 404. There is no top-level `category`: it belongs to the attachment, and one file can be attached to several owners with a different category on each. |

### FileOwnerResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | [FileOwnerType](#fileownertype) | yes |  |
| `id` | integer | yes | Id of that object, resolvable on its own resource. |
| `category` | [FileCategory](#filecategory) | yes |  |

### FileOwnerType

String enum, 9 values.

`property`, `building`, `object`, `damage`, `contract`, `owner`, `person`, `mandate`, `user`

### FileCategory

String enum, 18 values.

`finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`
