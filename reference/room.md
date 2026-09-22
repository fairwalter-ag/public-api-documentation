# Room

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/rooms` | `listRooms` | List rooms |
| GET | `/public-api/v1/{mode}/rooms/{id}` | `getRoom` | Get room details |

## GET /public-api/v1/{mode}/rooms

**List rooms** — `listRooms`

Returns the rooms of rental objects reachable for the selected `{mode}`. Each room
carries an `objectId` FK that resolves via `getObject`.

Scope with `filter[objectId]`, `filter[buildingId]`, or `filter[propertyId]`; use `q`
to search by room name.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[buildingId]` | query | integer |  | Restricts results to records belonging to the given building id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** name
- **Filterable:** `filter[objectId]`, `filter[buildingId]`, `filter[propertyId]`
- **Sortable:** `id`, `name` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [RoomApiResponse](#roomapiresponse).

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
      "objectId": 789,
      "name": "Küche",
      "category": "Küche",
      "area": "12.5"
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

## GET /public-api/v1/{mode}/rooms/{id}

**Get room details** — `getRoom`

Returns a single room by id, including its template `category` and `area`.

Use `listRooms` for discovery when the id is unknown. The `objectId` FK links back to `getObject`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [RoomApiResponse](#roomapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Room not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "objectId": 789,
  "name": "Küche",
  "category": "Küche",
  "area": "12.5"
}
```

## Schemas

### RoomApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `objectId` | integer | yes | FK to the rental object this room belongs to. Resolve via `getObject`. |
| `name` | string | yes | Room name, e.g. "Küche" or "Schlafzimmer 1". |
| `category` | string · nullable |  | Room template name (customer/system-defined), e.g. "Badezimmer". Null when the room is not based on a template. |
| `area` | string · nullable |  | Floor area in m² as a decimal string. Trailing zeros are trimmed. Sent as a string — never a float — to preserve precision. Null when not recorded. |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
