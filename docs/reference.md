# Bucket v1 Reference Documentation

## 1. Overview

**Purpose:**
Bucket v1 is a storage-only service responsible for the immutable storage and retrieval of versioned artifacts with cryptographic provenance guarantees. It is a low-level data layer service — it does not interpret, process, or manage business logic for stored artifacts.

**Core Guarantees:**

* **Immutable Storage:** Once written, artifact bytes cannot be modified or deleted.
* **Provenance & Integrity:** Every artifact is referenced by a content-derived cryptographic digest (SHA-256). Stored data integrity is verifiable at any time.
* **Versioning:** Every artifact version is retained; historical versions remain accessible via their digest.

**Explicit Non-Responsibilities:**

* ❌ No artifact validation (beyond integrity checks)
* ❌ No artifact lifecycle or retention policies
* ❌ No access control or authentication (handled upstream)
* ❌ No semantic understanding of artifact contents
* ❌ No indexing, search, or cataloging beyond direct digest lookup

## 2. Schemas

### 2.1 Artifact Metadata

Stored as JSON alongside each artifact.

```json
{
  "bucket_id": "string",
  "artifact_id": "string",
  "version": "string",
  "digest": "string",
  "size_bytes": "integer",
  "created_at": "ISO 8601 timestamp",
  "uploaded_by": "string",
  "provenance_source": "string"
}
```

**Field Definitions:**

* **bucket_id:** Logical grouping identifier.
* **artifact_id:** Unique identifier for the artifact type.
* **version:** User-defined version string.
* **digest:** SHA-256 hash of the artifact bytes.
* **size_bytes:** Exact byte count of artifact.
* **created_at:** Timestamp of artifact creation (from client).
* **uploaded_by:** Identity of uploader (from client context).
* **provenance_source:** Originating system or pipeline identifier.

### 2.2 Error Response Schema

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## 3. Endpoints

### 3.1 PUT /v1/{bucket_id}/{artifact_id}

Upload a new artifact version.

**Request:**

**Headers:**

* `X-Artifact-Version: {version}`
* `X-Artifact-Digest: sha256:{hex_digest}`
* `X-Uploaded-By: {identity}`
* `X-Provenance-Source: {source}`
* `Content-Type: application/octet-stream`

**Body:** Raw artifact bytes.

**Validation (Storage-Only):**

* Computes SHA-256 of request body.
* Verifies computed digest matches `X-Artifact-Digest`.
* Rejects if size exceeds system limits (configuration-driven).
* Does not validate artifact semantics, structure, or version ordering.

**Response:**

* `201 Created` on success.
* `400 Bad Request` if digest mismatch or missing required headers.
* `409 Conflict` if identical digest already exists for same `(bucket_id, artifact_id, version)`.
* **Idempotency:** Uploading identical `(bucket_id, artifact_id, version, digest)` returns `200 OK`.

### 3.2 GET /v1/{bucket_id}/{artifact_id}

Retrieve artifact metadata and/or content.

**Query Parameters:**

* `version` (Required): Target version.
* `digest` (Optional): Specific digest to verify.
* `metadata_only` (Optional): If true, returns only metadata.

**Response:**

* `200 OK` with artifact bytes (or metadata JSON if `metadata_only=true`).
* `404 Not Found` if artifact does not exist.
* `412 Precondition Failed` if `digest` param provided and does not match stored digest.

### 3.3 GET /v1/{bucket_id}/{artifact_id}/versions

List all stored versions for an artifact.

**Response:**

```json
{
  "versions": [
    {
      "version": "string",
      "digest": "string",
      "size_bytes": "integer",
      "created_at": "string"
    }
  ]
}
```

## 4. Storage Guarantees & Constraints

### 4.1 Provenance Chain

* Artifact identity = `(bucket_id, artifact_id, version, digest)`.
* Digest is computed client-side and verified server-side.
* Any tampering with stored bytes will be detected upon retrieval (digest mismatch).
* Timestamp and source metadata are provided by client and stored as-is; no server-side validation of these fields.

### 4.2 Immutability

* No updates or deletions allowed via Bucket v1 API.
* Storage layer may replicate for durability, but bytes are never altered.
* Artifact aging/cleanup (if any) is managed by infrastructure, not Bucket v1 business logic.

### 4.3 Limitations

* Maximum artifact size: 5 GiB (configurable, but fixed per deployment).
* No atomic transactions across artifacts.
* No consistency guarantees across regions (active-passive replication only).
* Listing operations (`/versions`) may have eventual consistency characteristics.

## 5. Usage Examples

### 5.1 Upload Artifact

```bash
curl -X PUT \
  -H "X-Artifact-Version: 2.1.0" \
  -H "X-Artifact-Digest: sha256:abc123..." \
  -H "X-Uploaded-By: build-server-01" \
  -H "X-Provenance-Source: ci-pipeline-42" \
  --data-binary @artifact.tar.gz \
  https://bucket.example.com/v1/my-bucket/my-app
```

### 5.2 Retrieve with Digest Verification

```bash
curl "https://bucket.example.com/v1/my-bucket/my-app?version=2.1.0&digest=sha256:abc123..."
```

### 5.3 Retrieve Metadata Only

```bash
curl "https://bucket.example.com/v1/my-bucket/my-app?version=2.1.0&metadata_only=true"
```

## 6. Operational Notes

* **Monitoring:** Metrics exposed for upload counts, bytes stored, digest verification failures.
* **Logging:** All operations logged with `(bucket_id, artifact_id, version, digest, actor)`.
* **Backward Compatibility:** This documentation reflects the actual v1 API behavior; no undocumented features or side-effects exist.
* **Failure Modes:** Network timeouts, storage unavailability, or corruptions detectable via digest mismatch.
