# System Design Diagrams

## 1. Class Diagram

```mermaid
classDiagram
    class Expense {
        +Integer id
        +Float amount
        +String date
        +String category_id
        +String payment_method
        +String note
        +String type
    }
    class Category {
        +Integer id
        +String name
        +String type
    }
    class ContactMessage {
        +Integer id
        +String name
        +String email
        +String subject
        +String message
        +DateTime created_at
    }
    
    Expense "*" -- "1" Category : belongs to
```

## 2. ER Diagram (Entity-Relationship)

```mermaid
erDiagram
    EXPENSE {
        int id PK
        float amount
        date date
        string payment_method
        string note
        string type
        int category_id FK
    }
    CATEGORY {
        int id PK
        string name
        string type
    }
    CONTACT_MESSAGE {
        int id PK
        string name
        string email
        string subject
        text message
        datetime created_at
    }
    
    CATEGORY ||--o{ EXPENSE : "has"
```

## 3. Sequence Diagram (Add Expense)

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Server
    participant Database
    
    User->>Browser: Fills Expense Form
    Browser->>Server: POST /expenses/add
    Server->>Server: Validate Data
    Server->>Database: INSERT INTO expense
    Database-->>Server: Success
    Server-->>Browser: Redirect to List
    Browser-->>User: Show "Expense Added"
```

## 4. Component Diagram

```mermaid
graph TD
    subgraph Client
        Browser[Web Browser]
    end
    
    subgraph Server
        Router[Flask Router]
        Service[Expense Service]
        Model[SQLAlchemy Models]
    end
    
    subgraph Data
        DB[(SQLite DB)]
    end
    
    Browser <--> Router
    Router <--> Service
    Service <--> Model
    Model <--> DB
```

## 5. Activity Diagram (Add Transaction)

```mermaid
flowchart TD
    Start((Start)) --> OpenForm[Open Add Transaction Page]
    OpenForm --> InputData[/Input Details/]
    InputData --> SelectType{Select Type}
    SelectType -->|Income| SetIncome[Set Type = Income]
    SelectType -->|Expense| SetExpense[Set Type = Expense]
    SetIncome --> Submit[Submit Form]
    SetExpense --> Submit
    Submit --> Validate{Valid?}
    Validate -- No --> ShowError[Show Error] --> InputData
    Validate -- Yes --> SaveDB[(Save to DB)]
    SaveDB --> ShowSuccess[Show Success Message]
    ShowSuccess --> End((End))
```

## 6. State Transition Diagram (Expense Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Updated : Edit Transaction
    Updated --> Updated : Edit Again
    Created --> Deleted : Delete Transaction
    Updated --> Deleted : Delete Transaction
    Deleted --> [*]
```

## 7. Database Schema Design

| Table | Column | Type | Constraints | Description |
|-------|--------|------|-------------|-------------|
| **Category** | id | Integer | PK | Unique ID |
| | name | String(50) | Not Null | Category Name |
| | type | String(20) | Default 'expense' | Income/Expense |
| **Expense** | id | Integer | PK | Unique ID |
| | amount | Float | Not Null | Transaction Amount |
| | date | Date | Not Null | Transaction Date |
| | category_id | Integer | FK | Links to Category |
| | payment_method | String(50) | | Cash/Card/UPI |
| | note | String(200) | | Optional Note |
| | type | String(20) | Default 'expense' | Income/Expense |
| **ContactMessage** | id | Integer | PK | Unique ID |
| | name | String(100) | | Sender Name |
| | email | String(120) | | Sender Email |
| | subject | String(100) | | Message Subject |
| | message | Text | | Message Body |

## 8. Data Dictionary

- **Transaction**: A record of a financial exchange (Income or Expense).
- **Category**: A classification for transactions (e.g., Food, Salary).
- **Prefix Sum**: An algorithmic concept used to calculate cumulative spending over time.
- **Export**: The process of converting database records into an Excel file.

## 9. Decision Table (Transaction Validation)

| Condition | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|-----------|--------|--------|--------|--------|
| Amount > 0 | Y | N | Y | Y |
| Date Valid | Y | Y | N | Y |
| Category Selected | Y | Y | Y | N |
| **Action** | | | | |
| Save Transaction | X | | | |
| Show Error | | X | X | X |
