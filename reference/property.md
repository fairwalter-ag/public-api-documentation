# Property

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/{mode}/properties` | `listProperties` | List properties |
| GET | `/public-api/v1/{mode}/properties/{id}/files` | `listPropertyFiles` | List files of a property |
| GET | `/public-api/v1/{mode}/properties/{id}` | `getProperty` | Get property details |

## GET /public-api/v1/{mode}/properties

**List properties** — `listProperties`

Returns properties under reachable mandates for the selected `{mode}`.

Properties sit one level below mandates in the resource hierarchy (`Mandate → Property → Building → Object`). Each property carries a `mandateId` FK that resolves via `getMandate`.

Scope with `filter[mandateId]` to restrict to a single mandate. Use `q` for free-text search across name, ZIP and city.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name, postcode, city. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[mandateId]` | query | integer |  | Restricts results to records belonging to the given mandate id. |
| `sort` | query | string: `id` \| `-id` \| `name` \| `-name` \| `city` \| `-city` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name, city. |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**List capabilities**

- **Searchable (`q`):** name, postcode, city
- **Filterable:** `filter[mandateId]`
- **Sortable:** `id`, `name`, `city` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [PropertyApiResponse](#propertyapiresponse).

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
      "mandateId": 1,
      "managerId": 42,
      "name": "string",
      "postcode": "string",
      "city": "string",
      "canton": "ZH",
      "country": "AF",
      "egrid": "CH123456789012",
      "isActive": true
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

## GET /public-api/v1/{mode}/properties/{id}/files

**List files of a property** — `listPropertyFiles`

Returns the files attached to a property. Visible exactly when the property itself is
visible via `getProperty`; orphaned files and files of other customers never appear.

Use `getFile` for a file's owners and `downloadFile` for its binary.

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

## GET /public-api/v1/{mode}/properties/{id}

**Get property details** — `getProperty`

Returns a single property by id, including its address, canton, EGRID, and active flag.

Use `listProperties` for discovery when the id is unknown. The `mandateId` FK links back to `getMandate`; `getBuilding` / `listBuildings` traverse down to buildings under this property.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |
| `mode` | path | string: `rent` \| `condo` | yes | Business domain for the request. Use `rent` for rental-management data, `condo` for condominium-ownership data. The selected mode constrains every related resource. |

**Response** — `200` returns [PropertyApiResponse](#propertyapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Property not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "mandateId": 1,
  "managerId": 42,
  "name": "string",
  "postcode": "string",
  "city": "string",
  "canton": "ZH",
  "country": "AF",
  "egrid": "CH123456789012",
  "isActive": true
}
```

## Schemas

### PropertyApiResponse

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | integer | yes |  |
| `mandateId` | integer | yes | FK to the parent mandate. Resolve via `getMandate`. |
| `managerId` | integer | yes | Id of the user managing this property inside Fairwalter. Not resolvable via the Public API — exposed for cross-referencing with other systems. |
| `name` | string | yes |  |
| `postcode` | string | yes |  |
| `city` | string | yes |  |
| `canton` | string · nullable |  | Swiss canton abbreviation (two letters, e.g. "ZH", "BE"). Null when the property is outside Switzerland or the canton is unknown. |
| `country` | [Country](#country) | yes |  |
| `egrid` | string · nullable |  | Swiss federal property identifier (EGRID), 14-character alphanumeric code assigned by the Federal Office of Topography. Null when no EGRID is on record. |
| `isActive` | boolean | yes | Whether the property is currently active. Inactive properties are retained for historical reporting but no new contracts are signed against them. |

### Country

String enum, 249 values.

`AF`, `AX`, `AL`, `DZ`, `AS`, `AD`, `AO`, `AI`, `AQ`, `AG`, `AR`, `AM`, `AW`, `AU`, `AT`, `AZ`, `BS`, `BH`, `BD`, `BB`, `BY`, `BE`, `BZ`, `BJ`, `BM`, `BT`, `BO`, `BQ`, `BA`, `BW`, `BV`, `BR`, `IO`, `BN`, `BG`, `BF`, `BI`, `KH`, `CM`, `CA`, `CV`, `KY`, `CF`, `TD`, `CL`, `CN`, `CX`, `CC`, `CO`, `KM`, `CG`, `CD`, `CK`, `CR`, `CI`, `HR`, `CU`, `CW`, `CY`, `CZ`, `DK`, `DJ`, `DM`, `DO`, `EC`, `EG`, `SV`, `GQ`, `ER`, `EE`, `ET`, `FK`, `FO`, `FJ`, `FI`, `FR`, `GF`, `PF`, `TF`, `GA`, `GM`, `GE`, `DE`, `GH`, `GI`, `GR`, `GL`, `GD`, `GP`, `GU`, `GT`, `GG`, `GN`, `GW`, `GY`, `HT`, `HM`, `VA`, `HN`, `HK`, `HU`, `IS`, `IN`, `ID`, `IR`, `IQ`, `IE`, `IM`, `IL`, `IT`, `JM`, `JP`, `JE`, `JO`, `KZ`, `KE`, `KI`, `KP`, `KR`, `XK`, `KW`, `KG`, `LA`, `LV`, `LB`, `LS`, `LR`, `LY`, `LI`, `LT`, `LU`, `MO`, `MK`, `MG`, `MW`, `MY`, `MV`, `ML`, `MT`, `MH`, `MQ`, `MR`, `MU`, `YT`, `MX`, `FM`, `MD`, `MC`, `MN`, `ME`, `MS`, `MA`, `MZ`, `MM`, `NA`, `NR`, `NP`, `NL`, `NC`, `NZ`, `NI`, `NE`, `NG`, `NU`, `NF`, `MP`, `NO`, `OM`, `PK`, `PW`, `PS`, `PA`, `PG`, `PY`, `PE`, `PH`, `PN`, `PL`, `PT`, `PR`, `QA`, `RE`, `RO`, `RU`, `RW`, `BL`, `SH`, `KN`, `LC`, `MF`, `PM`, `VC`, `WS`, `SM`, `ST`, `SA`, `SN`, `RS`, `SC`, `SL`, `SG`, `SX`, `SK`, `SI`, `SB`, `SO`, `ZA`, `GS`, `SS`, `ES`, `LK`, `SD`, `SR`, `SZ`, `SE`, `CH`, `SY`, `TW`, `TJ`, `TZ`, `TH`, `TL`, `TG`, `TK`, `TO`, `TT`, `TN`, `TR`, `TM`, `TC`, `TV`, `UG`, `UA`, `AE`, `GB`, `US`, `UM`, `UY`, `UZ`, `VU`, `VE`, `VN`, `VG`, `VI`, `WF`, `EH`, `YE`, `ZM`, `ZW`

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
