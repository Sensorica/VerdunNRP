# Database Schema

VerdunNRP uses a relational database based on the REA (Resource-Event-Agent) accounting model. This document describes the core database tables and their relationships.

## Core Tables

### EconomicAgent
Represents participants in the value network.

```sql
CREATE TABLE EconomicAgent (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nick VARCHAR(32) UNIQUE NOT NULL,
    agent_type_id INTEGER REFERENCES AgentType(id),
    description TEXT,
    url VARCHAR(255),
    address VARCHAR(255),
    email VARCHAR(96),
    phone_primary VARCHAR(32),
    phone_secondary VARCHAR(32),
    latitude FLOAT,
    longitude FLOAT,
    reputation DECIMAL(8,2),
    is_context BOOLEAN DEFAULT FALSE,
    created_date DATE,
    changed_date DATE
);
```

### AgentType
Defines types of economic agents.

```sql
CREATE TABLE AgentType (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    party_type VARCHAR(12),
    description TEXT,
    is_context BOOLEAN DEFAULT FALSE
);
```

### EventType
Defines types of economic events.

```sql
CREATE TABLE EventType (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    label VARCHAR(32),
    inverse_label VARCHAR(40),
    relationship VARCHAR(12),
    related_to VARCHAR(12),
    resource_effect VARCHAR(12),
    unit_type VARCHAR(12)
);
```

### EconomicEvent
Records economic activities between agents.

```sql
CREATE TABLE EconomicEvent (
    id SERIAL PRIMARY KEY,
    event_type_id INTEGER REFERENCES EventType(id),
    provider_id INTEGER REFERENCES EconomicAgent(id),
    receiver_id INTEGER REFERENCES EconomicAgent(id),
    resource_type_id INTEGER REFERENCES EconomicResourceType(id),
    resource_id INTEGER REFERENCES EconomicResource(id),
    quantity DECIMAL(8,2),
    unit_of_quantity_id INTEGER REFERENCES Unit(id),
    value DECIMAL(8,2),
    unit_of_value_id INTEGER REFERENCES Unit(id),
    event_date TIMESTAMP,
    description TEXT
);
```

### EconomicResource
Represents resources in the system.

```sql
CREATE TABLE EconomicResource (
    id SERIAL PRIMARY KEY,
    identifier VARCHAR(128),
    resource_type_id INTEGER REFERENCES EconomicResourceType(id),
    quantity DECIMAL(8,2),
    unit_of_quantity_id INTEGER REFERENCES Unit(id),
    quality VARCHAR(32),
    notes TEXT,
    current_location_id INTEGER REFERENCES Location(id),
    created_date DATE,
    state_id INTEGER REFERENCES ResourceState(id)
);
```

## Supporting Tables

### Location
```sql
CREATE TABLE Location (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    description TEXT,
    address VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT
);
```

### Unit
```sql
CREATE TABLE Unit (
    id SERIAL PRIMARY KEY,
    unit_type VARCHAR(12),
    name VARCHAR(64),
    symbol VARCHAR(1),
    abbrev VARCHAR(8)
);
```

### AgentAssociation
```sql
CREATE TABLE AgentAssociation (
    id SERIAL PRIMARY KEY,
    is_associate_id INTEGER REFERENCES EconomicAgent(id),
    has_associate_id INTEGER REFERENCES EconomicAgent(id),
    association_type_id INTEGER REFERENCES AgentAssociationType(id),
    description TEXT,
    state VARCHAR(12)
);
```

### ResourceState
```sql
CREATE TABLE ResourceState (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    description TEXT
);
```

### ResourceClass
```sql
CREATE TABLE ResourceClass (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    description TEXT
);
```

## Model Relationships

### Agent Relationships

1. **Agent Hierarchy**
   - Agents can have parent-child relationships through `AgentType`
   - Context agents are marked with `is_context=True`
   - Agents can be associated through `AgentAssociation`

2. **Agent Associations**
   - Types defined in `AgentAssociationType`
   - States: active, inactive, potential
   - Behaviors: supplier, customer, member, peer

### Resource Management

1. **Resource States**
   - Defined in `ResourceState`

2. **Resource Classes**
   - Defined in `ResourceClass`

