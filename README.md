# Fairwalter Public API

Reference documentation for the read-only Fairwalter public API, version `1.0.0`.

This repository is generated once a day from the live specification at [`https://my.fairwalter.ch/public-api/docs.json`](https://my.fairwalter.ch/public-api/docs.json). Everything below is produced from it — nothing here is written by hand, and the commit history is the changelog of the API.

- [`openapi.json`](openapi.json) — the OpenAPI 3 document, committed verbatim. Point a client generator at it.
- [`reference/`](reference/) — one page per resource: endpoints, parameters, field tables and an example response.
- [`llms.txt`](llms.txt) / [`llms-full.txt`](llms-full.txt) — the same reference in one file, for handing to an assistant.
- [Interactive API console](https://my.fairwalter.ch/public-api/docs) — execute a request against your own data (sign-in required).

## Resources

- [Account](reference/account.md)
- [Asset](reference/asset.md)
- [Booking](reference/booking.md)
- [Building](reference/building.md)
- [Contract](reference/contract.md)
- [Damage](reference/damage.md)
- [DebitorInvoice](reference/debitor-invoice.md)
- [File](reference/file.md)
- [FiscalYear](reference/fiscal-year.md)
- [Mandate](reference/mandate.md)
- [Object](reference/object.md)
- [OpeningBalance](reference/opening-balance.md)
- [Owner](reference/owner.md)
- [Person](reference/person.md)
- [Property](reference/property.md)
- [Room](reference/room.md)
- [Service Provider](reference/service-provider.md)
- [User](reference/user.md)

---

Read-only public API v1.

The OpenAPI 3 document behind this page is served at `/public-api/docs.json` — point your code generator or HTTP client at it directly. It carries an absolute `servers[0].url`, so a generated client works without further configuration.

## Authentication

All `/public-api/v1` endpoints require a personal API token sent as a Bearer token in the `Authorization` header:

```
Authorization: Bearer fw_<your-token>
```

Tokens are issued per user and start with the `fw_` prefix. Contact your Fairwalter administrator to obtain a token.

### Using "Try it out"

Click the **Authorize** button at the top of this page, paste your `fw_...` token (Swagger UI adds the `Bearer ` prefix automatically), then use the "Try it out" buttons on individual endpoints.

## Resource model

Every resource is scoped to the customer the token belongs to, and further to the mandates the token may reach.

**Portfolio** — a one-to-many chain, each level carrying the FK of its parent:

```
Mandate → Property → Building → Object → Room
                                     ↘ Asset
```

- **Mandate** — the contract a property manager holds with an owner. Every other resource lives under exactly one mandate.
- **Property** — a land parcel under a mandate (`mandateId`).
- **Building** — sits on a property (`propertyId`).
- **Object** — a rental or ownership unit inside a building (`buildingId`).
- **Room** — a room inside an object (`objectId`).
- **Asset** — an appliance or installation, attached at whichever level it belongs to (`roomId`, `objectId`, `buildingId` or `propertyId`).

**Occupancy** — who uses an object, and under what agreement:

- **Contract** (`rent` only) — a tenancy on an object (`objectId`, `propertyId`, `mandateId`).
- **Owner** (`condo` only) — an ownership relation on an object. The condo counterpart of a contract, with its own vocabulary.
- **Person** — a natural person or company. Not mode-scoped: the same person can be a tenant here and an owner there. `roles` tells you which. Contracts and owners reference persons; use `filter[personId]` to go the other way.

**Finance** — the general ledger:

```
FiscalYear ──< OpeningBalance >── Account
     ╎                              ╎
     └──────< Booking >─────────────┘
```

- **FiscalYear** — either property-scoped (`type: accounting`, `propertyId` set) or a mandate-level rollup (`type: consolidation`, `mandateId` set). Exactly one of the two ids is non-null; the other is `null`.
- **Account** — one entry of the chart of accounts for the `{mode}` chart, with `number`, `label` and `category`.
- **OpeningBalance** — an account's balance carried into a fiscal year (`fiscalYearId`, `accountId`, `propertyId`).
- **Booking** — one journal entry (`debitAccountId`, `creditAccountId`, `propertyId`).
- **DebitorInvoice** — an outgoing invoice (`contractId`, `objectId`, `propertyId`, `mandateId`), the document behind most rent bookings.

**Operations and access:**

- **Damage** — a damage report (`objectId`, `buildingId`, `propertyId`, optional `serviceProviderId`).
- **ServiceProvider** — a trade contractor. Not mode-scoped.
- **User** — a property-management staff account, referenced by `managerId` on properties. Not mode-scoped.
- **File** — documents, listed under their owner (`/properties/{id}/files`, `/contracts/{id}/files`, …) and fetched by id via `getFile` / `downloadFile`.

Persons and mandates carry `name1` and `name2` (line 1 and line 2 of the name — company plus department, or last plus first name depending on `contactType`), not a single `name`. The one exception is the mandate sort key `sort=name`, which orders by `name1`.

Use `filter[*Id]` on list endpoints to traverse any of these edges. For example, `GET /public-api/v1/rent/objects?filter[propertyId]=42` returns every object under property 42.

## Modes

Most paths include a `{mode}` segment that selects the business domain:

- `rent` — rental-management data (`/public-api/v1/rent/...`).
- `condo` — condominium-ownership data (`/public-api/v1/condo/...`).

Mode constrains every related resource: a `rent` mandate only contains `rent` properties, buildings, and objects, and `{mode}/accounts` returns that mode's chart of accounts. `listMandates`, `listPersons`, `listServiceProviders` and `listUsers` carry no `{mode}` because they span both — mandates are the discriminator, so read `type` on a returned mandate to decide which mode to use for follow-up calls.

## Query parameters

- **Filter:** `filter[key]=value`. Allowed keys differ per endpoint and are listed on each operation.
- **Search:** `q=text` — case-insensitive partial match across the fields named in the `q` description.
- **Sort:** `sort=key` ascending, `sort=-key` descending.

Filters combine with `AND`; `q` narrows the same result set further.

### Bracket encoding

`filter[...]` contains characters that some clients and shells mangle. Either percent-encode the brackets, or disable globbing:

```bash
# Percent-encoded (works everywhere)
curl -H "Authorization: Bearer fw_..." \
  "https://app.fairwalter.ch/public-api/v1/rent/bookings?filter%5BfiscalYearId%5D=31&limit=500"

# Or -g / --globoff to keep the literal brackets
curl -g -H "Authorization: Bearer fw_..." \
  "https://app.fairwalter.ch/public-api/v1/rent/bookings?filter[fiscalYearId]=31&limit=500"
```

Most HTTP libraries encode query parameters for you; the problem is specific to shells and hand-built URLs.

## Response shapes

**List** endpoints wrap their rows in an envelope:

```json
{"data": [{"id": 1}, {"id": 2}], "meta": {"pagination": {"limit": 30, "offset": 0, "total": 2, "hasMore": false}}}
```

**Detail** endpoints return the bare object, with no `data` wrapper:

```json
{"id": 1}
```

This difference is deliberate — a single resource has no pagination to report. Detail responses also carry more fields than the list rows of the same resource.

**Amounts** are strings, never JSON numbers: a fixed two decimal places, `.` as the decimal separator, no thousands separator, no currency symbol (`"1700.00"`, `"-4420.00"`). Parse them as a decimal type with invariant culture — a de-CH locale parser reads `.` as a thousands separator and will silently turn `1700.00` into `170000`. Never parse them as floats.

All amounts are in **CHF**. Fairwalter is a single-currency product, so responses carry no `currency` field.

**Dates** are `YYYY-MM-DD` strings. Date-only fields have no time component or timezone.

## Pagination

List endpoints return at most `limit` items (default `30`) starting at `offset` (default `0`), plus a `meta.pagination` block with `limit`, `offset`, `total`, and `hasMore`. The maximum is `100` on most endpoints; export-oriented ones allow more (bookings: `500`). Each endpoint's `limit` parameter carries its own `maximum` in this spec, and a larger value is capped rather than rejected. To walk a full collection:

```text
offset = 0
loop:
  page = GET .../resources?limit=100&offset={offset}
  process(page.data)
  offset += page.data.length
  if not page.meta.pagination.hasMore: break
```

Prefer `hasMore` over `ceil(total/limit)` for the loop condition — `total` reflects the count at query time and may drift across pages if the underlying data changes. `limit=0` is accepted and silently normalized to 1; pass the endpoint's `maximum` for the largest page.

## Rate limits

Requests are limited to **1200 per minute per token**, measured over a sliding window. Every response carries the current state:

| Header                  | Meaning                                             |
|-------------------------|-----------------------------------------------------|
| `X-RateLimit-Limit`     | Requests allowed in the window.                     |
| `X-RateLimit-Remaining` | Requests left in the current window.                |
| `X-RateLimit-Reset`     | Unix timestamp (seconds) when the window refills.   |

Exceeding the limit returns `429` with error code `http` and a `Retry-After` header holding the number of seconds to wait. Honour it rather than retrying immediately; a bulk export that paginates at the endpoint's maximum page size stays far below the limit.

## Errors

Every error response uses the same JSON envelope:

```json
{
  "code": "badQuery",
  "message": "Unknown filter key: foo",
  "errors": [{"field": "filter.foo", "message": "Unknown filter key"}]
}
```

| Code              | HTTP   | Meaning                                                                |
|-------------------|--------|------------------------------------------------------------------------|
| `badQuery`        | 400    | Malformed query — unknown filter/sort key, invalid pagination value.   |
| `unauthenticated` | 401    | Bearer token missing, malformed, or revoked.                           |
| `accessDenied`    | 403    | Token is valid but cannot reach the requested mandate or object scope. |
| `notFound`        | 404    | No resource with the requested id (or it sits outside the token scope).|
| `http`            | other 4xx | Other client-side error surfaced by the framework, including `429`. |
| `internal`        | 500    | Unhandled server error.                                                |

## Accounting

This section is the contract for anyone building a booking export or a financial statement.

### Sign convention

Every booking is a double entry: exactly one debit account, exactly one credit account, and a **positive** `amount`. The direction is carried by which account is which — there are no negative booking amounts.

Balances are **debit-positive**, and the same formula applies to every account regardless of category:

```
signed_movement(account) = Σ amounts where account is debitAccountId
                         − Σ amounts where account is creditAccountId

closing_balance(account) = opening_balance + signed_movement
```

That single rule is the whole convention. It follows that, in a normal year:

| Category      | Normal sign | Reads as              |
|---------------|-------------|-----------------------|
| `assets`      | ≥ 0         | Aktiven               |
| `liabilities` | ≤ 0         | Passiven (incl. equity) |
| `revenue`     | ≤ 0         | Ertrag                |
| `expenses`    | ≥ 0         | Aufwand               |

Contra accounts flip the sign of their category — a value correction inside `assets` is negative, a revenue reduction is positive. Do not "fix" a sign because it looks wrong for its category; the sign is the data.

`OpeningBalance.amount` is **already signed** with this convention (a credit-side opening balance is negative). Booking `amount` is not — it is always positive.

### Categories and account numbers

`Account.category` has four values. There is deliberately no `equity` category: Fairwalter's internal model has four, and equity accounts file under `liabilities`. The chart follows the Swiss KMU / Liegenschaften layout, so the account `number` gives you the finer structure:

| `category`    | Number range        | Swiss label                                             |
|---------------|---------------------|---------------------------------------------------------|
| `assets`      | 1xxx                | Aktiven                                                 |
| `liabilities` | 2xxx                | Passiven — including 28xx *Kapital der Eigentümer* and 29xx *Reserven und Jahresgewinn/-verlust* (equity) |
| `revenue`     | 3xxx                | Ertrag                                                  |
| `expenses`    | 4xxx–8xxx, and 9000 | Aufwand — 4xxx–6xxx operating, 8xxx extraordinary and non-operating, 9000 the closing account |

Two traps in that table:

- **Account 9000 (`Abschluss Erfolgsrechnung`) is categorised `expenses`.** Summing everything in `expenses` therefore double-counts the annual result of a closed year. Exclude it — see below.
- **The 8xxx block holds both extraordinary income and extraordinary expense** yet sits entirely in `expenses`. Its signed total is what matters, not its category.

Rely on `category` for the statement side and on `number` for subtotals and ordering. `/accounts` returns deactivated accounts too (`isActive: false`), because historic bookings still reference them.

### Unresolvable account ids

`{mode}/accounts` lists one chart — the `rent` chart or the `condo` chart. A booking can reference an account from the *other* chart (this occurs in practice on condo properties booking against rent-chart accounts). Such an id is absent from `{mode}/accounts`, and `{mode}/accounts/{id}` returns `404` for it.

This is why every booking carries `debitAccountNumber` and `creditAccountNumber` alongside the ids: **the number always resolves, even when the id does not.** A ledger export should read the numbers off the booking and never join at all.

If you do need the label or category of such an account, retry the id under the other mode (`/rent/accounts/{id}` when you are exporting `condo`, and vice versa) and fall back to rendering the number alone rather than aborting the export. Never assume every `debitAccountId` / `creditAccountId` on a booking page resolves within the chart you fetched.

### Closing entries

Closing a fiscal year posts one ordinary booking — nothing about it is a special record type:

- `type` is `closing_entry`, and it is the only booking touching account **9000**.
- It is dated the **last day of the fiscal year** and carries `reference` `A` + the 6-digit fiscal-year id (e.g. `A000031`).
- **Profit:** debit 9000 / credit **2990** (`Jahresgewinn oder -verlust`). **Loss:** the reverse, debit 2990 / credit 9000.

Consequences for a consumer:

- **Income statement (Erfolgsrechnung):** exclude the closing entry, or the result appears twice — once as the revenue/expense movement and once as the balance of 9000. Filter it out by `type != closing_entry`, or equivalently by skipping bookings that touch account 9000.
- **Balance sheet (Bilanz):** *include* it. Account 2990 is a `liabilities` account, and after closing it carries the annual result, which is what makes the closed year balance.

**Locked is not closed.** `FiscalYear.isLocked` means bookings can no longer be added or changed; it can be set and lifted on its own. Whether the year has been *closed* is a separate question — answered by whether a `closing_entry` booking exists for it. A year can be locked without a closing entry, and closed without being locked.

### VAT

Fairwalter does **not** track tax codes or tax rates on bookings. There is no VAT field to export, and no way to split an amount into net and tax. Amounts are exactly as booked.

### The `reference` field

`reference` groups the bookings that came out of one source document. Every booking generated from the same invoice carries that invoice's reference, so grouping a page of bookings by `reference` reconstructs the documents behind them. The first character indicates the document type:

| Prefix | Source document                |
|--------|--------------------------------|
| `D`    | Debitor (outgoing) invoice     |
| `K`    | Creditor (incoming) invoice    |
| `G`    | Creditor reimbursement         |
| `N`    | Ancillary-expense settlement   |
| `L`    | Vacancy                        |
| `M`    | Manual booking                 |
| `A`    | Closing entry                  |

Two limits, both load-bearing:

- **It is not a voucher id.** The sequence is per customer, and a combined invoice re-stamps its sub-invoices with the parent's reference — so one reference can legitimately span several invoices. Use it for grouping, never as a primary key.
- **Do not derive the booking type from the prefix.** Historic and migrated data mixes them (creditor bookings carrying `M`, ancillary bookings carrying `D`). The `type` field is authoritative.

On `manual` bookings `reference` is whatever the user typed, so it need not follow any of this.

### Building a Bilanz and an Erfolgsrechnung

1. **Pick the fiscal year.** `GET /{mode}/fiscal-years` → note the `id`, `starts`, `ends`. `type: accounting` years are per property; `type: consolidation` years roll up a mandate.
2. **Fetch the chart.** `GET /{mode}/accounts?limit=100` (paginate) → map `id` → `{number, label, category, group}`. `category` decides the statement side, `group` gives you the subtotal headings, `number` the ordering.
3. **Fetch opening balances.** `GET /{mode}/opening-balances?filter[fiscalYearId]={id}&limit=100` (paginate) → map `accountId` → signed `amount`. Accounts with no row open at `0`.
4. **Fetch the journal.** `GET /{mode}/bookings?filter[fiscalYearId]={id}&limit=500` (paginate). The fiscal-year filter resolves to that year's property and date range for you.
5. **Accumulate.** For each booking add `amount` to its `debitAccountId` and subtract it from its `creditAccountId`. That yields `signed_movement` per account.
6. **Erfolgsrechnung** — movement only, opening balances are irrelevant. Take accounts with `category` `revenue` or `expenses`, **skip the closing entry**, and report `-signed_movement` for revenue (so income reads positive) and `signed_movement` for expenses. Result = revenue − expenses.
7. **Bilanz** — `opening_balance + signed_movement` for accounts with `category` `assets` or `liabilities`, **including** the closing entry.

**Reconciliation checks** — run these before trusting the output:

- Every booking page: `Σ debits = Σ credits` by construction, so the signed movement across *all* accounts must be `0`.
- Closed year: `Σ assets = −Σ liabilities` (Aktiven = Passiven), and `Σ revenue + Σ expenses + balance(9000) = 0`.
- Open year (no closing entry yet): `Σ assets + Σ liabilities = −(Σ revenue + Σ expenses)` — the difference between Aktiven and Passiven *is* the year's result.

### Worked example

One property, fiscal year `31` (2025). Opening balances:

| Account | Category    | `amount`     |
|---------|-------------|--------------|
| 1020 Bank | assets    | `"15230.45"` |
| 2000 Kreditoren | liabilities | `"-4100.00"` |
| 2800 Kapital der Eigentümer | liabilities | `"-11130.45"` |

Opening sums to `0`, as it must. Three bookings during the year:

| Date | Debit | Credit | `amount` | `type` |
|------|-------|--------|----------|--------|
| 2025-03-01 | 1100 Forderungen Mieter | 3000 Mietzins | `"1700.00"` | `debitor_invoice` |
| 2025-03-05 | 1020 Bank | 1100 Forderungen Mieter | `"1700.00"` | `debitor_invoice` |
| 2025-04-10 | 4131 Betriebskosten | 2000 Kreditoren | `"320.00"` | `creditor_invoice` |

Signed movements: `1020 +1700.00`, `1100 0.00`, `3000 −1700.00`, `4131 +320.00`, `2000 −320.00`.

**Erfolgsrechnung:** Ertrag `−(−1700.00) = 1700.00`, Aufwand `320.00`, result **`1380.00`** profit.

Closing therefore posts `debit 9000 / credit 2990`, `"1380.00"`, dated `2025-12-31`, `type: closing_entry`, `reference: "A000031"`.

**Bilanz after closing:**

| Account | Opening | Movement | Closing |
|---------|---------|----------|---------|
| 1020 Bank | `15230.45` | `+1700.00` | `16930.45` |
| 1100 Forderungen | `0.00` | `0.00` | `0.00` |
| 2000 Kreditoren | `-4100.00` | `-320.00` | `-4420.00` |
| 2800 Kapital | `-11130.45` | `0.00` | `-11130.45` |
| 2990 Jahresgewinn | `0.00` | `-1380.00` | `-1380.00` |

Aktiven `16930.45`, Passiven `−16930.45` — balanced. Before the closing entry existed, Aktiven `16930.45` minus Passiven `15550.45` would have left exactly the `1380.00` result.

## Common workflows

**Find every object in a property.** Call `GET /public-api/v1/{mode}/objects?filter[propertyId]={id}` and walk pages until `meta.pagination.hasMore` is `false`.

**Find buildings by address.** Call `GET /public-api/v1/{mode}/buildings?q=Bahnhofstrasse` and inspect `street` / `houseNumber` on the returned items.

**Fetch every resource of a type.** Start at `offset=0` with the endpoint's maximum `limit`, increment `offset` by `data.length` each round, stop when `meta.pagination.hasMore` is `false`.

**Export a year's journal for an accounting package.** Resolve the fiscal year, then page `/{mode}/bookings?filter[fiscalYearId]={id}&limit=500`. Each row already carries `debitAccountNumber` and `creditAccountNumber`, so no account lookup is needed at all — pull `/{mode}/accounts` only if your target system also wants account labels. Group by `reference` if it wants one voucher per document.

## Read-only safety

The API exposes `GET` operations only. No write, update, or delete endpoints exist — calling this API never modifies Fairwalter data.

---

## About this repository

Every file here except `tools/` and `.github/` is generated by [`tools/publish.py`](tools/publish.py) from the live specification — edit the API, not the Markdown.

This documentation is licensed under [CC BY 4.0](LICENSE). Attribution to Fairwalter AG is required.
