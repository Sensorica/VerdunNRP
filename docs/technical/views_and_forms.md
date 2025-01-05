write# Views and Forms Documentation

## Overview

VerdunNRP uses Django's built-in views and forms framework to handle user interactions and data processing. This document outlines the key views and forms used throughout the application.

## Forms

### Account Forms

#### 1. Authentication Forms

##### `LoginForm`
- **Purpose**: Handles user authentication
- **Fields**:
  - `password`: Password field with hidden input
  - `remember`: Boolean field for session persistence
- **Validation**: Validates user credentials against database

##### `SignupForm`
- **Purpose**: New user registration
- **Fields**:
  - `username`: Username field with alphanumeric validation
  - `password`: Password field
  - `password_confirm`: Password confirmation field
  - `email`: Email field with validation
  - `code`: Optional invitation code field

##### `ChangePasswordForm`
- **Purpose**: Password modification
- **Fields**:
  - `password_current`: Current password verification
  - `password_new`: New password input
  - `password_new_confirm`: New password confirmation
- **Validation**: Verifies current password and confirms new password match

### Equipment Forms

#### 1. Equipment Management

##### `EquipmentUseForm`
- **Purpose**: Logs equipment usage
- **Fields**:
  - `event_date`: Date of equipment use
  - `from_agent`: Paying agent
  - `quantity`: Equipment hours used
  - `technician`: Optional technician assignment
  - `technician_hours`: Technician time spent

##### `PaymentForm`
- **Purpose**: Processes equipment use payments
- **Fields**:
  - `payment_method`: Choice field (Cash, Check, Paypal, Other)

### Board Forms

#### 1. Resource Management

##### `ReceiveForm`
- **Purpose**: Handles resource reception
- **Fields**:
  - `event_date`: Receipt date
  - `identifier`: New lot number
  - `from_agent`: Source agent
  - `to_agent`: Receiving agent
  - `resource_type`: Type of resource

##### `TransferFlowForm`
- **Purpose**: Manages resource transfers
- **Fields**:
  - `event_date`: Transfer date
  - `to_agent`: Recipient
  - `quantity`: Transfer amount
  - `notes`: Optional notes
  - `paid`: Payment status
  - `value`: Transfer value
  - `unit_of_value`: Value unit

## Views

### Equipment Views

#### 1. Equipment Usage

##### `log_equipment_use`
- **Purpose**: Records equipment usage events
- **URL**: `/log-equipment-use/<scenario>/<equip_resource_id>/...`
- **Methods**: POST
- **Authentication**: Required
- **Parameters**:
  - `scenario`: Usage scenario (commercial, project, fablab, etc.)
  - `equip_resource_id`: Equipment identifier
  - `context_agent_id`: Context agent
  - Additional parameters for resource types and patterns

##### `pay_equipment_use`
- **Purpose**: Processes equipment usage payments
- **URL**: `/pay-equipment-use/<scenario>/<sale_id>/...`
- **Methods**: POST
- **Authentication**: Required
- **Parameters**:
  - `scenario`: Payment scenario
  - `sale_id`: Sale identifier
  - `process_id`: Process identifier
  - Additional parameters for payment processing

### Board Views

#### 1. Resource Management

##### `dhen_board`
- **Purpose**: Manages herb drying workflow
- **URL**: `/dhen-board/<context_agent_id>`
- **Methods**: GET
- **Parameters**:
  - `context_agent_id`: Optional context agent identifier
- **Features**:
  - Resource type filtering
  - Date-based operations
  - Multiple form handling

##### `purchase_resource`
- **Purpose**: Handles resource purchasing workflow
- **URL**: `/purchase-resource/<context_agent_id>/<commitment_id>`
- **Methods**: POST
- **Authentication**: Required
- **Features**:
  - Multi-stage workflow management
  - Form validation
  - Commitment tracking

## Form Validation

### 1. Common Validation Patterns

```python
def clean_field(self):
    value = self.cleaned_data["field"]
    if condition:
        raise forms.ValidationError("Error message")
    return value
```

### 2. Cross-Field Validation

```python
def clean(self):
    cleaned_data = super().clean()
    field1 = cleaned_data.get("field1")
    field2 = cleaned_data.get("field2")
    if field1 and field2 and field1 != field2:
        raise forms.ValidationError("Fields must match")
```

## Error Handling

### 1. Form Errors
- Field-level validation errors
- Form-level validation errors
- Custom error messages

### 2. View Errors
- HTTP 404 for missing objects
- HTTP 403 for unauthorized access
- Custom error pages

## Best Practices

### 1. Form Design
- Use appropriate field types
- Implement client-side validation
- Provide clear error messages
- Use form prefixes for multiple forms

### 2. View Implementation
- Follow RESTful principles
- Implement proper authentication
- Use class-based views when appropriate
- Handle edge cases gracefully

## Security Considerations

### 1. Form Security
- CSRF protection
- Input sanitization
- File upload validation
- Rate limiting

### 2. View Security
- Authentication checks
- Permission verification
- Session management
- XSS prevention
