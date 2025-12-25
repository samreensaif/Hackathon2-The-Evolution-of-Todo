---
title: BetterAuth Integration Spike
feature: todo-app
created: 2025-12-25
owner: architecture
---

# BetterAuth Integration Spike — Phase II

Summary
- This spike evaluates two integration approaches for authentication with BetterAuth and documents a recommended approach for Phase II (no code included).

Objectives
- Verify options for token ownership and verification.
- Document pros/cons, operational considerations, and recommended approach.
- Produce a checklist for the implementation task (T006) that follows.

Background
- The plan requires authentication using BetterAuth and JWTs. The open question: should the backend trust BetterAuth‑issued tokens directly, or should it verify BetterAuth credentials and then issue its own signed JWTs to clients?

Options Evaluated

- Option A — Trust BetterAuth tokens directly
  - Flow: Client authenticates with BetterAuth, receives a BetterAuth JWT; client sends that token to our API; backend verifies token signature and claims against BetterAuth's JWKS.
  - Pros:
    - Centralized identity: auth decisions, rotation, and policies live in BetterAuth.
    - Simpler server logic (no token issuance responsibility).
    - Single source of truth for sessions and revocation (if BetterAuth supports revocation/blacklist).
  - Cons:
    - Less control over token contents/claims (can't add app‑specific claims easily).
    - Revocation/refresh behavior depends on BetterAuth features; if BetterAuth doesn't support server‑side revocation, short TTLs are required.
    - More coupling to BetterAuth token formats and rotation cadence.

- Option B — Backend issues its own JWTs after verifying BetterAuth
  - Flow: Client authenticates with BetterAuth (or via backend exchange). Backend verifies BetterAuth proof, then issues a short‑lived access JWT (and optional refresh token) signed by our service for API access.
  - Pros:
    - Control: backend can include app‑specific claims (`roles`, `features`) and control token TTLs.
    - Easier local revocation strategies (refresh token rotation, server side blacklist if needed).
    - Decouples API token format from BetterAuth, easing future provider changes.
  - Cons:
    - Increased complexity: backend must implement secure token issuance, storage for refresh tokens (if used), and rotation logic.
    - Additional operational responsibility (signing keys, rotation, and secure storage).

Technical & Operational Considerations
- Token signing keys: for Option B we need secure key management (KMS or platform secret manager) and rotation strategy.
- Refresh tokens: if used, prefer httpOnly cookies for refresh tokens and store minimal server state for rotation if implementing rotating refresh tokens.
- Token validation: for Option A the backend must fetch and cache BetterAuth JWKS and validate `exp`, `iss`, and `aud` claims.
- Latency and availability: Option A relies on BetterAuth's token ingestion and JWKS availability; caching JWKS mitigates transient issues.
- Compliance and auditing: Option B allows adding fine‑grained app claims useful for auditing; Option A centralizes audit data at BetterAuth.

Recommendation (Phase II)
- Recommend Option B (backend‑issued JWTs after verifying BetterAuth) as the default for Phase II, with this rationale:
  - Gives the project control over token TTLs and app‑specific claims needed for authorization and future features.
  - Eases transition between identity providers in the future.
  - Enables implementing refresh token rotation and pragmatic revocation strategies without relying solely on external provider features.
- Accept Option A only if the team prefers minimal backend responsibilities and BetterAuth provides first‑class session/revocation features that meet product requirements.

Spike Acceptance Criteria (met)
- [x] Decision recorded: prefer Option B (backend‑issued JWTs) with tradeoffs noted.
- [x] Integration checklist drafted for implementation task T006.

Implementation Checklist (for T006 / next tasks)
- Decide token model: access token TTL (e.g., 15m) and refresh token TTL (e.g., 7d) or no refresh tokens.
- Key management: choose storage for signing keys (KMS, secrets manager) and rotation policy.
- Token format: define claims (`sub`, `exp`, `iat`, `roles`, `email`) and JWT signing algorithm (e.g., RS256 or ES256).
- Refresh token strategy: rotating refresh tokens vs. long‑lived refresh tokens; storage and revocation approach.
- JWKS integration: backend still needs to verify BetterAuth artifact during initial exchange (if using Option B), so implement JWKS fetch/caching.
- Security hardening: rate limiting on auth exchange, brute‑force protections, and secure cookie usage for refresh tokens.

Next Steps
- Create T006 (auth middleware) implementing token verification for backend‑issued JWTs.
- Create a small integration test that exercises token issuance and verification in staging.
- Document secrets and env vars required (KMS key name, `JWT_PRIVATE_KEY` or issuer config).

References
- BetterAuth docs (link): (add link during implementation)
- JWT RFC 7519 and recommended best practices for token lifecycle and storage.
