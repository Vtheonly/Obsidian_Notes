---
tags: [production, pii, data-leakage, privacy, compliance]
iteration: 4
created: 2026-08-08
aliases: [PII Protection, Data Leakage Prevention, Privacy in LLMs]
---

# 05 — PII and Data Leakage

> [!info] TL;DR
> PII (personally identifiable information) leakage is one of the most serious production AI risks. Three leakage paths exist: (1) **input leakage** — user PII sent to LLM providers without redaction; (2) **output leakage** — the model outputs PII from its context (training data, other users' data, retrieved documents); (3) **training data leakage** — the model memorized PII during pretraining and regurgitates it. Mitigation requires layered defense: PII detection, redaction, access control, logging restrictions, and contractual safeguards with providers.

## The Three Leakage Paths

### 1. Input Leakage
When a user submits a prompt containing PII (name, email, SSN, credit card, medical record), that PII is sent to the LLM provider. If the provider is a third party (OpenAI, Anthropic), this may violate data protection regulations (GDPR, HIPAA, CCPA) or internal data policies.

**Example**: a customer pastes their credit card number into a support chat. The LLM provider now has that number in their logs.

**Mitigation**:
- Detect and redact PII before sending to the LLM.
- Use providers with strong data retention policies (no training on user data, short retention).
- For sensitive data, use self-hosted models (no data leaves your infrastructure).

### 2. Output Leakage
The LLM outputs PII that was in its context but shouldn't be shared. This can happen through:
- **RAG retrieval**: the model retrieves a document containing other users' PII and includes it in the response.
- **Cross-conversation contamination**: a bug in memory management causes the model to see data from a different user's session.
- **System prompt leakage**: the model outputs the system prompt, which may contain sensitive configuration.

**Example**: a RAG system retrieves a customer's profile (including their SSN) and the model includes the SSN in its response to a different user.

**Mitigation**:
- Filter outputs for PII before sending to users.
- Enforce tenant isolation in RAG (queries only retrieve from the current tenant's documents).
- Sanitize retrieved documents (strip PII before adding to context).
- Audit system prompts for sensitive content.

### 3. Training Data Leakage
LLMs memorize some of their training data. If the training data contained PII (web crawls often include phone numbers, emails, addresses), the model can regurgitate it when prompted appropriately.

**Example**: asking a model "What is John Smith's phone number?" might cause it to output a real phone number from its training data.

**Mitigation**:
- Use models that were trained on deduplicated, PII-scrubbed data (most modern providers do this).
- Implement output PII filtering.
- Fine-tune on data that has been scrubbed of PII.
- Educate users not to share PII with LLMs.

## PII Detection

### Rule-Based Detection
Use regex patterns for structured PII:
- **SSN**: `\b\d{3}-\d{2}-\d{4}\b`
- **Credit card**: Luhn-valid 16-digit numbers.
- **Email**: standard email regex.
- **Phone**: country-specific patterns.

**Pros**: fast, deterministic, no model needed.
**Cons**: misses unstructured PII (names, addresses), false negatives on non-standard formats.

### Named Entity Recognition (NER)
Use an NER model (spaCy, Presidio, a fine-tuned BERT) to detect entities:
- Person names.
- Organizations.
- Locations (addresses, cities).
- Dates.
- Miscellaneous identifiers.

**Pros**: catches unstructured PII that regex misses.
**Cons**: slower than regex; may have false positives (e.g., flagging a fictional character name).

### Presidio (Microsoft)
Open-source PII detection and redaction framework. Combines regex, NER, and customizable recognizers. The de facto standard for PII handling in AI applications.

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "My SSN is 123-45-6789 and my email is john@example.com"

# Detect PII
results = analyzer.analyze(text=text, entities=["SSN", "EMAIL_ADDRESS"], language='en')

# Redact PII
anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
print(anonymized.text)  # "My SSN is <SSN> and my email is <EMAIL_ADDRESS>"
```

### LLM-Based Detection
Use a small LLM to classify whether text contains PII. More flexible than rule-based or NER, but slower and more expensive.

## Redaction Strategies

### Masking
Replace PII with a placeholder: `john@example.com` → `<EMAIL>`. Simple, reversible if you maintain a mapping.

### Hashing
Replace PII with a hash: `john@example.com` → `a3f5b2c1`. Non-reversible, but allows re-identification if needed (e.g., for analytics).

### Generalization
Replace specific PII with a category: `35 years old` → `30-40 years old`. Preserves utility for analysis while reducing identifiability.

### Synthetic Replacement
Replace real PII with synthetic data: `john@example.com` → `user123@example.com`. Useful for testing and demos.

### Tokenization
Replace PII with a token that maps back to the original via a secure lookup. Allows the LLM to "see" the PII (via the token) without it being in plaintext.

## Access Control

### Tenant Isolation
In multi-tenant systems, enforce strict isolation:
- Each tenant's data is in a separate schema or has row-level security.
- Queries are scoped to the current tenant (no cross-tenant retrieval).
- Memory is per-tenant (no shared conversation state).

Without this, RAG retrieval can return documents from other tenants — a critical data leakage risk.

### Role-Based Access Control (RBAC)
Different users have different access levels:
- **Read access**: can query documents.
- **Write access**: can add documents.
- **Admin access**: can manage tenants, configure models.

Enforce RBAC at the application layer, not just at the LLM level. The LLM cannot be trusted to enforce access control — it can be tricked via prompt injection.

### Audit Logging
Log every access to sensitive data:
- Who accessed what document when.
- What was retrieved in RAG queries.
- What was sent to the LLM.

Audit logs are essential for compliance (GDPR, HIPAA) and for investigating incidents.

## Provider Considerations

### Data Retention Policies
Different LLM providers have different data retention policies:
- **OpenAI (API)**: retains data for 30 days for abuse monitoring, then deletes. Does not use API data for training (as of 2023).
- **Anthropic (API)**: similar to OpenAI; does not use API data for training.
- **Google (Vertex AI)**: configurable retention; does not use customer data for training by default.
- **Self-hosted (vLLM, Ollama)**: no data leaves your infrastructure.

For sensitive data, self-hosting is the safest option. If using a third-party provider, review their data retention and training policies carefully.

### Enterprise Agreements
For enterprise deployments, negotiate:
- **Zero data retention**: provider does not retain any data after processing.
- **No training on customer data**: explicit contractual prohibition.
- **Data residency**: data is processed only in specified regions.
- **Audit rights**: you can audit the provider's compliance.

### API Configuration
Some providers offer configuration options:
- **OpenAI zero retention**: available for eligible customers with enterprise agreements.
- **Azure OpenAI**: data is processed in your Azure region, with enterprise-grade compliance.
- **AWS Bedrock**: data stays in your AWS account, with HIPAA/GDPR compliance.

## Compliance Considerations

### GDPR (European Union)
- **Right to be forgotten**: users can request deletion of their data, including from model training data.
- **Data minimization**: only collect PII necessary for the purpose.
- **Cross-border transfer restrictions**: PII cannot leave the EU without adequate safeguards.

### HIPAA (United States, healthcare)
- **Protected Health Information (PHI)**: medical data requires special handling.
- **Business Associate Agreement (BAA)**: required with any third party that handles PHI.
- **Audit trails**: required for all PHI access.

### CCPA/CPRA (California)
- **Right to know**: users can request what data is collected.
- **Right to delete**: users can request deletion.
- **Right to opt out of sale**: users can opt out of data "sale" (broadly defined).

### Industry-Specific Regulations
- **FINRA** (finance): communication retention and monitoring.
- **FERPA** (education): student data privacy.
- **COPPA** (children): data collection from children under 13.

## Common Pitfalls

### Logging PII
Application logs capture PII (e.g., logging the full prompt for debugging). This violates compliance regulations. Scrub PII from logs; restrict access to logs containing sensitive data.

### No Tenant Isolation in RAG
A RAG system retrieves documents across all tenants because the vector DB doesn't enforce tenant scoping. Critical data leakage risk. Use row-level security or per-tenant indexes.

### Trusting the LLM with Access Control
The LLM decides what data to retrieve or output based on prompts. Prompt injection can bypass this. Enforce access control in application code, not in prompts.

### Sending PII to Third-Party Providers
Without redaction, user PII goes directly to OpenAI/Anthropic. Use PII detection and redaction before any third-party API call.

### No Audit Trail
Without audit logs, you cannot investigate incidents or comply with regulations. Log every access to sensitive data.

### Memorized PII in Models
Fine-tuning on data containing PII can cause the model to memorize and regurgitate it. Scrub PII from fine-tuning data; use deduplication to reduce memorization.

## See Also

- [[01 - LLM Security and Prompt Injection]]
- [[02 - Reference Production Architectures]]
- [[03 - Gateway and Router Patterns]]
- [[04 - Guardrails]]
- [[06 - Failure Modes and Graceful Degradation]]
- [[22 - Production AI/MOC|22 Production AI MOC]]
