# Contract

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/rent/contracts` | `listContracts` | List rent contracts |
| GET | `/public-api/v1/rent/contracts/{id}/files` | `listContractFiles` | List files of a contract |
| GET | `/public-api/v1/rent/contracts/{id}` | `getContract` | Get rent contract details |

## GET /public-api/v1/rent/contracts

**List rent contracts** — `listContracts`

Returns rent contracts (tenancies) reachable by the token, including vacancy
periods (`isVacancy: true`). Each row carries the derived `status`, the linked
`persons`, and the `currentRent` effective today; the full rent version history
is on the detail endpoint.

Narrow with `filter[status]`, `filter[isVacancy]`, `filter[mainContractId]`,
`filter[personId]`, `filter[objectId]`, `filter[propertyId]` or
`filter[mandateId]`. Use `q` to search by linked person name.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name1, name2. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[status]` | query | string: `upcoming` \| `active` \| `noticed` \| `terminated` |  | Restricts results to records matching the given status. |
| `filter[isVacancy]` | query | string: `true` \| `false` |  | Restricts results to records matching the given isVacancy. |
| `filter[mainContractId]` | query | integer |  | Restricts results to records belonging to the given mainContract id. |
| `filter[personId]` | query | integer |  | Restricts results to records belonging to the given person id. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `sort` | query | string: `id` \| `-id` \| `starts` \| `-starts` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, starts. |

**List capabilities**

