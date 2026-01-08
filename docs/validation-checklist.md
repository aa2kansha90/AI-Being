# Bucket v1 Client-Side Validation Checklist

## Purpose

This checklist defines non-semantic validation that should be performed client-side before writing artifacts to Bucket v1. These checks ensure basic data quality and prevent technically invalid writes without interpreting artifact content or making policy decisions.

## 1. Metadata Validation

### 1.1 Required Fields Presence

✅ Check that all required metadata fields are present and non-empty:

* bucket_id
* artifact_id
* version
* digest (SHA-256, prefixed with sha256:)
* size_bytes
* created_at (ISO 8601 format)
* uploaded_by
* provenance_source

❌ Do NOT validate:

* Whether bucket_id corresponds to an existing bucket
* Whether artifact_id follows naming conventions
* Semantic meaning of any field

### 1.2 Field Format Validation

✅ Validate basic format constraints:

* bucket_id: 1-255 chars, alphanumeric plus -, _, .
* artifact_id: 1-255 chars, alphanumeric plus -, _, .
* version: 1-100 chars, not empty
* digest: Matches `^sha256:[a-fA-F0-9]{64}$`
* size_bytes: Integer > 0 and ≤ configured max (e.g., 5 GiB)
* created_at: Valid ISO 8601 timestamp, not in the future
* uploaded_by: Non-empty, 1-500 chars
* provenance_source: Non-empty, 1-500 chars

❌ Do NOT validate:

* Whether created_at is reasonable beyond future check
* Whether uploaded_by corresponds to a real user/system
* Whether provenance_source is legitimate

## 2. Provenance Identifiers Validation

### 2.1 Digest Consistency

✅ Verify cryptographic integrity:

* Compute SHA-256 of actual artifact bytes
* Compare computed digest with metadata digest
* Require exact match (case-insensitive for hex portion)

✅ Verify digest uniqueness per context:

* Check in external registry that `(bucket_id, artifact_id, version, digest)` doesn't already exist

❌ Do NOT validate:

* Cryptographic strength beyond SHA-256
* Matching digest with external system expectations

### 2.2 Provenance Chain Basic Checks

✅ Verify minimal provenance linkage:

* `provenance_source` should not be empty or "unknown"
* `uploaded_by` should not be "system" or generic
* Both fields contain identifiable information

✅ Log provenance for audit trail:

* Record `{artifact_id, version, uploaded_by, provenance_source, timestamp}`
* Store separately from Bucket (application logs)

❌ Do NOT validate:

* Authorization of provenance_source
* Permission of uploaded_by
* Semantic relationship between source and artifact

## 3. Version Identifiers Validation

### 3.1 Version Format & Uniqueness

✅ Check version string validity:

* Not empty
* Does not contain invalid characters (`/ \ : * ? " < > |`)
* Length ≤ 100 chars

✅ Ensure version uniqueness:

* `(bucket_id, artifact_id, version)` unique in external registry
* Reject if same tuple exists with different digest (version conflict)

❌ Do NOT validate:

* Semantic versioning compliance
* Version ordering or sequence
* Whether version "makes sense" for artifact type

### 3.2 Version Stability Checks

✅ Verify version doesn't change for same content:

* Same `(bucket_id, artifact_id, digest)` must use same version
* Reject version hijacking

❌ Do NOT validate:

* Version increment rules
* Correspondence to release status (alpha/beta/stable)

## 4. Size & Structural Validation

### 4.1 Size Boundaries

✅ Check practical limits:

* Minimum size > 0 bytes
* Maximum ≤ Bucket's configured limit
* Warn if > warning threshold (e.g., 1 GiB)

✅ Verify size matches actual bytes

❌ Do NOT validate:

* Appropriateness for artifact type
* Compression ratio or efficiency

### 4.2 Basic Structural Soundness

✅ Check for obvious corruption:

* JSON parsable if content-type JSON
* GZIP magic bytes if file extension suggests compressed
* No embedded null bytes in metadata strings

❌ Do NOT validate:

* Schema compliance
* Data correctness or quality
* Format version compatibility
* Encoding beyond basic UTF-8 check

## 5. Contextual Validation (Non-Semantic)

### 5.1 Rate & Volume Limits

✅ Client-side throttling:

* Maximum uploads per minute
* Maximum data volume per hour
* Reject if exceeded

✅ Check quota availability if using quotas

❌ Do NOT validate:

* Business justification for volume

### 5.2 Temporal Consistency

✅ Check for time anomalies:

* `created_at` not in future (+5 min skew allowed)
* Not unreasonably past (>30 days)
* Log warnings

✅ Verify operation sequence:

* If previous version exists, `created_at` ≥ previous
* Allow equal timestamps for batch uploads

❌ Do NOT validate:

* Actual creation time accuracy
* Business timeline compliance

## 6. Checklist Summary Table

| Validation Category | Must Check                              | Must NOT Check                    |
| ------------------- | --------------------------------------- | --------------------------------- |
| Metadata Presence   | All required fields present             | Whether fields are meaningful     |
| Field Format        | Basic syntax, length limits             | Semantic correctness              |
| Digest              | SHA-256 format, matches bytes           | Cryptographic strength assessment |
| Provenance          | Non-empty, identifiable values          | Authorization or legitimacy       |
| Version             | Unique per artifact, basic syntax       | Version ordering, semantics       |
| Size                | >0, ≤max, matches actual bytes          | Appropriateness for content       |
| Structure           | No null bytes, parsable if known format | Schema compliance, data quality   |
| Rate Limits         | Client-side throttling                  | Business justification            |
| Timestamps          | Not in future, not unreasonably past    | Actual creation time accuracy     |

## 7. Implementation Notes

### 7.1 Validation Order

* Fast failures first: size limits, required fields
* Expensive checks last: digest computation, registry lookups
* Idempotency: Check for existing identical artifact early

### 7.2 Error Messaging

* Be specific: "digest mismatch" not "validation failed"
* Include offending value
* Suggest fix

### 7.3 Audit Trail

* Log all validation attempts (pass/fail)
* Include timestamp, client ID, artifact_id, version, validation result
* Store separately from Bucket

### 7.4 Idempotency Handling

* Identical `(bucket_id, artifact_id, version, digest)` exists: skip upload, return reference
* Same version but different digest: reject with conflict error
* Never auto-generate new versions

## 8. Example Validation Flow

1. Parse metadata → Fail if missing required fields
2. Validate field formats → Fail if syntax invalid
3. Check size limits → Fail if too large
4. Compute SHA-256 of bytes → Fail if mismatch
5. Query external registry:

   * If identical quadruplet exists → Return existing (idempotent)
   * If same version, different digest → Reject (version conflict)
   * If new version → Continue
6. Check rate limits → Fail if exceeded
7. Validate timestamps → Warn if anomalous
8. Perform basic structure check → Warn if suspicious
9. Upload to Bucket
10. Record in external registry
