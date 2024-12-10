# Value Network Implementation

VerdunNRP implements a sophisticated value network system based on the REA (Resource-Event-Agent) accounting model. This document details the core implementation.

## Core Components

### 1. Economic Agents (EconomicAgent)

Economic agents are the fundamental actors in the system. The implementation includes:

#### Agent Types
- Individual
- Organization
- Network
- Project (Context Agent)

#### Key Features
```python
class EconomicAgent:
    name          # Agent's full name
    nick          # Unique identifier (max 32 chars)
    agent_type    # Reference to AgentType
    is_context    # Boolean for context agents
    reputation    # Decimal field for reputation tracking
    unit_of_claim_value  # Unit used for claims in context
```

#### Agent Relationships
- Parent-child hierarchies
- Associations between agents
- Context participation
- Supply chain connections

### 2. Economic Events

Events track all economic activities in the system:

#### Event Types
```python
class EventType:
    name              # Event type name
    label            # Display label
    relationship     # in/out direction
    resource_effect  # Impact on resources
    unit_type       # Type of units involved
```

#### Event Categories
1. Work Contributions
   - Time tracking
   - Task completion
   - Skill contributions

2. Resource Events
   - Creation
   - Consumption
   - Use
   - Citation

3. Transfer Events
   - Internal transfers
   - External exchanges
   - Distributions

### Event Processing
The system processes events through several key mechanisms:

1. **Event Creation and Validation**
   - Events are validated against process patterns
   - Resource quantities and types are checked
   - Stage transitions are enforced

2. **Value Computation**
   - Events can compute income shares based on value equations
   - Contributions are tracked and valued
   - Resource flows maintain value history

3. **Distribution Processing**
   - Value equations determine distribution of resources
   - Multiple distribution methods supported
   - Automatic disbursement handling

### 3. Resources

Resources represent all valuable items in the system:

#### Resource Types
```python
class EconomicResourceType:
    name            # Resource type name
    resource_class  # Classification
    unit           # Unit of inventory
    unit_of_use    # Unit for usage
    substitutable  # Whether instances are interchangeable
    inventory_rule # Inventory tracking behavior
```

#### Resource States
- Available
- In use
- Consumed
- Transferred
- Reserved

#### Resource Management

1. **Resource Types**
   - Define characteristics and behavior
   - Track units and measurements
   - Support multiple stages

2. **Resource Tracking**
   - Quantity and quality monitoring
   - Location and stage tracking
   - Value and price history

3. **Resource Flows**
   - Track resource movements
   - Maintain provenance
   - Support transformations

### 4. Process Patterns

Patterns define standard workflows:

```python
class ProcessPattern:
    name           # Pattern name
    event_types    # Associated event types
    use_cases     # Applicable use cases
```

#### Pattern Features
- Resource type matching
- Facet value validation
- Event type relationships
- Use case compatibility

## Value Calculations

### 1. Contribution Tracking
```python
class EconomicEvent:
    event_type
    provider
    receiver
    resource_type
    quantity
    value
    unit_of_value
```

### 2. Value Equations
- Contribution-based calculations
- Resource valuation
- Distribution rules
- Claims generation

### Value Equations

#### Structure
Value equations define how value is distributed:

1. **Buckets**
   - Group similar contributions
   - Apply specific rules
   - Handle different value types

2. **Rules**
   - Define contribution valuation
   - Set distribution criteria
   - Support custom formulas

3. **Distribution**
   - Calculate shares based on rules
   - Process disbursements
   - Track distributions

#### Implementation Details

1. **Event Processing**
```python
def compute_income_shares(self, value_equation, quantity, events, visited):
    # Track contributions
    contributions = self.resource_contribution_events()
    for evt in contributions:
        # Apply bucket rules
        value = evt.bucket_rule(value_equation)
        if value:
            # Calculate shares
            vpu = value / evt.quantity
            evt.share = quantity * vpu
            events.append(evt)
```

2. **Value Distribution**
```python
def run_value_equation_and_save(self, distribution, money_resource, amount_to_distribute):
    # Calculate distributions
    distribution_events = self.run_value_equation(amount_to_distribute)
    
    # Process disbursements
    for dist_event in distribution_events:
        # Create/update virtual accounts
        va = dist_event.to_agent.virtual_accounts()
        
        # Record distributions
        dist_event.resource = va
        dist_event.save()
```

## Integration Points

### 1. RESTful API

#### Key Endpoints
```python
# Agent Management
/api/agents/
/api/people/
/api/contexts/

# Economic Events
/api/events/
/api/contributions/

# Resources
/api/resources/
/api/resource-types/
```

#### Serialization
```python
class EconomicAgentSerializer:
    fields = [
        'url',
        'name',
        'nick',
        'agent_type',
        'address',
        'email',
        'projects'
    ]
```

### 2. Linked Data Support

The system supports JSON-LD format with:
- FOAF vocabulary
- Schema.org integration
- Value Flows vocabulary
- RDF compatibility

## Database Schema

### Core Tables
1. EconomicAgent
2. EconomicEvent
3. EconomicResource
4. ProcessPattern
5. ResourceType

### Relationships
- Agent associations
- Event connections
- Resource tracking
- Pattern matching

## Security Model

### 1. Authentication
- User-Agent linking
- Token-based API auth
- Permission checks

### 2. Authorization
- Context-based access
- Role-based permissions
- Resource ownership

## Performance Considerations

### 1. Indexing
- Agent identification
- Event tracking
- Resource location
- Pattern matching

### 2. Caching
- Resource states
- Value calculations
- Pattern matching
- Agent relationships

## Best Practices

1. **Event Processing**
   - Validate events before processing
   - Maintain audit trails
   - Handle edge cases gracefully

2. **Resource Management**
   - Track resource states
   - Validate transformations
   - Maintain provenance

3. **Value Distribution**
   - Use appropriate value equations
   - Validate distributions
   - Track disbursements
