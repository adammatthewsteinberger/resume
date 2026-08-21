# Adam Matthew Steinberger

**Staff Software Architect & AI Automation Engineer** — RAG systems, event-driven Azure microservices, and automation pipelines that the people who inherit them can actually run.

Greenville, SC (remote / US remote) · [+1-864-517-4117](tel:+18645174117) · [adam@matthewsteinberger.com](mailto:adam@matthewsteinberger.com) · [linkedin.com/in/adammatthewsteinberger](https://www.linkedin.com/in/adammatthewsteinberger/) · [github.com/adammatthewsteinberger](https://github.com/adammatthewsteinberger) · [hire.adam.matthewsteinberger.com](https://hire.adam.matthewsteinberger.com)

> Available September 2026 for Staff Software Architect, AI Automation Engineer, Staff/Principal AI Engineer, Solutions Architect, or Platform/Automation Engineer roles — W2 preferred, contract-to-hire OK.

## Summary

I build AI systems that actually work inside enterprise environments — production-grade platforms that handle real data, real security requirements, and real organizational complexity, *not demos*. **13+ years** across AI, cloud, fintech, insurance, healthcare, and cybersecurity. Most recently: **sole architect of a multi-vendor AI governance gateway**, **co-lead of a 20-microservice AI payroll platform**, author of two identity-governance-as-code control planes and the shared Python platform library adopted by 17+ repositories — all on private AKS with secretless (OIDC / workload identity) delivery and supply-chain security in CI. The work starts with a business problem nobody has solved cleanly and ends with **something the people who inherit it can run** — architecture documented before code, junior developers trained in parallel, handoffs that hold. I document everything for the same reason a RAG pipeline cites its sources.

## Core Skills

- **AI & LLM Systems:** RAG and vector search (pgvector, FAISS, Azure AI Search, Pinecone), multi-vendor LLM gateways with cost/policy governance, AI agents and multi-agent orchestration, MCP servers, structured outputs, HITL gating, LoRA fine-tuning; Azure OpenAI/Foundry, Claude, GPT, Gemini, Grok, Mistral, vLLM, Ollama, LangChain, Document Intelligence, Content Safety; OWASP LLM Top 10 / NIST AI RMF
- **Azure & Cloud:** AKS (private clusters, workload identity, KEDA), Functions, App Service, Service Bus, Event Hubs, Key Vault, App Configuration, App Insights/OpenTelemetry, Data Explorer (KQL), Cosmos DB, PostgreSQL, Redis, Blob/Data Lake, App Gateway + WAF, Private Endpoints, Entra ID, Microsoft Graph; sovereign/government cloud; AWS (Textract, Lambda, S3)
- **Platform, DevSecOps & Delivery:** Terraform, Bicep, Helm, Kustomize, Flux/Argo CD GitOps, Docker, GitHub Actions (OIDC federated credentials, self-hosted runners), build-once/promote-by-digest; Trivy, Semgrep, CodeQL, Bandit, Gitleaks/TruffleHog, Checkov, pip-audit, SBOM (Syft/CycloneDX), Cosign keyless signing, Kyverno/OPA admission; threat modeling (STRIDE), SOC 2 readiness, ADRs
- **Identity & Governance:** Okta (core, IGA, Workflows), Microsoft Entra ID, SAML 2.0, OIDC/OAuth 2.0, workload identity federation, RBAC (control and data plane), governance-as-code reconciliation, SOX-aligned access governance, GxP-classified functional specifications
- **Languages & Frameworks:** Python 3.11/3.12 (FastAPI, Flask, SQLAlchemy 2, Pydantic, kopf), TypeScript/NestJS, Next.js 15/16 + React 19, C#/.NET (Web API, MVC), Java Spring Boot, gRPC/REST, OpenAPI 3.1, Bash, SQL, KQL
- **Quality & Data:** pytest, Hypothesis, mutmut, contract/e2e/chaos tests, mypy --strict, ruff, import-linter-enforced onion architecture; PostgreSQL, MongoDB, Snowflake, SQL Server, Oracle, Redis; ETL/API integrations (HubSpot, SharePoint, Salesforce, Outlook)
- **Delivery & Leadership:** Discovery → documented solution → Jira decomposition → mentored handoff; Scrum (CSM), Security-First Scrum (author), evidence-based delivery (DORA/CHAOS/QSM), architecture documentation, mentoring

## Experience

### The Vizius Group — Senior Azure and AI Development Engineer
*Sep 2025 – Aug 2026 · Greenville, SC*

- **AI governance gateway** _(sole architect, ~54k LOC)_ — one policy-enforced, OpenAI-compatible API in front of the full Azure AI surface plus Anthropic, OpenAI/Codex, Cursor, Grok, and Gemini: per-project allowlists, allow/deny/fallback policy with hot reload, multi-unit Redis rate limiting, per-call USD cost attribution with enforced spend caps (denial-of-wallet control), and an HMAC-signed, hash-chained, write-once audit trail; Entra ID app-role auth over workload identity — **no API keys in the path**. Agent sandboxing, egress policy, and SSRF checks mapped to OWASP LLM Top 10 / NIST AI RMF; Python SDK, CLI, MCP server, Next.js admin portal; 9 autoscaled pods on private AKS via GitOps. **Migrated three product teams onto it** and retired their app-held credentials.
- **AI payroll automation platform** _(co-lead, ~420k LOC)_ — 20 microservices in an onion-architecture monorepo across four human-approved phases with the final submission modeled as irreversible; RAG over the document store, AI-directed spreadsheet corrections, earnings and report review. Owned Terraform, 20 Helm charts, Kustomize, GitOps, and 10 CI/CD workflows; 585 test modules across unit/integration/contract/e2e/smoke. Architecture **production-ready at day 45**; a junior developer trained in parallel now owns it.
- **Technical report generation platform** _(lead, ~54k LOC)_ — turns raw electrical-testing instrument data into standards-aware customer deliverables: mail-webhook ingestion with per-document fan-out, a multi-vendor parser seam, a deterministic deficiency analyzer fed by a scraped standards store plus LLM review, blocking data-quality validation, SAML 2.0 + Entra dual-issuer SSO, per-user bearer auth replacing a shared API key. **Eliminated silent false-success deploys**; authored the SOC 2 readiness assessment, threat model, ADRs, and an evidence-based delivery operating model.
- **Identity governance as code** _(sole author, two control planes)_ — a Kubernetes operator (kopf) that reconciles directory governance state against Git-declared custom resources with **fully secretless multi-tenant auth** (federated credentials, zero stored tenant secrets) and an LLM that drafts pull requests for judgment calls; and an IdP governance platform managing 40 resource kinds through six addressing patterns with drift classification (auto-remediate safe, PR + human approval for destructive), point-in-time reversion, and dual APM/SIEM log shipping. Plus a versioned, idempotent sync API for 114+ directory groups that replaced a low-code workflow.
- **Multi-system ticket relay** _(sole author, ~20k LOC)_ — N-way sync with a symmetric schema (no privileged hub): version vectors, echo suppression, a conflict policy engine that downgrades unimplemented strategies to manual hold, edge HMAC verification with vault-backed per-tenant secrets, config-driven generic connector. **653 tests, 93% coverage**, mypy --strict clean, import-linter-enforced pure domain, property/mutation/chaos tests proving convergence.
- **Multi-tenant observability portal** _(lead)_ — sub-second streaming, analytical, and federated APM/vendor/cost planes, **every payload tagged with its freshness**; CLI, REST, HMAC webhooks, MCP server, and SDK over one core; SAML SSO; KEDA.
- **vibey-bootstrap** _(formerly azure-bootstrap; open source, MIT)_ — authored the firm's shared Python platform library through three major versions on PyPI, **adopted by 17+ repositories**: four-phase logging↔config bootstrap, structured logging with correlation IDs and masking, tiered alerting, ingress classifier, dead-letter-aware consumers, ten logging transports behind a never-block/never-raise shipper, transactional outbox; 86% coverage; four platforms refactored to delete the code it replaced.
- **DevSecOps, secretless by default** — OIDC workload identity federation across 20 CI workflows in 9 repositories, managed identity at runtime, CSI-driver vault secrets; supply-chain pipelines with SAST, SCA, IaC scanning, secret detection, SBOM generation, keyless image signing, and policy-as-code admission; cleared 24 IaC policy findings; **security self-reviews** closed an auth bypass, path traversal, SSRF, timing-unsafe comparison, query injection, and an over-scoped CI credential before release. Cross-tenant production migration on OIDC and least-privilege RBAC.
- **Architecture & advisory** — **five formal architecture document sets (~180 pages)** including a three-tier package (43-page design, 10-page executive summary, one-sheet) and a STRIDE threat model; identity-governance advisory for a **SOX-regulated enterprise of ~5,700 identities** (market survey, platform decision report, API/SDK/MCP coverage assessment across eight platforms, GxP-classified functional specifications, SOX-to-IAM risk mapping); AI vendor terms comparison for legal and procurement.
- **Enablement & thought leadership** — authored *Security-First Scrum* (framework, two training manuals, four AI-agent rulesets), an evidence-based delivery velocity playbook, and a **~110,000-word technical reference library** compiled into vibey-skills (18 plugins / 71 skills); mentored junior developers on three projects; built the firm's LinkedIn thought-leadership program end to end, including a narrative white paper on export-control compliance and cloud enclave architecture produced and written from recorded expert interviews.

### The Apologist Project (volunteer) — Volunteer Software Architect — open-source-style contribution
*Apr 2026 – Present · Remote*

- **Project Excite** — designed and built an **adapter-based relay microservice** handing seekers from the AI to live volunteers on Chatwoot or EchoGlobal: abstract adapter + concrete adapters, **explicit session state machine with idempotent teardown**, Redis-backed session manager, HMAC-verified webhooks, QStash-queued delivery, shared in-session @agent. Three technical executive summaries and a unified relay schema reference written before implementation.
- **Shipped across split PR stacks** (schema, relay lib/HTTP, backend proxy, client UI, admin monitoring) plus **security hardening** (XSS via DOMPurify, CORS allowlist, Sentry PII off, rate limiting) and CI/PHPUnit repair; ~68 commits.

### Adam Matthew Steinberger LLC — Independent product design
*2026 · Greenville, SC*

- **Business plans and software architecture documents** for two SaaS concepts — a mobile-first social platform (React Native, FastAPI, Azure Container Apps) and a decentralized confidential-AI protocol.

### Adam Matthew Steinberger LLC — Senior Software Engineering Consultant
*Mar 2025 – Aug 2025 · Greenville, SC*

- **Self-hosted RAG chatbot** _(non-profit)_ — on-premise RAG on Mistral-7B + FAISS behind an OpenAI-compatible vLLM API; Grafana/Prometheus on every token; Docker on bare metal; **zero external dependencies; shipped in 30 days**.
- **Cloud RAG chatbot** _(sales agency)_ — Gemini-based RAG with API-driven web search; **shipped in 30 days**.
- **Web push notification system** _(non-profit, GodFocus)_ — timezone-aware scheduling, personalization, VAPID encryption; **159/159 tests, 85.84% coverage** via AI-assisted TDD in **5 billable hours against a 30+ hour estimate**.
- **Codebase review & architecture** _(non-profit)_ — **190+ files / 59,000 lines in 10 hours**; surfaced 5% test coverage and missing auth middleware; delivered a technical brief, executive summary, and phased Onion roadmap.

### Lima One Capital — Senior Software Engineer
*May 2023 – Feb 2025 · Greenville, SC*

- **Rearchitected the core integration layer** from legacy Mulesoft APIs into NestJS microservices (gRPC + REST) on PostgreSQL.
- **Full-stack .NET/React** work on a mortgage-broker platform: credit-report integrations and pricing-engine APIs.
- **ETL pipelines and API connectors** across HubSpot, SharePoint, Snowflake, Salesforce, and third-party providers.
- **Built Snow Portal**, a Snowflake job scheduler that **replaced Alteryx at a fraction of the cost**; automated HR-to-ITSM sync.

### Earlier experience

- **Transcat** — Senior Software Engineer, Rochester, NY (Apr 2022 – Jan 2023). *Led a team* delivering .NET Web APIs and a React front end for lab-equipment calibration; hardened the Magento channel.
- **LeaseTrack** — Senior Software Engineer, Latham, NY (Jun 2021 – Apr 2022). Python + AWS Textract insurance-document parsing, plus a Java Spring Boot annotation system feeding the ML training pipeline.
- **Akmazio Software** — Senior Software Engineer (founding engineer), Albany, NY (May 2020 – May 2021). *Founding engineer:* built the entire C#/.NET + MS SQL backend (DigitalOcean) for an advisor-matching platform; wrote the business plan, managed interns and a 1099 developer, ran a distributed Scrum test team.
- **Bestpass by Fleetworthy** — Software Engineer, Albany, NY (Sep 2019 – Apr 2020). Toll-billing system in C# MVC + Knockout.js; *introduced automated unit testing* to a legacy codebase that had none.
- **New York State Insurance Fund (NYSIF)** — Software Engineer, Albany, NY (Mar 2015 – Aug 2019). *Migrated VB6 systems to C# MVC*, refactored Oracle EDI integrations, mentored juniors, standardized engineering process.
- **Town and Country Computer Services** — Junior Software Engineer, Schenectady, NY (Jul 2013 – Mar 2015). C# ASP.NET / SQL Server quoting, rating, and reporting apps used all day by insurance underwriters; *client-facing from day one*.
- **GE HealthCare** — Junior Software Engineer, Barrington, IL (Aug 2012 – Feb 2013). Zero Footprint (ZFP), a browser-based JavaScript CT/MRI viewer for real-time 3D scrolling; *built the full i18n feature*. First Scrum team.

## Open Source

- **[claudeloop](https://github.com/adammatthewsteinberger/claudeloop) · [codexloop](https://github.com/adammatthewsteinberger/codexloop) · [cursorloop](https://github.com/adammatthewsteinberger/cursorloop) · [agyloop](https://github.com/adammatthewsteinberger/agyloop) · [vibey](https://github.com/adammatthewsteinberger/vibey)** — Onion-architected autonomous session runners for Claude Code, OpenAI Codex, Cursor Agent, and Google Antigravity _(never block on a human; distinguish rate-limit windows from exhausted credits)_ and **vibey**, the six-phase PostgreSQL-backed conductor on top of them.
- **[vibey-bootstrap](https://github.com/adammatthewsteinberger/vibey-bootstrap) · [vibey-skills](https://github.com/adammatthewsteinberger/vibey-skills)** — The Azure Functions cross-cutting layer _(formerly azure-bootstrap; 17+ repos)_ and an **18-plugin / 71-skill** Claude Code marketplace _(formerly vibe-engineering-skills)_.

All MIT-licensed, on PyPI — [hire.adam.matthewsteinberger.com/open-source](https://hire.adam.matthewsteinberger.com/open-source)

## Publications

- **[Novice to Navigator: Your Guide to AI Chatbots for Business](https://hire.adam.matthewsteinberger.com/novice-to-navigator)** — Plain-English guide to RAG chatbots for decision-makers; **first edition free online**, second edition in development _(ISBN 979-8274310628)_.

## Education & Certifications

- **Skidmore College** — B.A., Computer Science (2010 – 2012)
- **Rensselaer Polytechnic Institute** — Electrical and Electronics Engineering (2008 – 2010)
- **Certified ScrumMaster (CSM)** — Scrum Alliance (2021)

---

Formats: [PDF](adam-steinberger-resume.pdf) · [DOCX](adam-steinberger-resume.docx) · [TXT](adam-steinberger-resume.txt) · [Scrum certificate](scrum-certificate.pdf) · Everything else: [hire.adam.matthewsteinberger.com/hire-me](https://hire.adam.matthewsteinberger.com/hire-me)
