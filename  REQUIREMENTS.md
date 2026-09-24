# Requirements — Customer Search

## User Story

As a user,  
I want to search customers by name or email,  
so that I can quickly find the customer record I need.

## Functional Requirements

**FR-01:** The system shall allow users to search customers using a full or partial name.

**FR-02:** The system shall allow users to search customers using a full or partial email address.

**FR-03:** The system shall return customers whose name or email contains the search term.

**FR-04:** The system shall display search results in order of relevance, with the most relevant matches appearing first.

**FR-05:** The system shall display an appropriate message when no customers match the search criteria.

**FR-06:** The system shall display only customer information authorized for the current user to access.

**FR-07:** The system shall update the search results based on the user's search input without requiring the user to navigate away from the customer search screen.

**FR-08:** The system shall support searching across the complete customer dataset, including datasets containing a large number of customer records.

## Non-Functional Requirements

**NFR-01:** The system shall return search results within 2 seconds for at least 95% of searches under normal operating conditions.

**NFR-02:** The system shall protect customer information by enforcing the application's authentication and authorization controls during customer searches.

**NFR-03:** The customer search interface shall be usable on both desktop and mobile devices.

**NFR-04:** The search functionality shall maintain acceptable response times when the customer database contains at least 100,000 customer records.

## Open Questions

**Q-01:** What customer fields, in addition to name and email, should be displayed in the search results?

**Q-02:** What criteria should determine the relevance order of search results?

## Constraints / Assumptions

**C-01:** The search functionality will use the existing customer database and authentication/authorization mechanisms.

**A-01:** Customer names and email addresses are stored in a searchable format in the database.