# Damage

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/damages` | `listDamages` | List damages |
| GET | `/public-api/v1/{mode}/damages/{id}/files` | `listDamageFiles` | List files of a damage |
| GET | `/public-api/v1/{mode}/damages/{id}` | `getDamage` | Get damage details |

## GET /public-api/v1/{mode}/damages

**List damages** — `listDamages`

Returns the damages (repair tickets) reachable for the selected `{mode}`. Each
damage is anchored to a building (`buildingId`) and optionally pinned to an object
(`objectId`), an asset (`assetId`), and an assigned contractor (`serviceProviderId`).

Scope with `filter[status]`, `filter[serviceProviderId]`, `filter[objectId]`,
`filter[buildingId]`, or `filter[propertyId]`; use `q` to search across title and description.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: title, description. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[status]` | query | string: `new` \| `offer_requested` \| `order_placed` \| `invoice_pending` \| `correction_needed` \| `finished` |  | Restricts results to records matching the given status. |
| `filter[serviceProviderId]` | query | integer |  | Restricts results to records belonging to the given serviceProvider id. |
| `filter[objectId]` | query | integer |  | Restricts results to records belonging to the given object id. |
| `filter[buildingId]` | query | integer |  | Restricts results to records belonging to the given building id. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `sort` | query | string: `id` \| `-id` \| `dateOfDamage` \| `-dateOfDamage` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, dateOfDamage. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** title, description
- **Filterable:** `filter[status]` (`new`, `offer_requested`, `order_placed`, `invoice_pending`, `correction_needed`, `finished`), `filter[serviceProviderId]`, `filter[objectId]`, `filter[buildingId]`, `filter[propertyId]`
- **Sortable:** `id`, `dateOfDamage` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [DamageApiResponse](#damageapiresponse).

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
      "buildingId": 12,
      "propertyId": 7,
      "objectId": 789,
      "assetId": 4021,
      "serviceProviderId": 55,
      "status": "new",
      "title": "Geschirrspüler undicht",
      "description": "string",
      "cause": "string",
      "dateOfDamage": "2026-05-28",
      "estimatedCost": "350.00"
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

## GET /public-api/v1/{mode}/damages/{id}/files

**List files of a damage** — `listDamageFiles`

Returns the files attached to a damage. Visible exactly when the damage is visible via `getDamage`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[category]` | query | string enum (18 values) |  | Restricts results to records matching the given category. One of: `finance`, `contracts`, `correspondence`, `protocol`, `personal_information`, `state_documents`, `repairs_and_damage`, `pictures`, `various`, `rules_and_regulations`, `locking_schedule`, `plan`, `service_contracts`, `insurance`, `offer`, `condominium_protocol`, `condominium_meeting`, `profile_image`. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `uploadedAt` \| `-uploadedAt` \| `fileSize` \| `-fileSize` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, uploadedAt, fileSize. |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

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

## GET /public-api/v1/{mode}/damages/{id}

**Get damage details** — `getDamage`

Returns a single damage by id, including its status, title, description, cause,
date, and estimated cost, plus the building/object/asset/service-provider it relates to.

Use `listDamages` for discovery when the id is unknown.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [DamageApiResponse](#damageapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Damage not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "buildingId": 12,
  "propertyId": 7,
  "objectId": 789,
  "assetId": 4021,
  "serviceProviderId": 55,
  "status": "new",
  "title": "Geschirrspüler undicht",
  "description": "string",
  "cause": "string",
  "dateOfDamage": "2026-05-28",
  "estimatedCost": "350.00"
}
```

## Schemas

### DamageApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `buildingId` | integer | yes | FK to the building the damage is anchored to (always set). Resolve via `getBuilding`. |
| `propertyId` | integer | yes | FK to the property, derived via the building. Resolve via `getProperty`. |
| `objectId` | integer | yes | FK to the rental object the damage concerns (always set). Resolve via `getObject`. |
| `assetId` | integer · nullable |  | FK to the asset, set when the damage concerns a specific asset. Null otherwise. |
| `serviceProviderId` | integer · nullable |  | FK to the assigned repair contractor. Null when none assigned. Resolve via `getServiceProvider`. |
| `status` | [DamageStatus](#damagestatus) | yes |  |
| `title` | string | yes | Short description / title of the damage. |
| `description` | string · nullable |  | Detailed damage description. Null when not recorded. |
| `cause` | string · nullable |  | Cause / reason for the damage. Null when not recorded. |
| `dateOfDamage` | string (date) · nullable |  | Date the damage occurred. Null when not recorded. |
| `estimatedCost` | string · nullable |  | Estimated repair cost as a fixed two-decimal string. Sent as a string — never a float — to preserve precision. Null when not recorded. |

### DamageStatus

String enum, 6 values.

`new`, `offer_requested`, `order_placed`, `invoice_pending`, `correction_needed`, `finished`

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
