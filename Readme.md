# CareerGraph

CareerGraph is a graph-powered career recommendation application built using Flask and CognoDB.

It helps users discover suitable career roles based on the skills they already have. For each recommended career, the application shows:

- Match percentage
- Matching skills
- Skills the user needs to learn
- Companies associated with the career
- A short explanation of why the career matches their profile

---

## Problem Statement

Choosing a career path can be difficult when a person has several skills but does not know which roles best match them.

CareerGraph models the relationships between:

- Students
- Skills
- Career roles
- Companies

This allows the application to recommend career paths based on the connections between a user's skills and the skills required by different roles.

---

## Why a Graph Database?

Career recommendations are naturally relationship-driven.

A user's skills connect to career roles, while career roles connect to companies.

The graph structure can represent these relationships directly:

```text
Student
   |
   | HAS_SKILL
   v
 Skill
   ^
   | REQUIRES
   |
JobRole
   ^
   | OFFERS
   |
Company
```

## Features

### Career Matching

Users select the skills they currently have and CareerGraph calculates a match percentage for available career roles.

### Matching Skills

The application shows which required skills the user already possesses.

### Skills to Learn

The application identifies skills required by a role that the user does not currently have.

### Company Recommendations

CareerGraph displays companies associated with each recommended career role.

### Match Explanation

Each recommendation includes a short explanation of why the role matches the user's current skills.

### Interactive UI

The application provides:

- Skill selection
- Loading state
- Empty state
- Career recommendation cards
- Match progress bars
- Skill chips
- Company chips
- Clear Selection functionality

---

## Technology Stack

- **Python**
- **Flask**
- **CognoDB**
- **Neo4j Python Driver**
- **openCypher**
- **HTML**
- **CSS**
- **JavaScript**
- **Git / GitHub**

---

## Graph Data Model

### Nodes

| Node | Description |
|---|---|
| `Student` | Represents a user/student |
| `Skill` | Represents a technical or analytical skill |
| `JobRole` | Represents a career role |
| `Company` | Represents a company associated with a career role |

### Relationships

| Relationship | Meaning |
|---|---|
| `Student -[:HAS_SKILL]-> Skill` | A student possesses a skill |
| `JobRole -[:REQUIRES]-> Skill` | A career role requires a skill |
| `Company -[:OFFERS]-> JobRole` | A company offers a career role |

### Graph Structure

```text
                   ┌──────────────┐
                   │   Student    │
                   └──────┬───────┘
                          │
                      HAS_SKILL
                          │
                          ▼
                   ┌──────────────┐
                   │    Skill     │
                   └──────▲───────┘
                          │
                       REQUIRES
                          │
                   ┌──────┴───────┐
                   │   JobRole    │
                   └──────▲───────┘
                          │
                         OFFERS
                          │
                   ┌──────┴───────┐
                   │   Company    │
                   └──────────────┘
