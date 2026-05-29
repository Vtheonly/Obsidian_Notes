#!/usr/bin/env python3
"""Fix quiz files by appending missing matching questions with proper newlines."""

extras = {}

# Chapter_01/Q1.md - add 1 matching question
extras['Chapter_01'] = {}

extras['Chapter_01']['Q1'] = """

> [!question] Match the relational algebra operation with its result.
>> [!example] Group A
>> a) R ∪ S
>> b) R ∩ S
>> c) R - S
>> d) R × S
>
>> [!example] Group B
>> n) Tuples in R that are not in S
>> o) All unique tuples from both relations
>> p) Every combination of tuples from R and S
>> q) Tuples common to both relations
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
"""

extras['Chapter_01']['Q2'] = """

> [!question] Match the SQL view characteristic with its description.
>> [!example] Group A
>> a) WITH CHECK OPTION
>> b) Materialized view
>> c) Simple view
>> d) Complex view
>
>> [!example] Group B
>> n) Physically stored snapshot
>> o) Uses joins or aggregations
>> p) Single table, no functions
>> q) Prevents invisible row modifications
>
>> [!success]- Answer
>> a) -> q)
>> b) -> n)
>> c) -> p)
>> d) -> o)
"""

extras['Chapter_02'] = {}
extras['Chapter_02']['Q1'] = """

> [!question] Match the database object with its purpose.
>> [!example] Group A
>> a) Index
>> b) View
>> c) Sequence
>> d) Synonym
>
>> [!example] Group B
>> n) Virtual table
>> o) Speeds up data retrieval
>> p) Alias for another object
>> q) Generates unique numbers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)
"""

extras['Chapter_02']['Q2'] = """

> [!question] Match the access privilege with its SQL command.
>> [!example] Group A
>> a) GRANT
>> b) REVOKE
>> c) DENY
>> d) CREATE USER
>
>> [!example] Group B
>> n) Removes a permission
>> o) Blocks access explicitly
>> p) Assigns a permission
>> q) Creates a database account
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)
"""

extras['Chapter_03'] = {}
extras['Chapter_03']['Q1'] = """

> [!question] Match the concurrency control term with its definition.
>> [!example] Group A
>> a) Serializability
>> b) Recoverability
>> c) Cascadeless
>> d) Strictness
>
>> [!example] Group B
>> n) No cascading aborts possible
>> o) Equivalent to serial execution
>> p) Dirty reads not possible
>> q) Committed transactions are recoverable
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
"""

extras['Chapter_03']['Q2'] = """

> [!question] Match the RAID level with its description.
>> [!example] Group A
>> a) RAID 0
>> b) RAID 1
>> c) RAID 5
>> d) RAID 10
>
>> [!example] Group B
>> n) Mirroring + striping
>> o) Striping without parity
>> p) Mirroring
>> q) Striping with distributed parity
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> q)
>> d) -> n)
"""

extras['Chapter_04'] = {}
extras['Chapter_04']['Q1'] = """

> [!question] Match the query plan node type with its operation.
>> [!example] Group A
>> a) Seq Scan
>> b) Index Scan
>> c) Bitmap Heap Scan
>> d) Materialize
>
>> [!example] Group B
>> n) Reads index then fetches pages
>> o) Reads table sequentially
>> p) Caches intermediate results
>> q) Combines bitmap index scans
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)
"""

extras['Chapter_04']['Q2'] = """

> [!question] Match the optimization concept with its description.
>> [!example] Group A
>> a) Selectivity
>> b) Cardinality
>> c) Histogram
>> d) Correlation
>
>> [!example] Group B
>> n) Row count estimate
>> o) Fraction of rows matching a predicate
>> p) Physical ordering of column values
>> q) Value distribution across ranges
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> q)
>> d) -> p)

> [!question] Match the physical operator with its memory usage.
>> [!example] Group A
>> a) Hash join
>> b) Sort-merge join
>> c) Nested loop join
>> d) Index nested loop join
>
>> [!example] Group B
>> n) Minimal memory (row-by-row)
>> o) Memory for hash table
>> p) Minimal + index lookups
>> q) Memory for sort buffers
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)
"""

extras['Chapter_05'] = {}
extras['Chapter_05']['Q1'] = """

> [!question] Match the PL/SQL cursor type with its scope.
>> [!example] Group A
>> a) Implicit cursor
>> b) Explicit cursor
>> c) REF CURSOR
>> d) Cursor variable
>
>> [!example] Group B
>> n) Another name for REF CURSOR
>> o) Dynamically assigned to queries
>> p) Automatically managed by Oracle
>> q) Explicitly declared in DECLARE
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)
"""

extras['Chapter_05']['Q2'] = """

> [!question] Match the PL/SQL collection method with its effect.
>> [!example] Group A
>> a) FIRST
>> b) LAST
>> c) NEXT
>> d) PRIOR
>
>> [!example] Group B
>> n) Returns previous index
>> o) Returns last index
>> p) Returns first index
>> q) Returns next index
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)
"""

extras['Chapter_06'] = {}
extras['Chapter_06']['Q1'] = """

> [!question] Match the window function with its purpose.
>> [!example] Group A
>> a) ROW_NUMBER
>> b) RANK
>> c) DENSE_RANK
>> d) NTILE
>
>> [!example] Group B
>> n) Assigns rank with no gaps
>> o) Divides rows into buckets
>> p) Assigns unique sequential number
>> q) Assigns rank with gaps
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)
"""

extras['Chapter_06']['Q2'] = """

> [!question] Match the database design principle with its description.
>> [!example] Group A
>> a) Entity integrity
>> b) Referential integrity
>> c) Domain integrity
>> d) User-defined integrity
>
>> [!example] Group B
>> n) Business-specific rules
>> o) FK matches PK or NULL
>> p) Primary key is unique and not null
>> q) Column values must be of correct type
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the MySQL storage engine with its feature.
>> [!example] Group A
>> a) InnoDB
>> b) MyISAM
>> c) MEMORY
>> d) ARCHIVE
>
>> [!example] Group B
>> n) High-speed, volatile storage
>> o) Full-text search, table-level locking
>> p) High-compression, append-only
>> q) Transactions, row-level locking
>
>> [!success]- Answer
>> a) -> q)
>> b) -> o)
>> c) -> n)
>> d) -> p)
"""

import os

quiz_base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Quiz')

for chapter, files in extras.items():
    for fname, content in files.items():
        fp = os.path.join(quiz_base, chapter, f'{fname}.md')
        with open(fp, 'a') as f:
            f.write(content)
        print(f'  Fixed: {chapter}/{fname}.md')

print('\nAll fixes applied.')