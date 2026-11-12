# Physical Join Algorithms & Database Indexing

This note covers **Physical Scan Paths, Join Algorithm Pseudocode & Complexity, Pipelining vs. Materialization, and Database Indexing Internals** (Clustered vs. Secondary, Composite Leftmost Prefix, B+ Trees, Extendible Hashing, and Bitmap Indexes).

---

## 1. Physical Access Paths & Execution Strategies

### Access Paths
- **Sequential (Table) Scan:** Reads every page sequentially ($P_R$ I/Os). Fastest when a table is small OR when **selectivity is low** (e.g., `WHERE gender = 'Male'` matching 50% of rows—following a secondary index for 50% of rows triggers expensive random disk I/O that loses to a sequential scan!).
- **Index Scan:** Traverses a B+ tree (`WHERE id = 5`) to locate RowIDs, then reads matching data blocks.
- **Index-Only Scan (Covering Index):** If the index contains **all** columns referenced in `SELECT` and `WHERE`, the DBMS returns results straight from the index without touching the main table pages at all.

### Execution Strategies: Materialization vs. Pipelining
- **Materialization:** Each operator finishes completely and writes its entire intermediate output to a temporary disk table before passing it up (slow disk I/O, required for blocking operators like `SORT` and `GROUP BY`).
- **Pipelining (Volcano Iterator Model):** Every operator exposes `open()`, `next()`, and `close()`. Parent operators pull tuples one by one on demand (`Project.next()` $\leftarrow$ `Join.next()` $\leftarrow$ `Filter.next()`) in RAM with zero intermediate disk writes.

---

## 2. Physical Join Algorithms (Pseudocode, Complexity & Memory)

### A. Simple Nested Loop Join (SNLJ)
```text
J := Ø
FOR EACH row r IN outer_table R DO:
    FOR EACH row s IN inner_table S DO:
        IF r.key == s.key THEN J := J ∪ {r || s}
    END FOR
END FOR
RETURN J
```
- **Complexity / I/O Cost:** $\mathcal{O}(N_R \cdot N_S)$ comparisons; page I/O = **$P_R + (N_R \times P_S)$** (or $P_R + P_R \cdot P_S$ page-at-a-time).
- **Memory & Use:** $\mathcal{O}(1)$ RAM frames; viable only for tiny tables.

### B. Index Nested Loop Join (INLJ)
```text
J := Ø
FOR EACH row r IN outer_table R DO:
    s_rows := Index_Search(Index_S, r.key)  -- O(log N_S) B+ tree lookup
    FOR EACH s IN s_rows DO: J := J ∪ {r || s}
END FOR
RETURN J
```
- **Complexity:** $\mathcal{O}(N_R \log N_S)$; ideal when joining a small filtered outer table $R$ against a large indexed inner table $S$.

### C. Sort-Merge Join (SMJ)
```text
Sort(R, key); Sort(S, key)
r_idx := 0; s_idx := 0
WHILE r_idx < N_R AND s_idx < N_S DO:
    IF R[r_idx].key == S[s_idx].key THEN
        match_start_s := s_idx
        WHILE r_idx < N_R AND R[r_idx].key == S[match_start_s].key DO:
            s_idx := match_start_s
            WHILE s_idx < N_S AND R[r_idx].key == S[s_idx].key DO:
                J := J ∪ {R[r_idx] || S[s_idx]}; s_idx++
            END WHILE
            r_idx++
        END WHILE
    ELSE IF R[r_idx].key < S[s_idx].key THEN r_idx++
    ELSE s_idx++
END WHILE
```
- **Complexity:** $\mathcal{O}(N_R \log N_R + N_S \log N_S)$ if sorting is needed, or linear $\mathcal{O}(N_R + N_S)$ / **$P_R + P_S$** if both inputs are already sorted (clustered indexes) or `ORDER BY` matches the join key.

