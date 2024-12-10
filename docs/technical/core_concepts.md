# Core Concepts

VerdunNRP is built on the Resource-Event-Agent (REA) accounting model, which provides a robust framework for tracking economic resources, events, and agents in a value network.

## REA Model Components

### 1. Economic Agents (EconomicAgent)

Economic agents are the participants in the value network. They can be:

- Individuals
- Organizations
- Networks
- Projects

Key attributes:
- Name and identification (nick)
- Type (AgentType)
- Contact information
- Location
- Reputation

### 2. Economic Events

Events represent economic activities between agents. Types include:

- Work contributions
- Resource creation
- Resource consumption
- Transfers
- Distributions

Each event has:
- Event type
- Provider and receiver
- Resource type and quantity
- Date and location
- Value measurements

### 3. Economic Resources

Resources that flow between agents. Characteristics:

- Resource type
- Tracking identifier
- Quantity and unit
- Quality
- Location
- State (condition)

## Value Network Features

### 1. Agent Relationships

- Hierarchical structures (parent-child)
- Peer relationships
- Supply chain connections
- Customer relationships

### 2. Resource Tracking

- Inventory management
- Resource flows
- Value calculations
- State changes

### 3. Process Management

- Work processes
- Resource transformation
- Supply chain processes
- Distribution processes

### 4. Value Equations

Used to:
- Calculate contributions
- Determine distributions
- Track value flows
- Manage rewards

## Technical Implementation

### 1. Database Models

#### Core Models

##### EconomicAgent
- Primary model for participants in the value network
- Key fields:
  - `name`: Full name of the agent
  - `nick`: Unique identifier (max 32 chars)
  - `agent_type`: Reference to AgentType
  - `description`: Detailed description
  - `is_context`: Boolean indicating if agent is a context agent
  - `reputation`: Decimal field tracking agent's reputation
  - `unit_of_claim_value`: Unit used for claims in context agents

##### AgentType
- Defines categories of economic agents
- Supports hierarchical relationships through `parent` field
- Includes party_type classification (individual, organization, etc.)
- Special flag `is_context` for context agents

##### EventType
- Defines types of economic activities
- Key attributes:
  - `relationship`: Direction of event (in/out)
  - `related_to`: What the event relates to (process, exchange, etc.)
  - `resource_effect`: Impact on resources
  - `unit_type`: Type of units involved

##### EconomicResource
- Represents resources in the system
- Tracks:
  - Quantity and units
  - Quality and state
  - Location
  - Resource type relationship
  - Creation and modification dates

#### Supporting Models

##### Location
- Tracks physical locations
- Includes:
  - Name and description
  - Address
  - Geographical coordinates (latitude/longitude)
  - Related resources and agents

##### Unit
- Defines measurement units
- Categories include:
  - Area
  - Length
  - Time
  - Value
  - Weight
  - Volume
  - Count

##### AgentAssociation
- Manages relationships between agents
- Types include:
  - Supplier relationships
  - Customer relationships
  - Membership
  - Peer relationships

### 2. Core Functionalities

#### Agent Management
- Creation and management of economic agents
- Hierarchical organization support
- Association and relationship tracking
- Reputation management
- Location-based services

#### Resource Management
- Resource tracking and inventory
- State and location management
- Resource type relationships
- Quality control
- Unit conversion

#### Event Processing
- Event creation and validation
- Resource effect tracking
- Process and exchange management
- Value calculations
- Distribution management

#### Value Network Features
1. **Agent Relationships**
   - Hierarchical structures
   - Peer relationships
   - Supply chain connections
   - Customer relationships

2. **Resource Tracking**
   - Inventory management
   - Resource flows
   - Value calculations
   - State changes

3. **Process Management**
   - Work processes
   - Resource transformation
   - Supply chain processes
   - Distribution processes

4. **Value Equations**
   - Contribution calculations
   - Distribution determinations
   - Value flow tracking
   - Reward management

### 3. Integration Points

#### API Structure
- RESTful endpoints for:
  - Agent management
  - Event logging
  - Resource tracking
  - Process management
  - Value calculations

#### External Systems
- Authentication system integration
- Geographic information systems
- Accounting systems
- Resource planning systems

### 4. Best Practices

#### Data Management
1. Always maintain unique identifiers for agents (`nick` field)
2. Use appropriate unit types for measurements
3. Track all resource state changes
4. Maintain accurate location data

#### Process Implementation
1. Validate all economic events
2. Track resource effects
3. Maintain relationship hierarchies
4. Document value calculations

#### Security Considerations
1. Protect agent information
2. Validate association changes
3. Control access to value equations
4. Monitor reputation changes

## Integration Points

### 1. External Systems

- Accounting systems
- Inventory management
- Project management
- Communication tools

### 2. Data Exchange

- RESTful API
- JSON-LD support
- RDF compatibility
- Linked Open Data
