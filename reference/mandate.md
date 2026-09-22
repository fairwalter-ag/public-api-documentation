# Mandate

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/mandates` | `listMandates` | List mandates |
| GET | `/public-api/v1/mandates/{id}/files` | `listMandateFiles` | List files of a mandate |
| GET | `/public-api/v1/mandates/{id}` | `getMandate` | Get mandate details |

## GET /public-api/v1/mandates

**List mandates** — `listMandates`

Returns mandates the calling token can reach.

A mandate is the top of the Public API resource hierarchy: `Mandate → Property → Building → Object`. Every other resource lives under exactly one mandate, so this endpoint is the discovery starting point.

No filter keys are exposed (mandates are not scoped by any other resource); use `q` for free-text search across the mandate name, second name, street, postal code and city. Read `type` on each returned mandate (`rent` or `condo`) to decide which `{mode}` to pass on related endpoints.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name1, name2, street, postcode, city. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name. |

**List capabilities**

- **Searchable (`q`):** name1, name2, street, postcode, city
- **Sortable:** `id`, `name` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [MandateApiResponse](#mandateapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `400` | Invalid query parameters |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "data": [
    {
      "id": 1,
      "name1": "Müller",
      "name2": "Anna",
      "contactType": "natural",
      "type": "rent",
      "salutation": "unspecified",
      "email": "string",
      "phone": "string",
      "website": "string",
      "address": {
        "street": "string",
        "houseNumber": "string",
        "postcode": "string",
        "city": "string",
        "country": "string"
      }
    }
  ],
  "meta": {
    "pagination": {
      "limit": 30,
      "offset": 0,
      "total": 1,
      "hasMore": false
    }
  }
}
```

## GET /public-api/v1/mandates/{id}/files

**List files of a mandate** — `listMandateFiles`

Returns the files attached to a mandate. Visible exactly when the mandate is visible via `getMandate`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[category]` | query | string enum (18 values) |  | Restricts results to records matching the given category. One of: `finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `uploadedAt` \| `-uploadedAt` \| `fileSize` \| `-fileSize` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, uploadedAt, fileSize. |
| `id` | path | integer | yes |  |

**List capabilities**

- **Searchable (`q`):** name
- **Filterable:** `filter[category]` (`finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`)
- **Sortable:** `id`, `name`, `uploadedAt`, `fileSize` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [FileApiResponse](#fileapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `400` | Invalid query parameters |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Parent resource not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "data": [
    {
      "id": 4711,
      "name": "Hausordnung.pdf",
      "category": "finance",
      "mimeType": "application/pdf",
      "fileSize": 184320,
      "uploadedAt": "2026-03-14T09:12:00+01:00"
    }
  ],
  "meta": {
    "pagination": {
      "limit": 30,
      "offset": 0,
      "total": 1,
      "hasMore": false
    }
  }
}
```

## GET /public-api/v1/mandates/{id}

**Get mandate details** — `getMandate`

Returns a single mandate by id, including its contact, address, and `type` (`rent` or `condo`).

Use `listMandates` for discovery when the id is unknown. The returned `type` determines which `{mode}` to pass on related endpoints (`getProperty`, `getBuilding`, `getObject`, and their list counterparts).

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [MandateApiResponse](#mandateapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Mandate not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "name1": "Müller",
  "name2": "Anna",
  "contactType": "natural",
  "type": "rent",
  "salutation": "unspecified",
  "email": "string",
  "phone": "string",
  "website": "string",
  "address": {
    "street": "string",
    "houseNumber": "string",
    "postcode": "string",
    "city": "string",
    "country": "string"
  }
}
```

## Schemas

### MandateApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `name1` | string | yes | Primary name. For a private contact this is the family name; for an organization this is the full legal name. |
| `name2` | string · nullable |  | Secondary name. For a private contact this is the given name(s); for an organization this is the secondary line (e.g. department or c/o). Null when not applicable. |
| `contactType` | [ContactType](#contacttype) | yes |  |
| `type` | [MandateType](#mandatetype) | yes |  |
| `salutation` | [Salutation](#salutation) | yes |  |
| `email` | string · nullable |  |  |
| `phone` | string · nullable |  |  |
| `website` | string · nullable |  |  |
| `address` | [AddressDto](#addressdto) | yes |  |

### ContactType

String enum, 2 values.

`natural`, `legal`

### MandateType

String enum, 2 values.

`rent`, `condo`

### Salutation

String enum, 3 values.

`unspecified`, `mrs`, `mr`

### AddressDto

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `street` | string | yes |  |
| `houseNumber` | string | yes |  |
| `postcode` | string | yes |  |
| `city` | string | yes |  |
| `country` | string | yes |  |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |

### FileApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes | Resolve metadata via `getFile` and the binary via `downloadFile`. |
| `name` | string | yes | File name as uploaded. |
| `category` | [FileCategory](#filecategory) | yes |  |
| `mimeType` | string | yes | Stored content type. |
| `fileSize` | integer | yes | Size in bytes. |
| `uploadedAt` | string (date-time) | yes | When the file was uploaded, ISO 8601. |

### FileCategory

String enum, 18 values.

`finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`
