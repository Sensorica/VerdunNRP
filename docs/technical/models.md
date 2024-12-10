# VerdunNRP Models Documentation

## Overview

The VerdunNRP project uses a comprehensive model architecture based on the Resource-Event-Agent (REA) accounting model. This documentation provides an in-depth look at the core models, their relationships, and implementation details.

## Core Model Principles

1. **Domain-Driven Design**
   - Rich domain models
   - Encapsulated business logic
   - Clear separation of concerns

2. **REA Accounting Model**
   - Resource-centric design
   - Event-driven interactions
   - Agent-based relationships

## Valueaccounting Core Models

### 1. EconomicAgent Model

#### Purpose
Represents participants in the economic network, including individuals, organizations, and projects.

#### Key Fields
```python
class EconomicAgent(models.Model):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=32, unique=True)
    agent_type = models.ForeignKey(AgentType)
    description = models.TextField(blank=True)
    
    # Location and Contact
    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=32, blank=True)
    
    # Geospatial Information
    latitude = models.FloatField(default=0.0, blank=True)
    longitude = models.FloatField(default=0.0, blank=True)
    
    # Reputation and Tracking
    reputation = models.DecimalField(max_digits=8, decimal_places=2)
    is_context = models.BooleanField(default=False)
```

#### Key Methods
- `get_absolute_url()`: Generate unique URL for agent
- `contributions()`: Retrieve agent's contributions
- `resources_created()`: List resources created
- `active_processes()`: Get active processes

### 2. EventType Model

#### Purpose
Defines types of economic events with detailed metadata.

#### Key Fields
```python
class EventType(models.Model):
    name = models.CharField(max_length=128)
    label = models.CharField(max_length=32)
    
    # Event Characteristics
    relationship = models.CharField(
        choices=DIRECTION_CHOICES, 
        default='in'
    )
    related_to = models.CharField(
        choices=RELATED_CHOICES, 
        default='process'
    )
    resource_effect = models.CharField(
        choices=RESOURCE_EFFECT_CHOICES
    )
    unit_type = models.CharField(
        choices=UNIT_TYPE_CHOICES, 
        blank=True
    )
```

#### Key Methods
- `creates_resources()`: Check if event creates resources
- `is_work()`: Determine if event is work-related
- `default_event_value_equation()`: Get default valuation method

### 3. EconomicEvent Model

#### Purpose
Represents economic activities and interactions between agents.

#### Key Fields
```python
class EconomicEvent(models.Model):
    event_type = models.ForeignKey(EventType)
    
    # Agent Relationships
    provider = models.ForeignKey(
        EconomicAgent, 
        related_name='events_provided'
    )
    receiver = models.ForeignKey(
        EconomicAgent, 
        related_name='events_received'
    )
    
    # Resource Details
    resource_type = models.ForeignKey(EconomicResourceType)
    resource = models.ForeignKey(EconomicResource)
    
    # Quantitative Measurements
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_of_quantity = models.ForeignKey(Unit)
    
    # Value Tracking
    value = models.DecimalField(max_digits=8, decimal_places=2)
    unit_of_value = models.ForeignKey(Unit)
    
    # Temporal and Contextual Information
    event_date = models.DateTimeField()
    description = models.TextField(blank=True)
```

#### Key Methods
- `process_effects()`: Apply resource and value changes
- `validate_event()`: Ensure event integrity
- `calculate_value()`: Compute event's economic value

### 4. EconomicResource Model

#### Purpose
Tracks resources within the economic network.

#### Key Fields
```python
class EconomicResource(models.Model):
    identifier = models.CharField(max_length=128, unique=True)
    resource_type = models.ForeignKey(EconomicResourceType)
    
    # Quantitative Attributes
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_of_quantity = models.ForeignKey(Unit)
    
    # Resource Characteristics
    quality = models.CharField(max_length=32, blank=True)
    current_location = models.ForeignKey(Location)
    state = models.ForeignKey(ResourceState)
    
    # Tracking Metadata
    created_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

#### Key Methods
- `increment_quantity()`: Increase resource quantity
- `decrement_quantity()`: Reduce resource quantity
- `change_location()`: Update resource location
- `update_state()`: Modify resource state

## Supporting Models

### AgentType
Defines categories and hierarchies of economic agents.

### Unit
Manages measurement units across different domains.

### Location
Tracks geographical and spatial information.

## Model Relationships

1. **Agent Relationships**
   - Hierarchical agent types
   - Agent associations
   - Context agent management

2. **Resource Flows**
   - Resource type relationships
   - Event-driven resource changes
   - Location and state tracking

3. **Event Processing**
   - Event type definitions
   - Resource effect tracking
   - Value calculations

## Best Practices

### Model Design
1. Use meaningful, unique identifiers
2. Implement comprehensive validation
3. Maintain clear relationship semantics
4. Support flexible resource tracking

### Performance Considerations
1. Optimize database indexes
2. Use appropriate field types
3. Implement efficient querying
4. Minimize database load

### Security Guidelines
1. Validate all input data
2. Implement role-based access
3. Protect sensitive information
4. Audit critical model changes

## Future Enhancements
1. Machine learning integration
2. Advanced predictive modeling
3. Enhanced value calculation algorithms
4. Improved resource tracking

## Changelog

### v1.0.0
- Initial REA model implementation
- Core agent, event, and resource models
- Basic validation and tracking

### v1.1.0
- Enhanced relationship tracking
- Improved value calculation methods
- Expanded resource state management
