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
