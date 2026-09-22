# Asset

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/assets` | `listAssets` | List assets |
| GET | `/public-api/v1/{mode}/assets/{id}` | `getAsset` | Get asset details |

## GET /public-api/v1/{mode}/assets

**List assets** — `listAssets`

Returns the assets (equipment/installations) of rental objects reachable for the
selected `{mode}`. Each asset carries `roomId` and `objectId` FKs that resolve via
`getRoom` and `getObject`.

Scope with `filter[roomId]`, `filter[objectId]`, `filter[buildingId]`, or
`filter[propertyId]`; use `q` to search across name, manufacturer, model and serial number.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name, manufacturer, model, serialNo. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[roomId]` | query | integer |  | Restricts results to records belonging to the given room id. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[buildingId]` | query | integer |  | Restricts results to records belonging to the given building id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `nextServiceDate` \| `-nextServiceDate` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, nextServiceDate. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** name, manufacturer, model, serialNo
- **Filterable:** `filter[roomId]`, `filter[objectId]`, `filter[buildingId]`, `filter[propertyId]`
- **Sortable:** `id`, `name`, `nextServiceDate` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [AssetApiResponse](#assetapiresponse).

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
      "roomId": 301,
      "objectId": 789,
      "name": "Geschirrspüler",
      "category": "Haushaltsgerät",
      "description": "string",
      "manufacturer": "string",
      "model": "string",
      "serialNo": "string",
      "buildYear": 2021,
      "dateOfPurchase": "2021-06-15",
      "guaranteePeriodYears": 2,
      "lifeExpectancyYears": 12,
      "lastServiceDate": "2025-02-10",
      "nextServiceDate": "2027-02-10",
      "cost": "1890.00"
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

## GET /public-api/v1/{mode}/assets/{id}

**Get asset details** — `getAsset`

Returns a single asset by id, including its template `category`, identification
(manufacturer, model, serial number), and service/guarantee dates.

Use `listAssets` for discovery when the id is unknown. The `roomId` / `objectId` FKs
link back to `getRoom` / `getObject`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [AssetApiResponse](#assetapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Asset not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "roomId": 301,
  "objectId": 789,
  "name": "Geschirrspüler",
  "category": "Haushaltsgerät",
  "description": "string",
  "manufacturer": "string",
  "model": "string",
  "serialNo": "string",
  "buildYear": 2021,
  "dateOfPurchase": "2021-06-15",
  "guaranteePeriodYears": 2,
  "lifeExpectancyYears": 12,
  "lastServiceDate": "2025-02-10",
  "nextServiceDate": "2027-02-10",
  "cost": "1890.00"
}
```

## Schemas

### AssetApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `roomId` | integer | yes | FK to the room this asset is located in. Resolve via `getRoom`. |
| `objectId` | integer | yes | FK to the rental object this asset belongs to. Resolve via `getObject`. |
| `name` | string | yes | Asset name, e.g. "Geschirrspüler". |
| `category` | string · nullable |  | Asset template name (customer/system-defined), e.g. "Haushaltsgerät". Null when not based on a template. |
| `description` | string · nullable |  |  |
| `manufacturer` | string · nullable |  |  |
| `model` | string · nullable |  |  |
| `serialNo` | string · nullable |  | Serial number. Null when not recorded. |
| `buildYear` | integer · nullable |  | Year the asset was built/manufactured. Null when not recorded. |
| `dateOfPurchase` | string (date) · nullable |  | Date of purchase. Null when not recorded. |
| `guaranteePeriodYears` | integer · nullable |  | Guarantee/warranty period in years. Null when not recorded. |
| `lifeExpectancyYears` | integer · nullable |  | Expected life span in years. Null when not recorded. |
| `lastServiceDate` | string (date) · nullable |  | Date of the last service. Null when not recorded. |
| `nextServiceDate` | string (date) · nullable |  | Date of the next scheduled service. Null when not recorded. |
| `cost` | string · nullable |  | Purchase/installation cost as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. Null when not recorded. |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
