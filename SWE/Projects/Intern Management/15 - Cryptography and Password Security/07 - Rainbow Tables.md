---
tags: [concept, cryptography, rainbow-tables, attacks]
type: concept
status: complete
prerequisites:
  - [[15 - Cryptography and Password Security/08 - Salt (and why it matters)]]
---

# Rainbow Tables

## What it is

A **rainbow table** is a pre-computed table of hash → password pairs. An attacker with a stolen hash DB looks up each hash in the table to find the password instantly.

## How it works

1. Attacker generates all possible passwords up to length N.
2. Hashes each one with the target algorithm (e.g., SHA-256).
3. Stores (hash, password) pairs in a lookup table.

For 8-character passwords using ASCII 33-126 (94 characters):
- Number of combinations: 94^8 ≈ 6 × 10^13.
- Storage: 6 × 10^13 × (32 bytes hash + 8 bytes password) = 2.4 PB.

Too much storage. Rainbow tables use a clever time-space tradeoff (hash chains) to reduce storage to ~100 GB while keeping lookup fast.

## Why the project is vulnerable

The project uses **unsalted SHA-256**. An attacker who steals the DB:
1. Downloads a pre-built SHA-256 rainbow table (~100 GB, available online).
2. For each `password_hash` in the DB, looks up the table.
3. Recovers most passwords in seconds.

If 100 users have "password123", the attacker cracks all 100 with one lookup.

## How salt defeats rainbow tables

With salt, each password has a unique hash. The attacker would need a separate rainbow table per salt. With 16-byte salts (2^128 possibilities), this is infeasible.

Even if the attacker knows the salt (it's stored next to the hash), they must re-compute the hash for each password × each salt — brute force, not lookup.

## Project Connection

The project's `toolkit.hashIt` uses no salt. The `salt` column in the DB is always NULL. Rainbow tables crack the entire DB in one pass.

The fix: Argon2id (auto-salts) or BCrypt (auto-salts). See [[15 - Cryptography and Password Security/01 - Argon2id]].

## Further reading

- Oechslin, "Making a Faster Cryptanalytic Time-Memory Trade-Off" (2003).
