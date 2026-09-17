---
tags: [moc, code-walkthrough, case-study]
type: moc
status: complete
---

# MOC — Code Walkthrough

> Before learning the theory, see what we're studying. This chapter is a brief,
> brutal tour of every file in the original repository and what it does (and
> what's wrong with it).

## Notes (read in order)

1. [[01 - Code Walkthrough/02 - Project File Map]] — every file in the repo and its role.
2. [[01 - Code Walkthrough/09 - main java and module-info]] — entry point + JPMS descriptor.
3. [[01 - Code Walkthrough/10 - oracleConnector java (the God Class)]] — 940-line monolith.
4. [[01 - Code Walkthrough/12 - toolkit java and DataPreprocessor java]] — string parsing, broken password hashing.
5. [[01 - Code Walkthrough/08 - loginController java]] — login flow with 3 redundant queries + magic role IDs.
6. [[01 - Code Walkthrough/06 - insertionInternController java]] — secretary view: insert, search, TitledPane pool, PDF, email tab.
7. [[01 - Code Walkthrough/07 - insertionUserController java]] — admin view: workers + themes + departments + hardcoded PieChart.
8. [[01 - Code Walkthrough/05 - chiefDecisionController java]] — chief view: accept/reject individually or bulk.
9. [[01 - Code Walkthrough/13 - updateInternController and updateUserController]] — update forms fed by `static String labelText`.
10. [[01 - Code Walkthrough/01 - FXML Files]] — 6 FXML views, absolute positioning, Glow, empty CSS.
11. [[01 - Code Walkthrough/04 - SQL Scripts]] — `insertion.sql` vs `requstes.sql` schema conflict.
12. [[01 - Code Walkthrough/11 - pom xml and docker-compose]] — Maven build + Docker setup.
13. [[01 - Code Walkthrough/03 - README and Hidden Features]] — claimed features that don't exist.