3. **Resource Type Relationships**
   - Parent-child relationships
   - Substitution relationships
   - Recipe inheritance

### Event Processing

1. **Event Type Relationships**
   - Direction: input/output
   - Related to: process/exchange
   - Resource effects: increment/decrement/none

2. **Event Processing Rules**
   - Validation requirements
   - Resource state changes
   - Value calculations

## Data Integrity

### Constraints

1. **Unique Constraints**
   - Agent nick names
   - Resource type names
   - Location names
   - Unit abbreviations

2. **Foreign Key Relationships**
   - Agent types to agents
   - Resource types to resources
   - Units to measurements
   - Locations to resources

### Indexes

1. **Primary Indexes**
   - All primary keys use SERIAL
   - Automatically indexed

2. **Secondary Indexes**
   - Agent nick names
   - Resource identifiers
   - Event dates
   - Location coordinates

## Data Access Patterns

### Common Queries

1. **Agent Queries**
```sql
-- Get all active agents of a specific type
SELECT * FROM EconomicAgent 
WHERE agent_type_id = ? AND state = 'active';

-- Get all members of a context agent
SELECT a.* FROM EconomicAgent a
JOIN AgentAssociation aa ON a.id = aa.is_associate_id
WHERE aa.has_associate_id = ? 
AND aa.association_type = 'member';
```

2. **Resource Queries**
```sql
-- Get available resources of a type
SELECT * FROM EconomicResource
WHERE resource_type_id = ? 
AND quantity > 0;

-- Get resources at a location
SELECT * FROM EconomicResource
WHERE current_location_id = ?;
```

3. **Event Queries**
```sql
-- Get events for a process
SELECT * FROM EconomicEvent
WHERE process_id = ?
ORDER BY event_date;

-- Get resource creation events
SELECT * FROM EconomicEvent
WHERE event_type_id IN (
    SELECT id FROM EventType 
    WHERE resource_effect = 'increment'
);
```

### Performance Considerations

1. **Query Optimization**
   - Use appropriate indexes
   - Join order optimization
   - Subquery optimization

2. **Data Volume Management**
   - Archive old events
   - Summarize historical data
   - Partition large tables

## Data Migration

### Version Control

1. **Schema Migrations**
   - Use South for Django migrations
   - Version control all changes
   - Document migration steps

2. **Data Migrations**
   - Handle data transformations
   - Preserve data integrity
   - Validate results

### Backup Strategy

1. **Regular Backups**
   - Daily full backups
   - Hourly incremental backups
   - Transaction log backups

2. **Recovery Procedures**
   - Point-in-time recovery
   - Transaction rollback
   - Data verification

## Best Practices

### Data Entry

1. **Validation Rules**
   - Required fields
   - Data type constraints
   - Business logic validation

2. **Default Values**
   - Sensible defaults
   - Automatic timestamps
   - System-generated IDs

### Data Maintenance

1. **Data Cleanup**
   - Regular consistency checks
   - Orphan record cleanup
   - Duplicate detection

2. **Performance Monitoring**
   - Query performance
   - Index usage
   - Storage utilization

## Indexes

Important indexes for performance:

```sql
CREATE INDEX idx_agent_nick ON EconomicAgent(nick);
CREATE INDEX idx_agent_type ON EconomicAgent(agent_type_id);
CREATE INDEX idx_event_date ON EconomicEvent(event_date);
CREATE INDEX idx_event_provider ON EconomicEvent(provider_id);
CREATE INDEX idx_event_receiver ON EconomicEvent(receiver_id);
CREATE INDEX idx_resource_identifier ON EconomicResource(identifier);
```

## Constraints

Key constraints for data integrity:

```sql
-- Ensure positive quantities
ALTER TABLE EconomicEvent
ADD CONSTRAINT positive_quantity CHECK (quantity >= 0);

-- Ensure valid dates
ALTER TABLE EconomicEvent
ADD CONSTRAINT valid_event_date CHECK (event_date <= CURRENT_TIMESTAMP);

-- Ensure unique agent associations
ALTER TABLE AgentAssociation
ADD CONSTRAINT unique_association UNIQUE (is_associate_id, has_associate_id, association_type_id);
