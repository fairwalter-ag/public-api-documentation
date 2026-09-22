# Service Provider

| Method | Path | Operation | Summary |
| --- | --- | --- | --- |
| GET | `/public-api/v1/service-providers` | `listServiceProviders` | List service providers |
| GET | `/public-api/v1/service-providers/{id}` | `getServiceProvider` | Get service provider details |

## GET /public-api/v1/service-providers

**List service providers** — `listServiceProviders`

Returns the service providers (contractors) the calling token can reach. An
all-mandate token sees every provider of the customer, including ones with no
property assignment; a mandate-restricted token sees only providers assigned to
a property within those mandates. Filter with `filter[propertyId]` or
`filter[domain]`; search across name and email with `q`.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | integer |  | Maximum number of items to return. limit=0 is accepted and silently treated as 1. Values above the maximum are capped to it. Default `30`. Maximum `100`. |
| `offset` | query | integer |  | Number of items to skip. Use with limit for pagination. Default `0`. |
| `q` | query | string |  | Free-text search across: name1, name2, email. Case-insensitive partial match; every word must match one of these fields (so "Peter Berger" matches first and last name in separate fields). Combine with filter[...] keys to narrow further. |
| `filter[propertyId]` | query | integer |  | Restricts results to records belonging to the given property id. |
| `filter[domain]` | query | string |  | Restricts results to records matching the given domain. |
| `sort` | query | string: `id` \| `-id` \| `name1` \| `-name1` |  | Sort field. Prefix with `-` for descending order (e.g. `-id`). Allowed: id, name1. |

**List capabilities**

- **Searchable (`q`):** name1, name2, email
- **Filterable:** `filter[propertyId]`, `filter[domain]`
- **Sortable:** `id`, `name1` (prefix `-` for descending)
- **Page size:** default `30`, maximum `100`

**Response** — `200` returns a list envelope around [ServiceProviderApiResponse](#serviceproviderapiresponse).

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
      "name1": "Muster Haustechnik AG",
      "name2": "string",
      "salutation": "unspecified",
      "email": "string",
      "phone": "string",
      "secondEmail": "string",
      "secondPhone": "string",
      "website": "string",
      "contactPersonName": "string",
      "secondContactPersonName": "string",
      "domains": [
        "Sanitär",
        "Heizung"
      ],
      "propertyIds": [
        7,
        9
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

## GET /public-api/v1/service-providers/{id}

**Get service provider details** — `getServiceProvider`

Returns a single service provider by id, including the trades it covers
(`domains`), the `propertyIds` it is assigned to, and its postal address.
Returns 404 when the provider does not exist or is outside the token's scope.

| Parameter | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `id` | path | integer | yes |  |

**Response** — `200` returns [ServiceProviderApiResponse](#serviceproviderapiresponse).

| Status | Description |
| --- | --- |
| `200` | OK |
| `401` | Missing or invalid token |
| `403` | Token cannot access this resource |
| `404` | Service provider not found |
| `429` | Rate limit exceeded |

**Example response**

```json
{
  "id": 1,
  "contactType": "natural",
  "name1": "Muster Haustechnik AG",
  "name2": "string",
  "salutation": "unspecified",
  "email": "string",
  "phone": "string",
  "secondEmail": "string",
  "secondPhone": "string",
  "website": "string",
  "contactPersonName": "string",
  "secondContactPersonName": "string",
  "domains": [
    "Sanitär",
    "Heizung"
  ],
  "propertyIds": [
    7,
    9
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

### ServiceProviderApiResponse

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
| `contactPersonName` | string · nullable |  | Primary contact person at the provider. Null when none on record. |
| `secondContactPersonName` | string · nullable |  | Second contact person at the provider. Null when none on record. |
| `domains` | string[] | yes | Trades the provider covers, as customer-defined free-text labels. |
| `propertyIds` | integer[] | yes | Ids of the properties this provider is assigned to. Resolve via `getProperty`. |
| `address` | [AddressDto](#addressdto) | yes |  |

### ContactType

String enum, 2 values.

`natural`, `legal`

### Salutation

String enum, 3 values.

`unspecified`, `mrs`, `mr`

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
