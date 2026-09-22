# Building

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/buildings` | `listBuildings` | List buildings |
| GET | `/public-api/v1/{mode}/buildings/{id}/files` | `listBuildingFiles` | List files of a building |
| GET | `/public-api/v1/{mode}/buildings/{id}` | `getBuilding` | Get building details |

## GET /public-api/v1/{mode}/buildings

**List buildings** — `listBuildings`

Returns buildings under reachable properties for the selected `{mode}`.

Buildings sit between properties and objects in the resource hierarchy (`Mandate → Property → Building → Object`). Each building carries a `propertyId` FK that resolves via `getProperty`.

Scope with `filter[propertyId]` (single property) or `filter[mandateId]` (every building under one mandate). Use `q` for free-text search across name, street, ZIP and city.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name, street, postcode, city. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `street` \| `-street` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, street. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** name, street, postcode, city
- **Filterable:** `filter[propertyId]`, `filter[mandateId]`
- **Sortable:** `id`, `name`, `street` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [BuildingApiResponse](#buildingapiresponse).

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
      "propertyId": 1,
      "name": "string",
      "street": "string",
      "houseNumber": "string",
      "egid": "123456789",
      "buildYear": 1998,
      "lastRenovation": 2018,
      "startOfRenting": "2021-01-01"
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

## GET /public-api/v1/{mode}/buildings/{id}/files

**List files of a building** — `listBuildingFiles`

Returns the files attached to a building. Visible exactly when the building is visible via `getBuilding`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[category]` | query | string enum (18 values) |  | Restricts results to records matching the given category. One of: `finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `uploadedAt` \| `-uploadedAt` \| `fileSize` \| `-fileSize` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, uploadedAt, fileSize. |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

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

## GET /public-api/v1/{mode}/buildings/{id}

**Get building details** — `getBuilding`

Returns a single building by id, including its address, EGID, build year, and `startOfRenting` date.

Use `listBuildings` for discovery when the id is unknown. The `propertyId` FK links back to `getProperty`; `getObject` / `listObjects` traverse down to objects inside this building.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [BuildingApiResponse](#buildingapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Building not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "propertyId": 1,
  "name": "string",
  "street": "string",
  "houseNumber": "string",
  "egid": "123456789",
  "buildYear": 1998,
  "lastRenovation": 2018,
  "startOfRenting": "2021-01-01"
}
```

## Schemas

### BuildingApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `propertyId` | integer | yes | FK to the parent property. Resolve via `getProperty`. |
| `name` | string | yes |  |
| `street` | string | yes |  |
| `houseNumber` | string | yes |  |
| `egid` | string · nullable |  | Swiss federal building identifier (EGID), assigned by the Federal Statistical Office. Null when the building has no EGID on record. |
| `buildYear` | integer · nullable |  | Year the building was constructed. Null when unknown. |
| `lastRenovation` | integer · nullable |  | Year of the most recent renovation. Null when never renovated or unknown. |
| `startOfRenting` | string (date) | yes | First day the building started accepting tenants (ISO 8601 date). |

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
