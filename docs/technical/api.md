# API Reference

[← Back to Main Documentation](../README.md)

## Table of Contents
1. [Authentication](#authentication)
2. [Equipment API](#equipment-api)
   - [Log Equipment Use](#log-equipment-use)
   - [Process Payment](#process-payment)
3. [Resource API](#resource-api)
   - [Create Resource](#create-resource)
   - [Transfer Resource](#transfer-resource)
4. [Board API](#board-api)
   - [Create Workflow](#create-workflow)
   - [Update Stage](#update-stage)
5. [Error Responses](#error-responses)
6. [Rate Limiting](#rate-limiting)

## Authentication

[↑ Back to Top](#table-of-contents)

```http
POST /api/auth/token/
Content-Type: application/json

{
    "username": "user",
    "password": "pass"
}
```

Response:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

## Equipment API

[↑ Back to Top](#table-of-contents)

### Log Equipment Use

```http
POST /api/equipment/log-use/
Authorization: Token <token>
Content-Type: application/json

{
    "equipment_id": "123",
    "hours": 2.5,
    "technician_id": "456",
    "notes": "Regular use"
}
```

### Process Payment

```http
POST /api/equipment/payment/
Authorization: Token <token>
Content-Type: application/json

{
    "use_id": "789",
    "payment_method": "cash",
    "amount": 50.00
}
```

## Resource API

[↑ Back to Top](#table-of-contents)

### Create Resource

```http
POST /api/resources/
Authorization: Token <token>
Content-Type: application/json

{
    "type": "herb",
    "quantity": 100,
    "unit": "kg",
    "location": "warehouse-1"
}
```

### Transfer Resource

```http
POST /api/resources/transfer/
Authorization: Token <token>
Content-Type: application/json

{
    "resource_id": "123",
    "to_location": "warehouse-2",
    "quantity": 50
}
```

## Board API

[↑ Back to Top](#table-of-contents)

### Create Workflow

```http
POST /api/boards/workflow/
Authorization: Token <token>
Content-Type: application/json

{
    "name": "Herb Processing",
    "stages": ["drying", "packaging", "storage"]
}
```

### Update Stage

```http
PUT /api/boards/stage/{stage_id}/
Authorization: Token <token>
Content-Type: application/json

{
    "status": "completed",
    "notes": "Process finished"
}
```

## Error Responses

[↑ Back to Top](#table-of-contents)

### 401 Unauthorized
```json
{
    "detail": "Invalid token"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 400 Bad Request
```json
{
    "error": "Invalid input",
    "details": {
        "field": ["Error message"]
    }
}
```

## Rate Limiting

[↑ Back to Top](#table-of-contents)

- 1000 requests per hour per user
- Rate limit headers included in response:
  ```
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1609459200
  ```
