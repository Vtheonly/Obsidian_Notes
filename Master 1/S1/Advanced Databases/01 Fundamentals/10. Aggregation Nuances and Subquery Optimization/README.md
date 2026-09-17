# 10. Aggregation Nuances and Subquery Optimization

This chapter covers SQL aggregation with `NULL`, filtering before and after grouping, and the reasoning needed to choose between joins, subqueries, and `EXISTS`.

## Contents

- [[01 NULL and Aggregate Functions]]
- [[02 COUNT and Other Aggregate Functions]]
- [[03 WHERE versus HAVING]]
- [[04 Subqueries and Correlated Subqueries]]
- [[05 EXISTS versus JOIN]]
- [[06 Aggregation and Subquery Exercises]]

## Learning Objectives

- predict how aggregate functions treat `NULL`;
- distinguish `COUNT(*)` from `COUNT(column)`;
- choose `WHERE` or `HAVING` according to the stage being filtered;
- recognize scalar, multi-row, and correlated subqueries;
- use `EXISTS` when the question is about existence rather than returning matching rows;
- reason about query plans instead of assuming one syntax is always faster.
