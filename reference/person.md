# Person

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/persons` | `listPersons` | List persons |
| GET | `/public-api/v1/persons/{id}/files` | `listPersonFiles` | List files of a person |
| GET | `/public-api/v1/persons/{id}` | `getPerson` | Get person details |

## GET /public-api/v1/persons

**List persons** — `listPersons`

Returns persons the calling token can reach. An all-mandate token sees every
person of the customer, including plain contacts with no contract link; a
mandate-restricted token sees only persons reachable via a contract party or
resident link within those mandates. Each row carries derived `roles` and the
current `address`; the address history is available on the detail endpoint.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name1, name2, email, phone. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[role]` | query | string: `tenant` \| `owner` \| `resident` |  | Restricts results to records matching the given role. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `sort` | query | string: `id` \| `-id` \| `name1` \| `-name1` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name1. |

**List capabilities**

- **Searchable (`q`):** name1, name2, email, phone
- **Filterable:** `filter[role]` (`tenant`, `owner`, `resident`), `filter[mandateId]`, `filter[propertyId]`
- **Sortable:** `id`, `name1` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [PersonApiResponse](#personapiresponse).

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
      "contactType": "natural",
      "name1": "Muster",
      "name2": "Hans",
      "salutation": "unspecified",
      "email": "string",
      "phone": "string",
      "secondEmail": "string",
      "secondPhone": "string",
      "website": "string",
      "communicationChannel": "email",
      "dateOfBirth": "1980-05-12",
      "maritalStatus": "married",
      "placeOfOrigin": "Luzern",
      "contactPersonName": "string",
      "secondContactPersonName": "string",
      "roles": [
        "tenant"
      ],
      "address": {
        "street": "string",
        "houseNumber": "string",
        "postcode": "string",
        "city": "string",
        "country": "string"
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

## GET /public-api/v1/persons/{id}/files

**List files of a person** — `listPersonFiles`

Returns the files attached to a person. Visible exactly when the person itself is visible via `getPerson`.

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

## GET /public-api/v1/persons/{id}

**Get person details** — `getPerson`

Returns a single person by id, including derived `roles`, the current
`address`, and the full `addresses` history (with scheduled future changes).
Returns 404 when the person does not exist or is outside the token's scope.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [PersonDetailApiResponse](#persondetailapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Person not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "addresses": [
    {
      "street": "string",
      "houseNumber": "string",
      "postcode": "string",
      "city": "string",
      "country": "string",
      "effectiveFrom": "2022-07-01"
    }
  ],
  "id": 1,
  "contactType": "natural",
  "name1": "Muster",
  "name2": "Hans",
  "salutation": "unspecified",
  "email": "string",
  "phone": "string",
  "secondEmail": "string",
  "secondPhone": "string",
  "website": "string",
  "communicationChannel": "email",
  "dateOfBirth": "1980-05-12",
  "maritalStatus": "married",
  "placeOfOrigin": "Luzern",
  "contactPersonName": "string",
  "secondContactPersonName": "string",
  "roles": [
    "tenant"
  ],
  "address": {
    "street": "string",
    "houseNumber": "string",
    "postcode": "string",
    "city": "string",
    "country": "string"
  }
}
```

## Schemas

### PersonApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `contactType` | [ContactType](#contacttype) | yes |  |
| `name1` | string | yes | Family name (natural) or company name (legal). |
| `name2` | string · nullable |  | Given name(s) (natural) or name addition (legal). Null when not applicable. |
| `salutation` | [Salutation](#salutation) | yes |  |
| `email` | string · nullable |  |  |
| `phone` | string · nullable |  |  |
| `secondEmail` | string · nullable |  |  |
| `secondPhone` | string · nullable |  |  |
| `website` | string · nullable |  |  |
| `communicationChannel` | [CommunicationChannel](#communicationchannel) | yes |  |
| `dateOfBirth` | string (date) · nullable |  | Date of birth (natural persons only). Null otherwise. |
| `maritalStatus` | [MaritalStatus](#maritalstatus) · nullable |  | Marital status (natural persons only). Values: `married`, `single`, `divorced`, `widowed`. Null otherwise. |
| `placeOfOrigin` | string · nullable |  | Swiss place of origin / Heimatort (natural persons only). Null otherwise. |
| `contactPersonName` | string · nullable |  | Contact person (legal persons only). Null otherwise. |
| `secondContactPersonName` | string · nullable |  | Second contact person (legal persons only). Null otherwise. |
| `roles` | string: `tenant` \| `owner` \| `resident`[] | yes | Roles derived from the person's active contract relations. Empty when the person has no active tenancy, ownership, or residency. |
| `address` | [AddressDto](#addressdto) · nullable |  | Current effective address, or null when the person has no address on record. |

### ContactType

String enum, 2 values.

`natural`, `legal`

### Salutation

String enum, 3 values.

`unspecified`, `mrs`, `mr`

### CommunicationChannel

String enum, 2 values.

`email`, `letter`

### MaritalStatus

String enum, 4 values.

`married`, `single`, `divorced`, `widowed`

### AddressDto

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `street` | string | yes |  |
| `houseNumber` | string | yes |  |
| `postcode` | string | yes |  |
| `city` | string | yes |  |
| `country` | string | yes |  |

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

### PersonDetailApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `addresses` | [PersonAddressDto](#personaddressdto)[] | yes | Full address history, oldest first; the baseline address (no `effectiveFrom`) leads. Includes scheduled future address changes. |
| `id` | integer | yes |  |
| `contactType` | [ContactType](#contacttype) | yes |  |
| `name1` | string | yes | Family name (natural) or company name (legal). |
| `name2` | string · nullable |  | Given name(s) (natural) or name addition (legal). Null when not applicable. |
| `salutation` | [Salutation](#salutation) | yes |  |
| `email` | string · nullable |  |  |
| `phone` | string · nullable |  |  |
| `secondEmail` | string · nullable |  |  |
| `secondPhone` | string · nullable |  |  |
| `website` | string · nullable |  |  |
| `communicationChannel` | [CommunicationChannel](#communicationchannel) | yes |  |
| `dateOfBirth` | string (date) · nullable |  | Date of birth (natural persons only). Null otherwise. |
| `maritalStatus` | [MaritalStatus](#maritalstatus) · nullable |  | Marital status (natural persons only). Values: `married`, `single`, `divorced`, `widowed`. Null otherwise. |
| `placeOfOrigin` | string · nullable |  | Swiss place of origin / Heimatort (natural persons only). Null otherwise. |
| `contactPersonName` | string · nullable |  | Contact person (legal persons only). Null otherwise. |
| `secondContactPersonName` | string · nullable |  | Second contact person (legal persons only). Null otherwise. |
| `roles` | string: `tenant` \| `owner` \| `resident`[] | yes | Roles derived from the person's active contract relations. Empty when the person has no active tenancy, ownership, or residency. |
| `address` | [AddressDto](#addressdto) · nullable |  | Current effective address, or null when the person has no address on record. |

### PersonAddressDto

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `street` | string | yes |  |
| `houseNumber` | string | yes |  |
| `postcode` | string | yes |  |
| `city` | string | yes |  |
| `country` | string | yes |  |
| `effectiveFrom` | string (date) · nullable |  | Day this address became effective. Null for the baseline address with no recorded start. |