- **Searchable (`q`):** name1, name2
- **Filterable:** `filter[status]` (`upcoming`, `active`, `noticed`, `terminated`), `filter[isVacancy]` (`true`, `false`), `filter[mainContractId]`, `filter[personId]`, `filter[objectId]`, `filter[propertyId]`, `filter[mandateId]`
- **Sortable:** `id`, `starts` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [ContractApiResponse](#contractapiresponse).

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
      "mainContractId": 1,
      "isVacancy": true,
      "status": "upcoming",
      "starts": "2024-04-01",
      "ends": "2025-01-31",
      "moveIn": "2025-01-31",
      "moveOut": "2025-01-31",
      "noticePeriodMonths": 3,
      "possibleNoticeMonths": [
        3,
        6,
        9
      ],
      "firstPossibleNotice": "2025-01-31",
      "hasVat": true,
      "qrReference": "string",
      "termination": {
        "noticedAt": "2025-01-31",
        "noticedBy": "landlord"
      },
      "deposit": {
        "type": "bank",
        "amount": "4500.00",
        "receivedAt": "2025-01-31",
        "insuranceProvider": "string",
        "insuranceNumber": "string"
      },
      "persons": [
        {
          "personId": 123,
          "roles": [
            "tenant"
          ],
          "isPrimary": true
        }
      ],
      "currentRent": {
        "starts": "2024-04-01",
        "ends": "2025-01-31",
        "netAmount": "1500.00",
        "grossAmount": "1700.00",
        "netAmountMonthly": "1500.00",
        "grossAmountMonthly": "1700.00",
        "billingCycle": 1,
        "hasVat": true,
        "referenceInterestRate": {
          "yearMonth": "2024-03",
          "rate": "1.50"
        },
        "indexBase": {
          "yearMonth": "2020-12"
        },
        "inflationIndex": {
          "yearMonth": "2024-11",
          "value": "107.10"
        },
        "lastCostSettlement": "2025-06",
        "ancillaryExpenses": [
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

## GET /public-api/v1/rent/contracts/{id}/files

**List files of a contract** — `listContractFiles`

Returns the files attached to a rent contract. Visible exactly when the contract is visible via `getContract`.

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

## GET /public-api/v1/rent/contracts/{id}

**Get rent contract details** — `getContract`

Returns a single rent contract (or vacancy entry) by id, including the linked
`persons`, deposit, notice details, the `currentRent`, and the full `rents`
version history. Returns 404 when the contract does not exist, is not a rent
contract, or is outside the token's scope.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [ContractDetailApiResponse](#contractdetailapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Contract not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "rents": [
    {
      "starts": "2024-04-01",
      "ends": "2025-01-31",
      "netAmount": "1500.00",
      "grossAmount": "1700.00",
      "netAmountMonthly": "1500.00",
      "grossAmountMonthly": "1700.00",
      "billingCycle": 1,
      "hasVat": true,
      "referenceInterestRate": {
        "yearMonth": "2024-03",
        "rate": "1.50"
      },
      "indexBase": {
        "yearMonth": "2020-12"
      },
      "inflationIndex": {
        "yearMonth": "2024-11",
        "value": "107.10"
      },
      "lastCostSettlement": "2025-06",
      "ancillaryExpenses": [
        {
          "name": "Heizkosten",
          "settlementMode": "flat",
          "amount": "80.00"
        }
      ]
    }
  ],
  "id": 1,
  "objectId": 789,
  "mainContractId": 1,
  "isVacancy": true,
  "status": "upcoming",
  "starts": "2024-04-01",
  "ends": "2025-01-31",
  "moveIn": "2025-01-31",
  "moveOut": "2025-01-31",
  "noticePeriodMonths": 3,
  "possibleNoticeMonths": [
    3,
    6,
    9
  ],
  "firstPossibleNotice": "2025-01-31",
  "hasVat": true,
  "qrReference": "string",
  "termination": {
    "noticedAt": "2025-01-31",
    "noticedBy": "landlord"
  },
  "deposit": {
    "type": "bank",
    "amount": "4500.00",
    "receivedAt": "2025-01-31",
    "insuranceProvider": "string",
    "insuranceNumber": "string"
  },
  "persons": [
    {
      "personId": 123,
      "roles": [
        "tenant"
      ],
      "isPrimary": true
    }
  ],
  "currentRent": {
    "starts": "2024-04-01",
    "ends": "2025-01-31",
    "netAmount": "1500.00",
    "grossAmount": "1700.00",
    "netAmountMonthly": "1500.00",
    "grossAmountMonthly": "1700.00",
    "billingCycle": 1,
    "hasVat": true,
    "referenceInterestRate": {
      "yearMonth": "2024-03",
      "rate": "1.50"
    },
    "indexBase": {
      "yearMonth": "2020-12"
    },
    "inflationIndex": {
      "yearMonth": "2024-11",
      "value": "107.10"
    },
    "lastCostSettlement": "2025-06",
    "ancillaryExpenses": [
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

### ContractApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `objectId` | integer | yes | FK to the object resource. Resolve via `getObject`. |
| `mainContractId` | integer · nullable |  | FK to the main contract when this is a sub-contract (e.g. parking, basement); null otherwise. |
| `isVacancy` | boolean | yes | True for vacancy entries (Leerstand). |
| `status` | [ContractStatus](#contractstatus) | yes |  |
| `starts` | string (date) | yes |  |
| `ends` | string (date) · nullable |  | Null = open-ended; set + not noticed = fixed-term. |
| `moveIn` | string (date) · nullable |  | Actual move-in date, if tracked. |
| `moveOut` | string (date) · nullable |  | Actual move-out date, if tracked. |
| `noticePeriodMonths` | integer | yes | Notice period in months. 0 for vacancy entries. |
| `possibleNoticeMonths` | integer[] | yes | Months (1–12) in which notice may be given. Empty for vacancy entries. |
| `firstPossibleNotice` | string (date) · nullable |  | Earliest date notice can be given; null if not set. |
| `hasVat` | boolean | yes |  |
| `qrReference` | string · nullable |  | Swiss QR-bill reference for rent payments; null if none. |
| `termination` | [ContractTerminationResponse](#contractterminationresponse) · nullable |  | Notice details; set only once notice has been given. |
| `deposit` | [ContractDepositResponse](#contractdepositresponse) · nullable |  | Security deposit; null when no deposit is recorded. |
| `persons` | [RelatedPersonResponse](#relatedpersonresponse)[] | yes | Persons linked to the contract (tenants and residents merged). |
| `currentRent` | [ContractRentResponse](#contractrentresponse) · nullable |  | The rent version effective today; null if none is effective. |

### ContractStatus

String enum, 4 values.

`upcoming`, `active`, `noticed`, `terminated`

### ContractTerminationResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `noticedAt` | string (date) | yes | Date notice was given. |
| `noticedBy` | [NoticedBy](#noticedby) | yes |  |

### NoticedBy

String enum, 2 values.

`landlord`, `tenant`

### ContractDepositResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | [DepositType](#deposittype) | yes |  |
| `amount` | string | yes | Deposit amount as a fixed two-decimal string. |
| `receivedAt` | string (date) · nullable |  | Date the deposit was received; null if not recorded. |
| `insuranceProvider` | string · nullable |  | Insurance provider — only set when `type` is `insurance`. |
| `insuranceNumber` | string · nullable |  | Insurance policy number — only set when `type` is `insurance`. |

### DepositType

String enum, 4 values.

`bank`, `insurance`, `zinsli`, `other`

### RelatedPersonResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `personId` | integer | yes | FK to the person resource. Resolve via `getPerson`. |
| `roles` | string: `tenant` \| `owner` \| `resident`[] | yes | Roles this person holds on the entry. `tenant`/`owner` = signatory, `resident` = occupant; a person can hold both. `tenant` appears on rent contracts, `owner` on condo owners. |
| `isPrimary` | boolean | yes | True for the single primary signatory (primary `tenant`/`owner`). Always false for pure residents. |

### ContractRentResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `starts` | string (date) | yes | Start of this rent version. |
| `ends` | string (date) · nullable |  | End of this rent version; null for the open-ended current version. |
| `netAmount` | string | yes | Net rent per billing cycle, as stored. Fixed two-decimal string. |
| `grossAmount` | string | yes | Gross rent per billing cycle (net + ancillary). Fixed two-decimal string. |
| `netAmountMonthly` | string | yes | Derived monthly net rent (`netAmount / billingCycle`). Fixed two-decimal string. |
| `grossAmountMonthly` | string | yes | Derived monthly gross rent (`grossAmount / billingCycle`). Fixed two-decimal string. |
| `billingCycle` | integer: `1` \| `3` \| `6` \| `12` | yes | Months per billing cycle. |
| `hasVat` | boolean | yes |  |
| `referenceInterestRate` | [ReferenceInterestRateResponse](#referenceinterestrateresponse) · nullable |  | Reference interest rate this rent is based on, or null. |
| `indexBase` | [IndexBaseResponse](#indexbaseresponse) · nullable |  | Inflation-index baseline this rent is anchored to, or null. |
| `inflationIndex` | [InflationIndexResponse](#inflationindexresponse) · nullable |  | Inflation index this rent is based on, or null. |
| `lastCostSettlement` | string · nullable |  | Last ancillary-cost settlement month, as `YYYY-MM`; null if never settled. |
| `ancillaryExpenses` | [AncillaryExpenseResponse](#ancillaryexpenseresponse)[] | yes | Agreed ancillary-expense positions for this rent version. |

### ReferenceInterestRateResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `yearMonth` | string | yes | Month the rate is valid from, as `YYYY-MM`. |
| `rate` | string | yes | Reference interest rate as a percentage, decimal string (e.g. `"1.50"` means 1.50%). Sent as a string to preserve precision. |

### IndexBaseResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `yearMonth` | string | yes | Baseline month, as `YYYY-MM`. |

### InflationIndexResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `yearMonth` | string | yes | Month of the index figure, as `YYYY-MM`. |
| `value` | string | yes | Index figure (index points) as a decimal string. Sent as a string to preserve precision. |

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

### ContractDetailApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `rents` | [ContractRentResponse](#contractrentresponse)[] | yes | Full rent version history, ordered by `starts`. |
| `id` | integer | yes |  |
| `objectId` | integer | yes | FK to the object resource. Resolve via `getObject`. |
| `mainContractId` | integer · nullable |  | FK to the main contract when this is a sub-contract (e.g. parking, basement); null otherwise. |
| `isVacancy` | boolean | yes | True for vacancy entries (Leerstand). |
| `status` | [ContractStatus](#contractstatus) | yes |  |
| `starts` | string (date) | yes |  |
| `ends` | string (date) · nullable |  | Null = open-ended; set + not noticed = fixed-term. |
| `moveIn` | string (date) · nullable |  | Actual move-in date, if tracked. |
| `moveOut` | string (date) · nullable |  | Actual move-out date, if tracked. |
| `noticePeriodMonths` | integer | yes | Notice period in months. 0 for vacancy entries. |
| `possibleNoticeMonths` | integer[] | yes | Months (1–12) in which notice may be given. Empty for vacancy entries. |
| `firstPossibleNotice` | string (date) · nullable |  | Earliest date notice can be given; null if not set. |
| `hasVat` | boolean | yes |  |
| `qrReference` | string · nullable |  | Swiss QR-bill reference for rent payments; null if none. |
| `termination` | [ContractTerminationResponse](#contractterminationresponse) · nullable |  | Notice details; set only once notice has been given. |
| `deposit` | [ContractDepositResponse](#contractdepositresponse) · nullable |  | Security deposit; null when no deposit is recorded. |
| `persons` | [RelatedPersonResponse](#relatedpersonresponse)[] | yes | Persons linked to the contract (tenants and residents merged). |
| `currentRent` | [ContractRentResponse](#contractrentresponse) · nullable |  | The rent version effective today; null if none is effective. |
