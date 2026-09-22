# User

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/users` | `listUsers` | List users |
| GET | `/public-api/v1/users/{id}/files` | `listUserFiles` | List files of a user |
| GET | `/public-api/v1/users/{id}` | `getUser` | Get user details |

## GET /public-api/v1/users

**List users** — `listUsers`

Returns the property-management staff accounts the calling token can reach.

Users are referenced by `managerId` on properties. A token with access to all mandates sees every (non-support) user of the customer; a token restricted to specific mandates sees only users assigned to an in-scope mandate, plus managers of in-scope properties.

Use `q` for free-text search across first name, last name, and email. Narrow with `filter[status]`, `filter[mandateId]`, or `filter[role]`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `filter[status]` | query | string: `invited` \| `active` \| `disabled` |  | Restricts results to users with the given lifecycle status. |
| `filter[mandateId]` | query | integer |  | Restricts results to users assigned to the given mandate id. |
| `filter[role]` | query | string: `account_owner` \| `manager` |  | Restricts results by system role. `manager` matches every user; `account_owner` matches account owners only. |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: firstName, lastName, email. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `sort` | query | string: `id` \| `-id` \| `lastName` \| `-lastName` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, lastName. |

**List capabilities**

- **Searchable (`q`):** firstName, lastName, email
- **Filterable:** `filter[status]` (`invited`, `active`, `disabled`), `filter[mandateId]`, `filter[role]` (`account_owner`, `manager`)
- **Sortable:** `id`, `lastName` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [UserApiResponse](#userapiresponse).

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
      "salutation": "unspecified",
      "firstName": "string",
      "lastName": "string",
      "email": "string",
      "phone": "+41 79 555 11 22",
      "jobTitle": "string",
      "language": "de",
      "status": "invited",
      "roles": [
        "manager"
      ],
      "mandateIds": [
        1
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

## GET /public-api/v1/users/{id}/files

**List files of a user** — `listUserFiles`

Returns the files attached to a user. The only `category` a user file can have is
`profile_image`. Visible exactly when the user itself is visible via `getUser`.

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

## GET /public-api/v1/users/{id}

**Get user details** — `getUser`

Returns a single user by id, including salutation, contact details, preferred language, lifecycle status, system roles, and assigned mandate ids.

Use `listUsers` for discovery when the id is unknown. A `managerId` reference on a property resolves here. With a restricted token a referenced user can fall outside the visible set; consumers must tolerate an unresolvable reference (`404`).

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [UserApiResponse](#userapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | User not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "salutation": "unspecified",
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phone": "+41 79 555 11 22",
  "jobTitle": "string",
  "language": "de",
  "status": "invited",
  "roles": [
    "manager"
  ],
  "mandateIds": [
    1
  ]
}
```

## Schemas

### UserApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `salutation` | [Salutation](#salutation) | yes |  |
| `firstName` | string | yes |  |
| `lastName` | string | yes |  |
| `email` | string | yes |  |
| `phone` | string · nullable |  | Mobile phone number. Null when not set. |
| `jobTitle` | string · nullable |  |  |
| `language` | [UserLanguage](#userlanguage) | yes |  |
| `status` | [UserStatus](#userstatus) | yes |  |
| `roles` | string: `manager` \| `account_owner`[] | yes | System roles. Every user is `manager`; account owners additionally hold `account_owner`. |
| `mandateIds` | integer[] | yes | Ids of the mandates this user is assigned to. |

### Salutation

String enum, 3 values.

`unspecified`, `mrs`, `mr`

### UserLanguage

String enum, 4 values.

`de`, `en`, `fr`, `it`

### UserStatus

String enum, 3 values.

`invited`, `active`, `disabled`

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
