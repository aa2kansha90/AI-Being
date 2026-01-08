# AI Assistant Integration Guide — Bucket v1

## Purpose

This guide explains how AI Assistant systems should interact with Bucket v1, a storage-only artifact repository. It clarifies what Bucket can and cannot do, and outlines patterns to prevent integration pitfalls.

## 1. What the AI Assistant May Store

You may store:

* Model checkpoints (weights, configurations)
* Inference results (batch outputs, evaluation predictions)
* Training artifacts (logs, metrics, hyperparameter sets)
* Dataset snapshots (preprocessed, tokenized, or sliced data)
* Generated content (text, images, structured outputs)
* System state (conversation history snapshots, session states)

**Key Principle:** Store immutable artifacts, not mutable state. Each upload is a frozen snapshot.

## 2. What Bucket v1 Is NOT (Critical Boundaries)

Bucket v1 must never be treated as:

### ❌ A Database

* No queries beyond exact `(bucket_id, artifact_id, version)` lookup
* No partial matches, no filtering by metadata, no full-text search
* No transactions or atomic multi-artifact operations

### ❌ A Configuration Store

* No last-write-wins semantics
* No automatic "latest version" resolution (track versions externally)
* No real-time updates or notifications

### ❌ A Validation Service

* Does not validate artifact formats (e.g., valid PyTorch checkpoint, correct JSON schema)
* Does not enforce version ordering (v2 can be uploaded before v1)
* Does not check semantic consistency between artifacts

### ❌ An Access Control Layer

* No built-in authentication/authorization
* No per-artifact permissions
* No audit logging beyond basic operation logs

### ❌ A Processing Pipeline

* No transformations (compression, format conversion, chunking)
* No indexing or cataloging
* No lifecycle management (automatic deletion, archiving)

## 3. Conceptual Integration Patterns

### 3.1 Write Flow: Storing AI Artifacts

**AI Assistant → Prepare Artifact → Compute Digest → Upload → Verify**

1. **Prepare Artifact**

   * Serialize data (tensors → safe tensors, logs → JSONL)
   * Add necessary metadata in your application layer

2. **Compute Digest (CLIENT RESPONSIBILITY)**

   * SHA-256 hash of exact bytes to upload
   * Must match header sent to Bucket

3. **Upload**

   * Include: version string, digest, provenance info
   * Bucket verifies ONLY: digest matches bytes

4. **Verify**

   * Store mapping: `(logical ID → bucket_id/artifact_id/version/digest)`
   * In your own database/registry

**Example: Storing a model checkpoint**

```json
// Metadata stored externally
{
  "model_name": "llama-3-8b-instruct",
  "task": "code_generation",
  "training_run": "run-47",
  "bucket_ref": "models/llama3/v3.1.0"
}
```

Bucket stores:

* bucket_id: "prod-models"
* artifact_id: "llama-3-8b-instruct"
* version: "v3.1.0"
* digest: "sha256:abc123..."
* bytes: [checkpoint file]

### 3.2 Read Flow: Retrieving for Inference/Evaluation

**Need Artifact → Lookup Reference → Fetch → Validate → Use**

1. **Lookup Reference**

   * Query YOUR registry: "latest stable model for task X"
   * Get exact tuple: `(bucket_id, artifact_id, version, digest)`

2. **Fetch**

   * Request from Bucket with all four identifiers
   * Optionally specify digest for verification

3. **Validate (RECOMMENDED)**

   * Recompute SHA-256 on received bytes
   * Compare with expected digest
   * Fail if mismatch (indicates corruption)

4. **Use**

   * Deserialize according to your format
   * Handle version compatibility in YOUR code

**Important:** Always store the digest alongside your logical references. The digest is the ground truth for artifact identity.

## 4. Rejection Scenarios & How to Handle Them

### Scenario 1: Digest Mismatch

* **Response:** 400 Bad Request
* **Reason:** Computed SHA-256 doesn't match X-Artifact-Digest header
* **Responsibility:** Retry upload with correct digest. Investigate compression/serialization differences. Never disable digest verification client-side.

### Scenario 2: Version Already Exists

* **Response:** 409 Conflict
* **Reason:** Same `(bucket_id, artifact_id, version, digest)` already stored
* **Action:** If digest differs, choose a new version string, update your external registry, and upload.

### Scenario 3: "Latest Version" Request

* Not handled by Bucket. Maintain an external registry:

  * Store `{ model_id, bucket_ref, is_latest, metadata }`
  * Update when new versions uploaded
  * Query registry, then fetch from Bucket

### Scenario 4: Artifact Too Large

* **Response:** 413 Payload Too Large
* **Reason:** Exceeds Bucket's configured limit (e.g., 5 GiB)
* **Solutions:** Implement chunking, store multiple artifacts with manifest, or consider compression (note: changes digest!).

## 5. Anti-Patterns to Avoid

* **Using Timestamps as Versions**

```yaml
# BAD
version: "2024-05-27T10:30:00Z"
# GOOD
version: "v3.1.0"
version: "run-47-checkpoint-epoch-50"
```

* **Assuming Sequential Version Availability**

```python
# BAD
for v in ["v1", "v2", "v3"]:
    fetch(bucket, artifact, v)
# GOOD
versions = list_versions(bucket, artifact)
for v in sorted(versions):
    fetch(bucket, artifact, v)
```

* **Storing Mutable State**

```python
# BAD
store("conversation_state", user_id, latest_state)
# GOOD
store("conversation_snapshot", f"{user_id}_{timestamp}", state)
```

* **Relying on Metadata for Filtering**

```python
# BAD
# "Find all artifacts where uploaded_by='training-cluster-5'"
# IMPOSSIBLE via Bucket API
# GOOD
db.query(Artifact).filter_by(uploaded_by="training-cluster-5")
```

## 6. Recommended Client-Side Patterns

### Pattern A: External Registry

```python
class ArtifactReference:
    logical_id: str      # e.g., "prod-model-llama3"
    bucket_id: str
    artifact_id: str
    version: str
    digest: str
    is_latest: bool
    metadata: JSON       # Your business metadata
```

Bucket stores only bytes + minimal metadata; relationships, tags, and descriptions stay in YOUR database.

### Pattern B: Manifest Files for Multi-Part Artifacts

```python
manifest = {
    "shards": [
        {"name": "shard_01.bin", "digest": "sha256:..."},
        {"name": "shard_02.bin", "digest": "sha256:..."}
    ]
}
```

Store manifest as artifact, store shards separately, reconstruct client-side.

### Pattern C: Content-Addressable Naming

```python
version = f"sha256-{digest[:12]}"
digest_to_logical = {"abc123...": {"model": "llama3", "version": "v3.1.0"}}
```

## 7. Security Considerations

**Client-Side Responsibilities:**

* Validate artifacts before upload (malware, format correctness)
* Implement access control in your layer (gateway, proxy, service mesh)
* Sanitize metadata (no PII in `uploaded_by` or `provenance_source`)
* Rotate credentials used to call Bucket API

**Bucket Provides:**

* Transport security (HTTPS)
* At-rest encryption (infrastructure-level)
* Digest-based integrity verification
