# Account

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/accounts` | `listAccounts` | List the chart of accounts |
| GET | `/public-api/v1/{mode}/accounts/{id}` | `getAccount` | Get a single account |

## GET /public-api/v1/{mode}/accounts

**List the chart of accounts** — `listAccounts`

Returns the customer's own chart of accounts for the selected `{mode}` chart
(rent/condo). The chart is customer-level, so every token of the customer sees the
same accounts.

Narrow with `filter[category]`. Use `q` to search by `label` (substring) or
`number` (prefix).

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: number, label. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[category]` | query | string: `assets` \| `liabilities` \| `revenue` \| `expenses` |  | Restricts results to records matching the given category. |
| `sort` | query | string: `number` \| `-number` \| `id` \| `-id` |  | Sort field. Prefix with `-` for descending order (e.g. `-number`). Allowed: number, id. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** number, label
- **Filterable:** `filter[category]` (`assets`, `liabilities`, `revenue`, `expenses`)
- **Sortable:** `number`, `id` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [AccountApiResponse](#accountapiresponse).

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
      "number": 1020,
      "label": "Bank",
      "category": "assets",
      "group": {
        "id": 17,
        "label": "Kapital der Eigentümer"
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

## GET /public-api/v1/{mode}/accounts/{id}

**Get a single account** — `getAccount`

Returns one account of the customer's own `{mode}` chart by id. Returns 404 when the
account does not exist, is not on the `{mode}` chart, or belongs to another customer.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [AccountApiResponse](#accountapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Account not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "number": 1020,
  "label": "Bank",
  "category": "assets",
  "group": {
    "id": 17,
    "label": "Kapital der Eigentümer"
  }
}
```

## Schemas

### AccountApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `number` | integer | yes | Account number, e.g. 1000. |
| `label` | string | yes |  |
| `category` | [AccountCategory](#accountcategory) | yes |  |
| `group` | [AccountGroupResponse](#accountgroupresponse) | yes |  |

### AccountCategory

String enum, 4 values.

`assets`, `liabilities`, `revenue`, `expenses`

### AccountGroupResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes | Stable id of the group. Groups are part of the chart of accounts, not customer data. |
| `label` | string | yes | German group heading as it appears on a financial statement. |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
