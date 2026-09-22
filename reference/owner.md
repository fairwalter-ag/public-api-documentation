# Owner

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/condo/owners` | `listOwners` | List condo owners |
| GET | `/public-api/v1/condo/owners/{id}/files` | `listOwnerFiles` | List files of a condo owner |
| GET | `/public-api/v1/condo/owners/{id}` | `getOwner` | Get condo owner details |

## GET /public-api/v1/condo/owners

**List condo owners** — `listOwners`

Returns condo ownership relations (Stockwerkeigentümer) reachable by the token.
Vacancy contracts are filtered out. Each row carries the derived `status`, the
unit's `quota` and `hasVotingRight`, the linked `persons`, and the
`currentContribution` effective today; the full contribution history is on the
detail endpoint.

Narrow with `filter[status]`, `filter[personId]`, `filter[objectId]`,
`filter[propertyId]` or `filter[mandateId]`. Use `q` to search by linked person
name.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name1, name2. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[status]` | query | string: `upcoming` \| `active` \| `terminated` |  | Restricts results to records matching the given status. |
| `filter[personId]` | query | integer |  | Restricts results to records belonging to the given person id. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `sort` | query | string: `id` \| `-id` \| `starts` \| `-starts` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, starts. |

**List capabilities**

- **Searchable (`q`):** name1, name2
- **Filterable:** `filter[status]` (`upcoming`, `active`, `terminated`), `filter[personId]`, `filter[objectId]`, `filter[propertyId]`, `filter[mandateId]`
- **Sortable:** `id`, `starts` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [OwnerApiResponse](#ownerapiresponse).

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
      "objectId": 640,
      "status": "upcoming",
      "starts": "2019-07-01",
      "ends": "2025-01-31",
      "quota": 85,
      "hasVotingRight": true,
      "qrReference": "string",
      "persons": [
        {
          "personId": 123,
          "roles": [
            "tenant"
          ],
          "isPrimary": true
        }
      ],
      "currentContribution": {
        "starts": "2026-01-01",
        "ends": "2025-01-31",
        "amount": "1200.00",
        "amountMonthly": "400.00",
        "billingCycle": 3,
        "positions": [
          {
            "name": "Heizkosten",
            "settlementMode": "flat",
            "amount": "80.00"
          }
        ]
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

## GET /public-api/v1/condo/owners/{id}/files

**List files of a condo owner** — `listOwnerFiles`

Returns the files attached to a condo owner. Visible exactly when the owner is visible via `getOwner`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[category]` | query | string enum (18 values) |  | Restricts results to records matching the given category. One of: `finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `uploadedAt` \| `-uploadedAt` \| `fileSize` \| `-fileSize` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, uploadedAt, fileSize. |
| `id` | path | integer | yes |  |

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

## GET /public-api/v1/condo/owners/{id}

**Get condo owner details** — `getOwner`

Returns a single condo ownership relation by id, including the unit's `quota`
and `hasVotingRight`, the linked `persons`, the `currentContribution`, and the full
`contributions` history. Returns 404 when the relation does not exist, is not a
condo relation, or is outside the token's scope.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [OwnerDetailApiResponse](#ownerdetailapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Owner not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "contributions": [
    {
      "starts": "2026-01-01",
      "ends": "2025-01-31",
      "amount": "1200.00",
      "amountMonthly": "400.00",
      "billingCycle": 3,
      "positions": [
        {
          "name": "Heizkosten",
          "settlementMode": "flat",
          "amount": "80.00"
        }
      ]
    }
  ],
  "id": 1,
  "objectId": 640,
  "status": "upcoming",
  "starts": "2019-07-01",
  "ends": "2025-01-31",
  "quota": 85,
  "hasVotingRight": true,
  "qrReference": "string",
  "persons": [
    {
      "personId": 123,
      "roles": [
        "tenant"
      ],
      "isPrimary": true
    }
  ],
  "currentContribution": {
    "starts": "2026-01-01",
    "ends": "2025-01-31",
    "amount": "1200.00",
    "amountMonthly": "400.00",
    "billingCycle": 3,
    "positions": [
      {
        "name": "Heizkosten",
        "settlementMode": "flat",
        "amount": "80.00"
      }
    ]
  }
}
```

## Schemas

### OwnerApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `objectId` | integer | yes | FK to the object resource. Resolve via `getObject`. |
| `status` | [OwnerStatus](#ownerstatus) | yes |  |
| `starts` | string (date) | yes | Ownership start. |
| `ends` | string (date) · nullable |  | Ownership end (e.g. on sale); null while ongoing. |
| `quota` | integer · nullable |  | Wertquota of the unit (ownership share, per-mille); null if not set. |
| `hasVotingRight` | boolean | yes | Voting right at the owners' assembly. |
| `qrReference` | string · nullable |  | Swiss QR-bill reference for contribution payments; null if none. |
| `persons` | [RelatedPersonResponse](#relatedpersonresponse)[] | yes | Persons linked to the ownership relation (owners and residents merged). |
| `currentContribution` | [ContributionResponse](#contributionresponse) · nullable |  | The contribution version effective today; null if none is effective. |

### OwnerStatus

String enum, 3 values.

`upcoming`, `active`, `terminated`

### RelatedPersonResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `personId` | integer | yes | FK to the person resource. Resolve via `getPerson`. |
| `roles` | string: `tenant` \| `owner` \| `resident`[] | yes | Roles this person holds on the entry. `tenant`/`owner` = signatory, `resident` = occupant; a person can hold both. `tenant` appears on rent contracts, `owner` on condo owners. |
| `isPrimary` | boolean | yes | True for the single primary signatory (primary `tenant`/`owner`). Always false for pure residents. |

### ContributionResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `starts` | string (date) | yes | Start of this contribution version. |
| `ends` | string (date) · nullable |  | End of this contribution version; null for the current version. |
| `amount` | string | yes | Contribution per billing cycle. Fixed two-decimal string. |
| `amountMonthly` | string | yes | Derived monthly contribution (`amount / billingCycle`). Fixed two-decimal string. |
| `billingCycle` | integer: `1` \| `3` \| `6` \| `12` | yes | Months per billing cycle. |
| `positions` | [AncillaryExpenseResponse](#ancillaryexpenseresponse)[] | yes | Cost breakdown — same semantics as rent ancillary expenses. |

### AncillaryExpenseResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | yes | Position label as configured on the account. |
| `settlementMode` | [SettlementMode](#settlementmode) | yes |  |
| `amount` | string · nullable |  | Fixed amount as a two-decimal string for `flat` positions; `null` for `settled` positions (those are collected via the gross/net difference). Sent as a string to preserve precision. |

### SettlementMode

String enum, 2 values.

`flat`, `settled`

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

### OwnerDetailApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `contributions` | [ContributionResponse](#contributionresponse)[] | yes | Full contribution version history, ordered by `starts`. |
| `id` | integer | yes |  |
| `objectId` | integer | yes | FK to the object resource. Resolve via `getObject`. |
| `status` | [OwnerStatus](#ownerstatus) | yes |  |
| `starts` | string (date) | yes | Ownership start. |
| `ends` | string (date) · nullable |  | Ownership end (e.g. on sale); null while ongoing. |
| `quota` | integer · nullable |  | Wertquota of the unit (ownership share, per-mille); null if not set. |
| `hasVotingRight` | boolean | yes | Voting right at the owners' assembly. |
| `qrReference` | string · nullable |  | Swiss QR-bill reference for contribution payments; null if none. |
| `persons` | [RelatedPersonResponse](#relatedpersonresponse)[] | yes | Persons linked to the ownership relation (owners and residents merged). |
| `currentContribution` | [ContributionResponse](#contributionresponse) · nullable |  | The contribution version effective today; null if none is effective. |
