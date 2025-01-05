# API Documentation

VerdunNRP provides a comprehensive RESTful API for interacting with the value network system.

## Authentication and Authorization

### Authentication Methods

1. **Token Authentication**
   - All API endpoints require authentication
   - Use token-based authentication in request headers
   ```http
   Authorization: Token your-api-token
   ```

2. **OAuth 2.0 Support**
   - Supports OAuth 2.0 for third-party integrations
   - Supports authorization code, client credentials, and refresh token flows

3. **JWT (JSON Web Tokens)**
   - Optional JWT-based authentication
   - Supports stateless authentication
   ```http
   Authorization: Bearer your-jwt-token
   ```

### Authorization Levels

1. **User Roles**
   - `ADMIN`: Full system access
   - `MANAGER`: Modify resources, create events
   - `CONTRIBUTOR`: Create and view limited resources
   - `VIEWER`: Read-only access

2. **Permissions**
   - Role-based access control (RBAC)
   - Granular permissions for each endpoint
   - Context-based access restrictions

### API Key Management

1. **API Key Generation**
   ```http
   POST /api/keys/generate/
   ```
   Response:
   ```json
   {
     "api_key": "unique-api-key",
     "created_at": "timestamp",
     "expires_at": "timestamp"
   }
   ```

2. **API Key Rotation**
   ```http
   POST /api/keys/rotate/
   ```

## Request/Response Formats

### Request Format
All requests should use JSON format for the request body:
```http
Content-Type: application/json
Accept: application/json
```

### Response Format
All responses follow a standard format:
```json
{
    "status": "success|error",
    "data": {
        // Response data here
    },
    "message": "Optional message",
    "metadata": {
        "version": "1.0",
        "timestamp": "ISO-8601 timestamp"
    }
}
```

## Error Handling

