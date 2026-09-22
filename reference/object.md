# Object

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/objects` | `listObjects` | List objects |
| GET | `/public-api/v1/{mode}/objects/{id}/files` | `listObjectFiles` | List files of an object |
| GET | `/public-api/v1/{mode}/objects/{id}` | `getObject` | Get object details |

## GET /public-api/v1/{mode}/objects

**List objects** — `listObjects`

Returns rental objects under reachable buildings for the selected `{mode}`.

Objects are the lowest level of the resource hierarchy (`Mandate → Property → Building → Object`). Each object carries a `buildingId` FK that resolves via `getBuilding`.

Scope with `filter[buildingId]`, `filter[propertyId]`, or `filter[mandateId]` to narrow the result set. Use `q` for free-text search across name, EWID, building name, and street.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name, ewid, buildingName, street. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[buildingId]` | query | integer |  | Restricts results to records belonging to the given building id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `area` \| `-area` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, area. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** name, ewid, buildingName, street
- **Filterable:** `filter[propertyId]`, `filter[buildingId]`, `filter[mandateId]`
- **Sortable:** `id`, `name`, `area` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [ObjectApiResponse](#objectapiresponse).

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
      "buildingId": 1,
      "name": "string",
      "type": "residential_apartment",
      "numberOfRooms": "3.5",
      "area": "85.4",
      "volume": "215",
      "floor": 2,
      "ewid": "001",
      "quota": 50,
      "hasVotingRight": true
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

## GET /public-api/v1/{mode}/objects/{id}/files

**List files of an object** — `listObjectFiles`

Returns the files attached to an object. Visible exactly when the object is visible via `getObject`.

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

## GET /public-api/v1/{mode}/objects/{id}

**Get object details** — `getObject`

Returns a single rental object by id, including its type, dimensions, floor, EWID, and (for condo objects) ownership quota and voting right.

Use `listObjects` for discovery when the id is unknown. The `buildingId` FK links back to `getBuilding`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [ObjectApiResponse](#objectapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Object not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "buildingId": 1,
  "name": "string",
  "type": "residential_apartment",
  "numberOfRooms": "3.5",
  "area": "85.4",
  "volume": "215",
  "floor": 2,
  "ewid": "001",
  "quota": 50,
  "hasVotingRight": true
}
```

## Schemas

### ObjectApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `buildingId` | integer | yes | FK to the parent building. Resolve via `getBuilding`. |
| `name` | string | yes |  |
| `type` | [ObjectType](#objecttype) | yes |  |
| `numberOfRooms` | string | yes | Number of rooms as a decimal string (e.g. "3.5"). Trailing zeros are trimmed. Sent as a string — never a float — to preserve precision. |
| `area` | string | yes | Net floor area in m² as a decimal string. Trailing zeros are trimmed. Sent as a string — never a float — to preserve precision. |
| `volume` | string | yes | Volume in m³ as a decimal string. Trailing zeros are trimmed. Sent as a string — never a float — to preserve precision. |
| `floor` | integer | yes | Floor on which the object is located. Ground floor is 0; basement floors are negative. |
| `ewid` | string · nullable |  | Swiss federal dwelling identifier (EWID), unique within an EGID. Null when the object has no EWID on record. |
| `quota` | integer · nullable |  | Condominium ownership share. Set on condo objects; null for rental objects. |
| `hasVotingRight` | boolean | yes | Whether the owner of this object holds a voting right at the condominium assembly. Meaningful for condo objects; defaults to false otherwise. |

### ObjectType

String enum, 41 values.

`residential_apartment`, `residential_maisonette`, `residential_attic_flat`, `residential_stepped_flat`, `residential_studio`, `residential_single_room`, `residential_granny_flat`, `residential_loft`, `residential_furnished_flat`, `residential_detached_house`, `residential_row_house`, `residential_duplex_house`, `residential_chalet`, `residential_rustico`, `parking_space_outside`, `parking_space_outside_e`, `parking_carport`, `parking_carport_e`, `parking_space_inside`, `parking_space_inside_e`, `parking_garage`, `parking_moto_outside`, `parking_moto_inside`, `commercial_office`, `commercial_retail`, `commercial_doctor`, `commercial_advertising`, `commercial_workshop`, `commercial_hobby_room`, `commercial_atelier`, `commercial_antenna`, `storage_storage`, `gastronomy_restaurant`, `gastronomy_bar`, `gastronomy_cafe`, `agricultural_agricultural`, `industrial_industrial`, `construction_plot`, `investment_investment`, `vacation_vacation`, `other_other`

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
