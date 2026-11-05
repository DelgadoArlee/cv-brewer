# General System Rules

## 1. Purpose

This document defines the general rules and constraints that govern the system's behavior, data handling, and operation.

## 2. General Rules

### 2.1 Data Integrity

- All data must be validated before being accepted or processed.
    
- Data must conform to its defined structure and requirements.
    
- The system must not introduce unsupported or fabricated information.
    

### 2.2 Data Management

- Persistent data must be managed consistently.
    
- Data access and modification must follow established rules.
    

### 2.3 Processing

- Inputs must be validated before processing.
    
- Processing operations must follow their defined requirements.
    
- Invalid or unsupported inputs must not proceed through processing.
    
- Processing failures must not result in invalid or incomplete data being accepted.
    

### 2.4 System Independence

- System components must maintain their defined responsibilities and boundaries.
    
- Internal implementations should remain replaceable without unnecessarily affecting other components.
    
- Components must interact through their defined interfaces.
    

### 2.5 External Dependencies

- External dependencies must follow defined integration requirements.
    
- The system must account for unavailable or improperly configured dependencies.
    

### 2.6 Output

- Generated outputs must conform to their defined requirements.
    
- Outputs must only contain information supported by their intended data sources.
    
- Generated files must follow the system's defined output and storage rules.