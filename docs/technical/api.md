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

## Request and Response Formats

### Content Types
- `application/json`: Primary content type
- `application/xml`: Optional XML support
- `multipart/form-data`: File uploads

### Standard Response Structure
```json
{
  "status": "success|error",
  "data": {},
  "error": {
    "code": "error_code",
    "message": "Detailed error description"
  },
  "metadata": {
    "timestamp": "ISO8601 timestamp",
    "request_id": "unique_request_identifier"
  }
}
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation errors
- `500 Internal Server Error`: Server-side errors

### Error Codes
```json
{
  "INVALID_PARAMETERS": "Request parameters are invalid",
  "AUTHENTICATION_REQUIRED": "Authentication token missing",
  "INSUFFICIENT_PERMISSIONS": "User lacks required permissions",
  "RESOURCE_NOT_FOUND": "Requested resource does not exist",
  "VALIDATION_ERROR": "Data validation failed"
}
```

## Rate Limiting

### Request Limits
- `DEFAULT`: 100 requests/minute
- `AUTHENTICATED`: 500 requests/minute
- `ADMIN`: Unlimited requests

### Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 75
X-RateLimit-Reset: 1609459200
```

## API Versioning

### Versioning Strategy
- URL-based versioning
- Current version: `v1`
- Backward compatibility maintained

### Version Endpoints
```http
/api/v1/agents/
/api/v1/events/
/api/v1/resources/
```

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
