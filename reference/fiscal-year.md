# FiscalYear

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/fiscal-years` | `listFiscalYears` | List fiscal years |
| GET | `/public-api/v1/{mode}/fiscal-years/{id}` | `getFiscalYear` | Get a fiscal year |

## GET /public-api/v1/{mode}/fiscal-years

**List fiscal years** — `listFiscalYears`

Returns the fiscal years reachable for the selected `{mode}`: regular accounting
years (per property) and consolidation years (per mandate). Internal
ancillary-expense and reporting periods are never returned.

Narrow with `filter[propertyId]` (accounting years), `filter[mandateId]`
(consolidation years), `filter[type]`, or `filter[isLocked]`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search. Case-insensitive partial match; every word must match one of the searchable fields. Combine with filter[...] keys to narrow further. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `filter[type]` | query | string: `accounting` \| `consolidation` |  | Restricts results to records matching the given type. |
| `filter[isLocked]` | query | string: `true` \| `false` |  | Restricts results to records matching the given isLocked. |
| `sort` | query | string: `starts` \| `-starts` \| `id` \| `-id` |  | Sort field. Prefix with `-` for descending order (e.g. `-starts`). Allowed: starts, id. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** Free-text search
- **Filterable:** `filter[propertyId]`, `filter[mandateId]`, `filter[type]` (`accounting`, `consolidation`), `filter[isLocked]` (`true`, `false`)
- **Sortable:** `starts`, `id` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [FiscalYearApiResponse](#fiscalyearapiresponse).

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
      "propertyId": 7,
      "mandateId": null,
      "label": "2025",
      "type": "accounting",
      "starts": "2025-01-01",
      "ends": "2025-12-31",
      "isLocked": true
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

## GET /public-api/v1/{mode}/fiscal-years/{id}

**Get a fiscal year** — `getFiscalYear`

Returns a single fiscal year by id. Returns 404 when it does not exist, is an
internal ancillary-expense / reporting period, is outside the token's scope, or
does not belong to the selected `{mode}`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [FiscalYearApiResponse](#fiscalyearapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Fiscal year not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "propertyId": 7,
  "mandateId": null,
  "label": "2025",
  "type": "accounting",
  "starts": "2025-01-01",
  "ends": "2025-12-31",
  "isLocked": true
}
```

## Schemas

### FiscalYearApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `propertyId` | integer · nullable |  | FK to the property. Set when `type` is `accounting`, otherwise null. |
| `mandateId` | integer · nullable |  | FK to the mandate. Set when `type` is `consolidation`, otherwise null. |
| `label` | string | yes | Human-readable label, e.g. the year. |
| `type` | [FiscalYearType](#fiscalyeartype) | yes |  |
| `starts` | string (date) | yes |  |
| `ends` | string (date) | yes |  |
| `isLocked` | boolean | yes | Bookings in this year can no longer be added or changed. Independent of whether the year has been closed: closing posts a `closing_entry` booking, locking is a separate flag that can be set and lifted on its own. |

### FiscalYearType

String enum, 2 values.

`accounting`, `consolidation`

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
