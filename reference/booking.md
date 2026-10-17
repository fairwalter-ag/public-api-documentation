# Booking

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/bookings` | `listBookings` | List bookings (journal) |
| GET | `/public-api/v1/{mode}/bookings/{id}` | `getBooking` | Get a booking |

## GET /public-api/v1/{mode}/bookings

**List bookings (journal)** — `listBookings`

Returns the journal entries reachable for the selected `{mode}`. Every booking is a
double entry with exactly one debit and one credit account and a positive amount.

The primary export flow is `filter[fiscalYearId]` (resolved to the year's
property/mandate and date range). Narrow further with `filter[dateFrom]` /
`filter[dateTo]` (inclusive range), `filter[accountId]` (debit or credit side),
`filter[propertyId]`, or `filter[type]`. Use `q` to search by label or reference.
This endpoint allows a larger page size (up to 500) for full-year exports.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `500`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: label, reference. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[fiscalYearId]` | query | integer |  | Restricts results to records belonging to the given fiscalYear id. |
| `filter[dateFrom]` | query | string (date) |  | Lower (inclusive) bound: only records whose date is on or after this value. |
| `filter[dateTo]` | query | string (date) |  | Upper (inclusive) bound: only records whose date is on or before this value. |
| `filter[accountId]` | query | integer |  | Restricts results to records belonging to the given account id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[type]` | query | string: `debitor_invoice` \| `creditor_invoice` \| `ancillary_expense` \| `vacancy` \| `reimbursement_invoice` \| `manual` \| `closing_entry` |  | Restricts results to records matching the given type. |
| `sort` | query | string: `date` \| `-date` \| `id` \| `-id` |  | Sort field. Prefix with `-` for descending order (e.g. `-date`). Allowed: date, id. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** label, reference
- **Filterable:** `filter[fiscalYearId]`, `filter[dateFrom]`, `filter[dateTo]`, `filter[accountId]`, `filter[propertyId]`, `filter[type]` (`debitor_invoice`, `creditor_invoice`, `ancillary_expense`, `vacancy`, `reimbursement_invoice`, `manual`, `closing_entry`)
- **Sortable:** `date`, `id` (prefix `-` for descending)
- **Page size:** default `30`, maximum `500`

**Response** — `200` returns a list envelope around [BookingApiResponse](#bookingapiresponse).

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
      "debitAccountId": 45,
      "debitAccountNumber": 1100,
      "creditAccountId": 12,
      "creditAccountNumber": 3000,
      "propertyId": 7,
      "date": "2025-03-01",
      "label": "Mietzins März 2025, Bahnhofstrasse 1, 2.OG",
      "reference": "RE-2025-0341",
      "type": "debitor_invoice",
      "amount": "1700.00"
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

## GET /public-api/v1/{mode}/bookings/{id}

**Get a booking** — `getBooking`

Returns a single journal entry by id. Returns 404 when it does not exist, is outside
the token's scope, or does not belong to the selected `{mode}`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [BookingApiResponse](#bookingapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Booking not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "debitAccountId": 45,
  "debitAccountNumber": 1100,
  "creditAccountId": 12,
  "creditAccountNumber": 3000,
  "propertyId": 7,
  "date": "2025-03-01",
  "label": "Mietzins März 2025, Bahnhofstrasse 1, 2.OG",
  "reference": "RE-2025-0341",
  "type": "debitor_invoice",
  "amount": "1700.00"
}
```

## Schemas

### BookingApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `debitAccountId` | integer | yes | FK to the debit account (Soll). Resolve via `getAccount`. |
| `debitAccountNumber` | integer | yes | Account number of the debit account, embedded so a ledger export needs no join. Resolves even when the account sits on the other `{mode}` chart and `getAccount` would 404. |
| `creditAccountId` | integer | yes | FK to the credit account (Haben). Resolve via `getAccount`. |
| `creditAccountNumber` | integer | yes | Account number of the credit account. See `debitAccountNumber`. |
| `propertyId` | integer | yes | FK to the property. Resolve via `getProperty`. |
| `date` | string (date) | yes |  |
| `label` | string | yes | Booking text. |
| `reference` | string · nullable |  | Free-text reference (e.g. invoice number); null when none. |
| `type` | [BookingType](#bookingtype) | yes |  |
| `amount` | string | yes | Booking amount as a fixed two-decimal string — always positive (direction is given by the debit/credit accounts). |

### BookingType

String enum, 7 values.

`debitor_invoice`, `creditor_invoice`, `ancillary_expense`, `vacancy`, `reimbursement_invoice`, `manual`, `closing_entry`

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |
