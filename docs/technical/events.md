# Event System

VerdunNRP's event system is the core mechanism for tracking all economic activities within the value network. This document details its implementation and usage.

## Event Types

### 1. Work Events
Track labor and contributions:

```python
class EventType:
    name = "Work"
    relationship = "out"
    resource_effect = "use"
    related_to = "process"
```

Features:
- Time tracking
- Skill tracking
- Task completion
- Quality assessment

### 2. Resource Events

#### Creation Events
```python
class EventType:
    name = "Create"
    relationship = "out"
    resource_effect = "create"
    related_to = "process"
```

Track:
- Resource production
- Asset creation
- Document generation

#### Consumption Events
```python
class EventType:
    name = "Consume"
    relationship = "in"
    resource_effect = "consume"
    related_to = "process"
```

Track:
- Material usage
- Resource depletion
- Inventory reduction

#### Use Events
```python
class EventType:
    name = "Use"
    relationship = "in"
    resource_effect = "use"
    related_to = "process"
```

Track:
- Tool usage
- Equipment utilization
- Facility use

### 3. Transfer Events

#### Internal Transfers
```python
class EventType:
    name = "Transfer"
    relationship = "both"
    resource_effect = "transfer"
    related_to = "exchange"
```

Features:
- Resource movement
- Ownership changes
- Location tracking

#### Distributions
```python
class EventType:
    name = "Distribution"
    relationship = "out"
    resource_effect = "transfer"
    related_to = "distribution"
```

Features:
- Value distribution
- Reward allocation
- Resource sharing

## Event Implementation

### 1. Core Event Model

```python
class EconomicEvent:
    event_type      # Reference to EventType
    event_date      # When the event occurred
    from_agent      # Provider
    to_agent        # Receiver
    resource_type   # Type of resource involved
    resource        # Specific resource instance
    quantity        # Amount
    unit_of_quantity # Unit of measurement
    value           # Economic value
    unit_of_value   # Value unit
    description     # Event description
```

### 2. Event Processing

#### Creation
```python
def create_event(event_type, from_agent, to_agent, resource_type, quantity):
    event = EconomicEvent.objects.create(
        event_type=event_type,
        from_agent=from_agent,
        to_agent=to_agent,
        resource_type=resource_type,
        quantity=quantity
    )
    process_event_effects(event)
```

#### Effect Processing
```python
def process_event_effects(event):
    if event.resource_effect == "create":
        create_resource(event)
    elif event.resource_effect == "consume":
        consume_resource(event)
    elif event.resource_effect == "use":
        use_resource(event)
    elif event.resource_effect == "transfer":
        transfer_resource(event)
```

### 3. Event Validation

#### Rules
1. Resource Availability
```python
def validate_resource_availability(event):
    if event.resource_effect in ["consume", "use", "transfer"]:
        return check_resource_quantity(event.resource, event.quantity)
```

2. Agent Authorization
```python
def validate_agent_authorization(event):
    return check_agent_permissions(event.from_agent, event.resource_type)
```

3. Event Consistency
```python
def validate_event_consistency(event):
    return validate_units(event) and validate_dates(event)
```

## Event Querying

### 1. Basic Queries

```python
# Get all events for an agent
agent_events = EconomicEvent.objects.filter(
    Q(from_agent=agent) | Q(to_agent=agent)
)

# Get all events in a context
context_events = EconomicEvent.objects.filter(
    context_agent=context
)

# Get all events of a type
type_events = EconomicEvent.objects.filter(
    event_type=event_type
)
```

### 2. Complex Queries

```python
# Get all resource creation events in a date range
creation_events = EconomicEvent.objects.filter(
    event_type__resource_effect="create",
    event_date__range=(start_date, end_date)
)

# Get all transfer events between agents
transfer_events = EconomicEvent.objects.filter(
    event_type__resource_effect="transfer",
    from_agent=agent1,
    to_agent=agent2
)
```

## Event Reporting

### 1. Contribution Reports
```python
def get_agent_contributions(agent, date_range):
    return EconomicEvent.objects.filter(
        from_agent=agent,
        event_type__relationship="out",
        event_date__range=date_range
    )
```

### 2. Resource Reports
```python
def get_resource_history(resource):
    return EconomicEvent.objects.filter(
        resource=resource
    ).order_by('event_date')
```

### 3. Value Reports
```python
def get_value_flows(context):
    return EconomicEvent.objects.filter(
        context_agent=context,
        value__isnull=False
    )
```

## Integration Points

### 1. API Endpoints
- `/api/events/`: List and create events
- `/api/contributions/`: List contribution events
- `/api/transfers/`: List transfer events

### 2. Event Hooks
```python
def register_event_hook(event_type, callback):
    """Register a callback for event type"""
    EVENT_HOOKS[event_type].append(callback)

def process_event_hooks(event):
    """Process all registered hooks for an event"""
    for hook in EVENT_HOOKS[event.event_type]:
        hook(event)
```

## Event System Implementation

### Core Components

### Event Types

The system defines several standard event types:

1. **Core Event Types**
   - Resource Events (creation, consumption)
   - Exchange Events (transfer, trade)
   - Work Events (contribution, process)
   - Distribution Events (value distribution)

2. **Event Type Properties**
   ```python
   class EventType:
       name = models.CharField(max_length=128)
       label = models.CharField(max_length=32)
       relationship = models.CharField(choices=DIRECTION_CHOICES)
       related_to = models.CharField(choices=RELATED_CHOICES)
       resource_effect = models.CharField(choices=RESOURCE_EFFECT_CHOICES)
       unit_type = models.CharField(choices=UNIT_TYPE_CHOICES)
   ```

### Event Processing

1. **Event Creation**
   ```python
   def create_economic_event(provider, receiver, resource_type, quantity):
       event = EconomicEvent.objects.create(
           event_type=event_type,
           provider=provider,
           receiver=receiver,
           resource_type=resource_type,
           quantity=quantity
       )
       event.process_effects()
       return event
   ```

2. **Validation Rules**
   - Provider and receiver must be valid agents
   - Resource type must match event type
   - Quantity must be positive
   - Units must be compatible

3. **Effect Processing**
   - Update resource quantities
   - Modify resource states
   - Calculate value changes
   - Record distributions

### Event Relationships

1. **Process Events**
   - Input events (consumption)
   - Output events (production)
   - Work contribution events

2. **Exchange Events**
   - Transfer events
   - Trade events
   - Reciprocal events

3. **Resource Events**
   - Creation events
   - Consumption events
   - Transfer events
   - State change events

### Implementation Details

1. **Event Creation**
   ```python
   class EconomicEvent:
       event_type = models.ForeignKey(EventType)
       provider = models.ForeignKey(EconomicAgent)
       receiver = models.ForeignKey(EconomicAgent)
       resource_type = models.ForeignKey(EconomicResourceType)
       resource = models.ForeignKey(EconomicResource)
       quantity = models.DecimalField()
       unit_of_quantity = models.ForeignKey(Unit)
       value = models.DecimalField()
       unit_of_value = models.ForeignKey(Unit)
   ```

2. **Event Processing**
   ```python
   def process_event(event):
       # Validate event
       if not event.is_valid():
           raise ValidationError()
       
       # Process resource effects
       if event.event_type.resource_effect == 'increment':
           event.resource.increment_quantity(event.quantity)
       elif event.event_type.resource_effect == 'decrement':
           event.resource.decrement_quantity(event.quantity)
       
       # Calculate values
       event.calculate_value()
       
       # Record distributions
       event.process_distributions()
   ```

3. **Value Calculations**
   ```python
   def calculate_value(event):
       if event.value_equation:
           return event.value_equation.calculate(event)
       return event.default_value()
   ```

### Integration Points

1. **Process Integration**
   - Event triggers process state changes
   - Process completion triggers events
   - Resource state updates

2. **Resource Integration**
   - Quantity updates
   - State changes
   - Location changes
   - Value calculations

3. **Agent Integration**
   - Reputation updates
   - Association changes
   - Context relationships

### Best Practices

1. **Event Creation**
   - Always validate events before processing
   - Use appropriate event types
   - Include all required relationships
   - Set correct units

2. **Event Processing**
   - Process events atomically
   - Handle failures gracefully
   - Log all changes
   - Maintain audit trail

3. **Value Calculations**
   - Use appropriate value equations
   - Validate calculations
   - Handle currency conversions
   - Track historical values

4. **Data Integrity**
   - Validate all relationships
   - Maintain consistency
   - Handle concurrent events
   - Preserve history

### Error Handling

1. **Validation Errors**
   - Invalid relationships
   - Insufficient quantities
   - Incompatible units
   - Missing required data

2. **Processing Errors**
   - Resource conflicts
   - Value calculation errors
   - Distribution failures
   - State transition errors

3. **Recovery Procedures**
   - Rollback changes
   - Log errors
   - Notify relevant agents
   - Maintain audit trail

### Monitoring and Maintenance

1. **Event Monitoring**
   - Track processing times
   - Monitor error rates
   - Analyze patterns
   - Alert on issues

2. **Data Maintenance**
   - Archive old events
   - Clean up invalid events
   - Update relationships
   - Optimize performance
