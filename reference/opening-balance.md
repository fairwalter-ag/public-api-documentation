# OpeningBalance

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/opening-balances` | `listOpeningBalances` | List opening balances |
| GET | `/public-api/v1/{mode}/opening-balances/{id}` | `getOpeningBalance` | Get an opening balance |

## GET /public-api/v1/{mode}/opening-balances

**List opening balances** — `listOpeningBalances`

Returns the opening balances (starting balances of balance-sheet accounts at the
beginning of a fiscal year) reachable for the selected `{mode}`. Combined with the
year's bookings, a consumer can reconstruct running balances.

The primary use is `filter[fiscalYearId]` — all opening balances of a year. Narrow
further with `filter[accountId]` or `filter[propertyId]`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search. Case-insensitive partial match; every word must match one of the searchable fields. Combine with filter[...] keys to narrow further. |
| `filter[fiscalYearId]` | query | integer |  | Restricts results to records belonging to the given fiscalYear id. |
| `filter[accountId]` | query | integer |  | Restricts results to records belonging to the given account id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `sort` | query | string: `id` \| `-id` \| `accountId` \| `-accountId` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, accountId. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** Free-text search
- **Filterable:** `filter[fiscalYearId]`, `filter[accountId]`, `filter[propertyId]`
- **Sortable:** `id`, `accountId` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [OpeningBalanceApiResponse](#openingbalanceapiresponse).

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
      "fiscalYearId": 31,
      "accountId": 12,
      "propertyId": 7,
      "amount": "15230.45"
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

## GET /public-api/v1/{mode}/opening-balances/{id}

**Get an opening balance** — `getOpeningBalance`

Returns a single opening balance by id. Returns 404 when it does not exist, is
outside the token's scope, or does not belong to the selected `{mode}`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [OpeningBalanceApiResponse](#openingbalanceapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Opening balance not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "fiscalYearId": 31,
  "accountId": 12,
  "propertyId": 7,
  "amount": "15230.45"
}
```

## Schemas

### OpeningBalanceApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `fiscalYearId` | integer | yes | FK to the fiscal year. Resolve via `getFiscalYear`. |
| `accountId` | integer | yes | FK to the account. Resolve via `getAccount`. |
| `propertyId` | integer | yes | FK to the property — opening balances are always per property, even under a consolidation fiscal year. |
| `amount` | string | yes | Opening balance as a fixed two-decimal string. Negative for credit-side balances. Sent as a string — never a float — to preserve precision. |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