### D. Hash Join (HJ)
```text
hash_map := {}
-- Phase 1: Build Phase (always build on the SMALLER table R so it fits in RAM!)
FOR EACH r IN R DO: hash_map[hash(r.key)].append(r) END FOR
-- Phase 2: Probe Phase (stream larger table S)
FOR EACH s IN S DO:
    FOR EACH r IN hash_map[hash(s.key)] DO:
        IF r.key == s.key THEN J := J ∪ {r || s}
    END FOR
END FOR
```
- **Complexity & Cost:** $\mathcal{O}(N_R + N_S)$ linear time! Needs $\mathcal{O}(P_R)$ RAM; if $R$ exceeds RAM, **Grace Hash Join** partitions and spills buckets to disk ($\approx \mathbf{3(P_R + P_S)}$ I/Os). Default champion for large unsorted equi-joins.

---

## 3. Database Indexing Deep Dive

### Analogies & Primary (Clustered) vs. Secondary Indexes
- **Clustered (Primary) Index — The Phone Book:** The table's physical rows on disk are stored in the exact sorted order of the index key (so data is right next to the key!). A table can have **at most one** clustered index (usually the Primary Key). Fast for range scans (`WHERE id BETWEEN 50 AND 100`).
- **Secondary (Non-Clustered) Index — The Book Index:** A separate sorted structure holding keys + RowID pointers to unsorted data rows. A table can have many secondary indexes (for `WHERE`, `JOIN`, `ORDER BY`, or alternate keys like `email`).

### Composite Indexes & The Leftmost Prefix Rule
```sql
CREATE INDEX idx_users_name ON users(last_name, first_name);
```
Because entries are sorted by `last_name` first and `first_name` second:
- Serves `WHERE last_name = 'Benali' AND first_name = 'Ahmed'` $\to$ **Fast index seek**.
- Serves `WHERE last_name = 'Benali'` $\to$ **Fast index seek**.
- **Cannot** efficiently serve `WHERE first_name = 'Ahmed'` alone (violates the **leftmost prefix rule**!).

### Write Overhead & Anti-Patterns
Every `INSERT`, `UPDATE` (on an indexed column), and `DELETE` must update and rebalance every index on the table (causing B-tree node splits/merges—during massive bulk loads, DBAs drop secondary indexes, load data, and rebuild them!). Also avoid wrapping indexed columns in functions (`WHERE YEAR(order_date) = 2026` disables B-tree seeks; write `WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31'`).

### Index Data Structures
1. **B+ Tree (Default General-Purpose Index):**
   ```mermaid
   flowchart TD
       Root["Root Node: [50]"] --> IntL["Internal: [20]"]
       Root --> IntR["Internal: [80]"]
       IntL --> L1["Leaf: 10, 15 -> Ptr"]
       IntL --> L2["Leaf: 20, 30 -> Ptr"]
       IntR --> L3["Leaf: 50, 60 -> Ptr"]
       IntR --> L4["Leaf: 80, 99 -> Ptr"]
       L1 <--> L2
       L2 <--> L3
       L3 <--> L4
   ```
   - **Internal nodes** hold only routing keys and child pointers (sized to disk pages like 8KB, maximizing **fan-out**); **leaf nodes** hold keys + pointers (or clustered rows) connected in a **doubly-linked list** for rapid range scans.
   - **Fan-Out Math ($1{,}000{,}000$ rows):** A Binary Search Tree (fan-out 2) needs $\log_2(10^6) \approx \mathbf{20}$ disk I/Os. A B+ Tree with fan-out 500 needs only $\log_{500}(10^6) \approx \mathbf{3}$ disk I/Os! (Step-by-step lookup of `user_id = 8675309` across 10M rows takes $\sim 23$ comparisons instead of 10 million scans.)
2. **Hash Index:** $\mathcal{O}(1)$ exact-match equality (`=`) lookups; **useless** for `<`, `>`, `BETWEEN`, `ORDER BY`, or `LIKE 'A%'`. **Static Hashing** suffers overflow chains degrading to $\mathcal{O}(N)$; **Dynamic (Extendible) Hashing** doubles directory depth via hash bit prefixes and splits only overflowing buckets, preserving $\mathcal{O}(1)$.
3. **Bitmap Index:** Stores bit arrays per value (`Gender = 'M'`: `[1,0,1]`, `'F'`: `[0,1,0]`) for **low-cardinality** warehouse columns; evaluates `AND`/`OR`/`COUNT` via native CPU bitwise instructions, but locks segments poorly under OLTP writes.