### Error Response Format
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": {
            // Additional error details
        }
    }
}
```

### Common Error Codes
- `AUTH_001`: Authentication failed
- `AUTH_002`: Token expired
- `PERM_001`: Insufficient permissions
- `VAL_001`: Validation error
- `RATE_001`: Rate limit exceeded
- `SYS_001`: System error

## Rate Limiting

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

### Limits by Endpoint Type
- GET requests: 1000 requests per hour
- POST/PUT/DELETE requests: 100 requests per hour
- Bulk operations: 10 requests per hour

### Rate Limit Response (429 Too Many Requests)
```json
{
    "status": "error",
    "error": {
        "code": "RATE_001",
        "message": "Rate limit exceeded",
        "details": {
            "reset_at": "2025-01-05T01:00:00Z",
            "retry_after": 3600
        }
    }
}
```

## API Versioning

### Version Header
Include the API version in the request header:
```http
Accept: application/json; version=1.0
```

### Version Path Prefix
Alternatively, use version in the URL path:
```http
https://api.verdunnrp.org/v1/resources
```

### Version Support
- v1.0: Current stable version (Fully supported)
- v0.9: Legacy version (Deprecated, sunset date: 2025-06-01)
- v1.1-beta: Beta version (Preview features)

### Version Lifecycle
1. Beta Release
   - Preview of new features
   - Subject to change
   - No SLA guarantees

2. Stable Release
   - Full production support
   - Backwards compatible changes only
   - Security updates

3. Deprecation
   - 6 months notice before EOL
   - Security fixes only
   - Migration guides provided

## API Endpoints

### Agents

#### List Agents
```http
GET /api/agents/
```

Query Parameters:
- `context`: Filter by context agent (e.g., ?context=project-name)
- `type`: Filter by agent type

Response:
```json
{
    "count": integer,
    "next": string (url),
    "previous": string (url),
    "results": [
        {
            "api_url": string,
            "url": string,
            "name": string,
            "nick": string,
            "slug": string,
            "agent_type": string,
            "address": string,
            "email": string,
            "projects": [
                {
                    "api_url": string,
                    "url": string,
                    "name": string,
                    "slug": string,
                    "agent_type": string,
                    "address": string
                }
            ]
        }
    ]
}
```

#### Get Agent
```http
GET /api/agents/{id}/
```

#### Create Agent
```http
POST /api/agents/
```

Required fields:
```json
{
    "name": string,
    "nick": string,
    "agent_type": string,
    "url": string,
    "address": string,
    "email": string
}
```

### Economic Events

#### List Events
```http
GET /api/events/
```

Query Parameters:
- `context`: Filter by context
- `event-type`: Filter by event type
- `provider`: Filter by providing agent
- `receiver`: Filter by receiving agent

Response:
```json
{
    "count": integer,
    "next": string (url),
    "previous": string (url),
    "results": [
        {
            "api_url": string,
            "event_date": string (date),
            "event_type": string,
            "from_agent": string,
            "to_agent": string,
            "context_agent": string,
            "resource_type": string,
            "resource": string,
            "description": string,
            "quantity": number,
            "unit_of_quantity": string,
            "is_contribution": boolean
        }
    ]
}
```

#### Create Event
```http
POST /api/events/
```

Required fields:
```json
{
    "event_date": string (date),
    "event_type": string,
    "from_agent": string,
    "to_agent": string,
    "resource_type": string,
    "quantity": number,
    "unit_of_quantity": string
}
```

### Contributions

#### List Contributions
```http
GET /api/contributions/
```

Query Parameters:
- `context`: Filter by context
- `event-type`: Filter by event type (e.g., ?event-type=work)

Response:
```json
{
    "count": integer,
    "results": [
        {
            "api_url": string,
            "event_date": string (date),
            "event_type": string,
            "from_agent": string,
            "to_agent": string,
            "context_agent": string,
            "resource_type": string,
            "description": string,
            "quantity": number,
            "unit_of_quantity": string,
            "is_contribution": boolean
        }
    ]
}
```

### Resources

#### List Resources
```http
GET /api/resources/
```

Query Parameters:
- `type`: Filter by resource type
- `state`: Filter by resource state

Response:
```json
{
    "count": integer,
    "results": [
        {
            "api_url": string,
            "resource_type": string,
            "identifier": string,
            "notes": string,
            "quantity": number,
            "unit_of_quantity": string
        }
    ]
}
```

### Get Resource
```http
GET /api/resources/{id}/
```

## Data Models

### Agent
```json
{
  "id": "string",
  "name": "string",
  "nick": "string",
  "agent_type": "string",
  "description": "string",
  "url": "string",
  "email": "string"
}
```

### Economic Event
```json
{
  "id": "string",
  "event_type": "string",
  "provider": "string",
  "receiver": "string",
  "resource_type": "string",
  "quantity": "number",
  "unit": "string",
  "date": "string"
}
```

### Resource
```json
{
  "id": "string",
  "resource_type": "string",
  "quantity": "number",
  "unit": "string",
  "state": "string",
  "location": "string"
}
```

## Linked Data

The API supports JSON-LD format for semantic data integration:

```http
GET /api/agents.jsonld
```

Returns agents in JSON-LD format with vocabularies based on:
- FOAF
- Schema.org
- Value Flows vocabulary

## Changelog

### v1.0.0
- Initial API release
- Core endpoints for agents, events, resources

### v1.1.0
- Added webhook support
- Improved authentication
- Enhanced error handling

## Deprecation Policy

- 6-month notice for major API changes
- Maintain backward compatibility
- Provide migration guides

## Documentation and Support

1. **Swagger/OpenAPI**
   - Interactive API documentation
   - `/api/docs/` endpoint

2. **Client Libraries**
   - Python SDK
   - JavaScript/TypeScript client
   - Postman collection

3. **Support Channels**
   - API documentation
   - Community forums
   - Support email
   - GitHub issues

## Security Best Practices

1. **HTTPS Only**
   - All API endpoints require HTTPS
   - TLS 1.2+ encryption
   - HSTS (HTTP Strict Transport Security)

2. **Input Validation**
   - Server-side validation for all inputs
   - Sanitize and validate all parameters
   - Prevent SQL injection and XSS attacks

3. **Logging and Monitoring**
   - Log all API access attempts
   - Monitor for suspicious activities
   - Implement IP-based blocking

## Integration Guidelines

### Third-Party Integrations
- Provide comprehensive webhook support
- Support for event-driven architectures
- Flexible data transformation

### Webhook Endpoints
```http
POST /api/webhooks/events/
POST /api/webhooks/resources/
```

## Performance Considerations

1. **Caching**
   - Implement Redis-based caching
   - Cache-Control headers
   - Conditional GET requests

2. **Pagination**
   - Default page size: 50 items
   - Maximum page size: 500 items
   ```http
   GET /api/agents/?page=2&page_size=100
   ```

3. **Compression**
   - Support gzip compression
   - Reduce payload size
   ```http
   Accept-Encoding: gzip
   ```
