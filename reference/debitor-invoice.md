# DebitorInvoice

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/debitor-invoices` | `listDebitorInvoices` | List debitor invoices |
| GET | `/public-api/v1/{mode}/debitor-invoices/{id}` | `getDebitorInvoice` | Get debitor invoice details |

## GET /public-api/v1/{mode}/debitor-invoices

**List debitor invoices** — `listDebitorInvoices`

Returns the debitor invoices (receivables issued to tenants/owners) reachable for
the selected `{mode}`, across all sources (rent, ancillary-expense settlements,
final accounts, manual invoices). Draft and vacancy invoices are never returned.
Each row carries the derived `status`, `isOverdue`, the aggregated `paidAmount` /
`openAmount` balance, and the linked recipient `persons`; the inline `positions`
and `payments` are on the detail endpoint.

Narrow with `filter[status]`, `filter[isOverdue]` (the dunning filter),
`filter[type]`, `filter[personId]` (the tenant-portal balance filter),
`filter[contractId]`, `filter[objectId]`, `filter[propertyId]`,
`filter[mandateId]`, or the `filter[dueDateFrom]` / `filter[dueDateTo]` range.
Use `q` to search by invoice number or label.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: reference, label. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[status]` | query | string: `sent` \| `partially_paid` \| `paid` \| `overpaid` |  | Restricts results to records matching the given status. |
| `filter[isOverdue]` | query | string: `true` \| `false` |  | Restricts results to records matching the given isOverdue. |
| `filter[type]` | query | string: `rent` \| `ancillary_expense` \| `final_account` \| `manual` \| `budget` \| `opening` |  | Restricts results to records matching the given type. |
| `filter[personId]` | query | integer |  | Restricts results to records belonging to the given person id. |
| `filter[contractId]` | query | integer |  | Restricts results to records belonging to the given contract id. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `filter[dueDateFrom]` | query | string (date) |  | Lower (inclusive) bound: only records whose dueDate is on or after this value. |
| `filter[dueDateTo]` | query | string (date) |  | Upper (inclusive) bound: only records whose dueDate is on or before this value. |
| `sort` | query | string: `id` \| `-id` \| `invoiceDate` \| `-invoiceDate` \| `dueDate` \| `-dueDate` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, invoiceDate, dueDate. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** reference, label
- **Filterable:** `filter[status]` (`sent`, `partially_paid`, `paid`, `overpaid`), `filter[isOverdue]` (`true`, `false`), `filter[type]` (`rent`, `ancillary_expense`, `final_account`, `manual`, `budget`, `opening`), `filter[personId]`, `filter[contractId]`, `filter[objectId]`, `filter[propertyId]`, `filter[mandateId]`, `filter[dueDateFrom]`, `filter[dueDateTo]`
- **Sortable:** `id`, `invoiceDate`, `dueDate` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [DebitorInvoiceApiResponse](#debitorinvoiceapiresponse).

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
      "contractId": 456,
      "objectId": 789,
      "propertyId": 7,
      "reference": "100001234",
      "label": "Mietzins Juni 2026",
      "type": "rent",
      "status": "sent",
      "isOverdue": true,
      "invoiceDate": "2026-05-20",
      "dueDate": "2026-06-01",
      "periodFrom": "2025-01-31",
      "periodTo": "2025-01-31",
      "currency": "CHF",
      "amount": "1700.00",
      "paidAmount": "1000.00",
      "openAmount": "700.00",
      "qrReference": "string",
      "reminderLevel": 1,
      "lastReminderAt": "2025-01-31",
      "persons": [
        {
          "personId": 123,
          "isPrimary": true
        }
      ]
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

## GET /public-api/v1/{mode}/debitor-invoices/{id}

**Get debitor invoice details** — `getDebitorInvoice`

Returns a single debitor invoice by id, including the recipient `persons`, the
inline `positions` and matched `payments`, and the derived `status` / `isOverdue`
and `paidAmount` / `openAmount` balance. Returns 404 when the invoice does not
exist, is a draft or vacancy invoice, is outside the token's scope, or does not
belong to the selected `{mode}`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [DebitorInvoiceDetailApiResponse](#debitorinvoicedetailapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Debitor invoice not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "positions": [
    {
      "label": "Nettomiete",
      "type": "normal",
      "amount": "1500.00"
    }
  ],
  "payments": [
    {
      "paidAt": "2026-06-05",
      "amount": "1000.00"
    }
  ],
  "id": 1,
  "contractId": 456,
  "objectId": 789,
  "propertyId": 7,
  "reference": "100001234",
  "label": "Mietzins Juni 2026",
  "type": "rent",
  "status": "sent",
  "isOverdue": true,
  "invoiceDate": "2026-05-20",
  "dueDate": "2026-06-01",
  "periodFrom": "2025-01-31",
  "periodTo": "2025-01-31",
  "currency": "CHF",
  "amount": "1700.00",
  "paidAmount": "1000.00",
  "openAmount": "700.00",
  "qrReference": "string",
  "reminderLevel": 1,
  "lastReminderAt": "2025-01-31",
  "persons": [
    {
      "personId": 123,
      "isPrimary": true
    }
  ]
}
```

## Schemas

### DebitorInvoiceApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `contractId` | integer | yes | FK to the contract the invoice belongs to. Resolve via `getContract`. |
| `objectId` | integer | yes | FK to the object, derived via the contract. Resolve via `getObject`. |
| `propertyId` | integer | yes | FK to the property, derived via the contract. Resolve via `getProperty`. |
| `reference` | string | yes | Invoice number. |
| `label` | string | yes | Human-readable invoice label. |
| `type` | [DebitorInvoiceType](#debitorinvoicetype) | yes |  |
| `status` | [DebitorInvoiceStatus](#debitorinvoicestatus) | yes |  |
| `isOverdue` | boolean | yes | Derived: the due date has passed and the invoice is not settled (not paid/overpaid). |
| `invoiceDate` | string (date) | yes |  |
| `dueDate` | string (date) | yes |  |
| `periodFrom` | string (date) · nullable |  | Billing period start (rent invoices); null when not applicable. |
| `periodTo` | string (date) · nullable |  | Billing period end (rent invoices); null when not applicable. |
| `currency` | string | yes |  |
| `amount` | string | yes | Invoice total as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. |
| `paidAmount` | string | yes | Sum of matched payments as a fixed two-decimal string — derived. |
| `openAmount` | string | yes | Outstanding balance (`amount - paidAmount`) as a fixed two-decimal string — derived. Negative when overpaid. |
| `qrReference` | string · nullable |  | Swiss QR-bill reference; null if none. |
| `reminderLevel` | integer | yes | Dunning level, 0–3. |
| `lastReminderAt` | string (date) · nullable |  | When the last reminder was created; null if none. |
| `persons` | [DebitorInvoicePersonResponse](#debitorinvoicepersonresponse)[] | yes | Persons the invoice is addressed to (recipients). |

### DebitorInvoiceType

String enum, 6 values.

`rent`, `ancillary_expense`, `final_account`, `manual`, `budget`, `opening`

### DebitorInvoiceStatus

String enum, 4 values.

`sent`, `partially_paid`, `paid`, `overpaid`

### DebitorInvoicePersonResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `personId` | integer | yes | FK to the person resource. Resolve via `getPerson`. |
| `isPrimary` | boolean | yes | True for the primary recipient of the invoice. |

### PaginationMeta

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `limit` | integer | yes |  |
| `offset` | integer | yes |  |
| `total` | integer | yes |  |
| `hasMore` | boolean | yes |  |

### DebitorInvoiceDetailApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `positions` | [DebitorInvoicePositionResponse](#debitorinvoicepositionresponse)[] | yes | Invoice line items, ordered by position. |
| `payments` | [DebitorInvoicePaymentResponse](#debitorinvoicepaymentresponse)[] | yes | Payments matched to the invoice. |
| `id` | integer | yes |  |
| `contractId` | integer | yes | FK to the contract the invoice belongs to. Resolve via `getContract`. |
| `objectId` | integer | yes | FK to the object, derived via the contract. Resolve via `getObject`. |
| `propertyId` | integer | yes | FK to the property, derived via the contract. Resolve via `getProperty`. |
| `reference` | string | yes | Invoice number. |
| `label` | string | yes | Human-readable invoice label. |
| `type` | [DebitorInvoiceType](#debitorinvoicetype) | yes |  |
| `status` | [DebitorInvoiceStatus](#debitorinvoicestatus) | yes |  |
| `isOverdue` | boolean | yes | Derived: the due date has passed and the invoice is not settled (not paid/overpaid). |
| `invoiceDate` | string (date) | yes |  |
| `dueDate` | string (date) | yes |  |
| `periodFrom` | string (date) · nullable |  | Billing period start (rent invoices); null when not applicable. |
| `periodTo` | string (date) · nullable |  | Billing period end (rent invoices); null when not applicable. |
| `currency` | string | yes |  |
| `amount` | string | yes | Invoice total as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. |
| `paidAmount` | string | yes | Sum of matched payments as a fixed two-decimal string — derived. |
| `openAmount` | string | yes | Outstanding balance (`amount - paidAmount`) as a fixed two-decimal string — derived. Negative when overpaid. |
| `qrReference` | string · nullable |  | Swiss QR-bill reference; null if none. |
| `reminderLevel` | integer | yes | Dunning level, 0–3. |
| `lastReminderAt` | string (date) · nullable |  | When the last reminder was created; null if none. |
| `persons` | [DebitorInvoicePersonResponse](#debitorinvoicepersonresponse)[] | yes | Persons the invoice is addressed to (recipients). |

### DebitorInvoicePositionResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | string | yes | Line-item label. |
| `type` | [InvoicePositionType](#invoicepositiontype) | yes |  |
| `amount` | string | yes | Line-item amount as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. |

### InvoicePositionType

String enum, 15 values.

`normal`, `vat`, `rent_net`, `rent_ancillary_expenses_actual`, `rent_ancillary_expenses_flat`, `ae_floating_reduction`, `ae_costs`, `administration_fee`, `rounding`, `budget_cost_share`, `budget_revenue_share`, `budget_fund_deposit`, `budget_previous_balance`, `budget_advance_charge`, `final_account`

### DebitorInvoicePaymentResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `paidAt` | string (date) | yes | Date the payment was received. |
| `amount` | string | yes | Payment amount as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. |
