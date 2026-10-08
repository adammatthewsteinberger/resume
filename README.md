# Adam Matthew Steinberger

**Staff Software Engineer · AI platforms, identity and agent infrastructure**

I build AI platforms that other teams can safely build on: no stored secrets, every call on the record, and a person signing off on anything that can't be undone.

Greenville, SC (US remote) · [+1-864-517-4117](tel:+18645174117) · [adam@matthewsteinberger.com](mailto:adam@matthewsteinberger.com) · [linkedin.com/in/adammatthewsteinberger](https://www.linkedin.com/in/adammatthewsteinberger/) · [github.com/adammatthewsteinberger](https://github.com/adammatthewsteinberger) · [vibewithadam.matthewsteinberger.com](https://vibewithadam.matthewsteinberger.com)

[![vibey on PyPI](https://img.shields.io/pypi/v/vibey-engine?label=vibey)](https://pypi.org/project/vibey-engine/) [![Code: MIT](https://img.shields.io/badge/code-MIT-yellow.svg)](LICENSE) [![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

> Available now for Staff+ engineering roles and fixed-scope contract work. US-remote.

**[Contribute to vibey](#open-source)** · [Hire me for a fixed-scope project](#fixed-scope-engagements) · [Hire me full-time](#experience)

For 14 years I've built production software for insurance, lending, healthcare and security teams. Lately I build the controls that let AI run safely inside them. My work is identity-first: workload identity instead of stored keys, audit trails that can't be quietly edited, and policy kept in Git where it can be reviewed. I write the architecture down before the code, train the people who will own it, and hand over systems that keep running after I leave. Since August I've built vibey in the open: a conductor for AI coding agents.

## Open source

**[vibey](https://github.com/the-vibey-project/vibey)** is where most of my current work happens. If you've left an AI coding agent running overnight, you've met the gap it fills. An agent can finish a task, but it can't interview you until the spec is sharp, keep going when one vendor's credits run out, or remember what was decided after a crash. vibey keeps all of that in a PostgreSQL ledger instead of a chat session, and moves work between engines without losing an open question.

```bash
uv tool install vibey-engine    # or: pipx install vibey-engine
```

Setup, including PostgreSQL, is in the [install guide](https://github.com/the-vibey-project/vibey#install). The [design paper](https://the-vibey-project.github.io/vibey/main/paper.pdf) explains why it works the way it does.

**Good ways in, if you'd like to help:**

- **Add an engine.** Each coding agent runs behind one engine contract, checked by a conformance suite (`vibey doctor --conformance`). Another agent CLI is a well-bounded first contribution.
- **Write a skill.** vibey-skills is a 140-plugin Claude Code marketplace, and a plugin is mostly Markdown. If you know a field well, that knowledge is useful there.
- **Try to break it.** Run it on a real repository and open an issue for whatever surprised you. The [contributing guide](https://github.com/the-vibey-project/vibey/blob/develop/CONTRIBUTING.md) is command-level, and it treats anything unclear as a bug in the guide.

[Contributing](https://github.com/the-vibey-project/vibey/blob/develop/CONTRIBUTING.md) · [Open issues](https://github.com/the-vibey-project/vibey/issues) · [Docs](https://the-vibey-project.github.io/vibey/main/) · [Volunteer with me](https://vibewithadam.matthewsteinberger.com/join-me)

**This repository is a small tool too.** [`tools/build_resume.py`](tools/build_resume.py) is one Python file that renders this page, the PDF, Word and text résumés, a [JSON Resume](resume.json) file and [`llms.txt`](llms.txt) from a single set of facts, so no format can drift from another. The code is MIT; fork it for your own résumé.

## Fixed-scope engagements

If you need one of these outcomes, I have delivered it before. Each one is sold as a fixed scope, with the deliverables and an acceptance checklist agreed in writing before work starts.

| Engagement | What you get |
|---|---|
| **[AI codebase and security review](SERVICES.md#ai-codebase-and-security-review)** | A severity-ranked findings report, a one-page executive summary and a phased roadmap. |
| **[Production RAG chatbot in 30 days](SERVICES.md#production-rag-chatbot-in-30-days)** | A chatbot that answers from your documents and cites them, with evaluation, monitoring and a handoff. |
| **[LLM cost and policy gateway](SERVICES.md#llm-cost-and-policy-gateway)** | One API in front of your AI vendors, with spend caps, allowlists and a tamper-evident audit trail. |
| **[Okta and Entra ID governance fixes](SERVICES.md#okta-and-entra-id-governance-fixes)** | An access review, then groups, roles and policy managed from Git with drift detection. |
| **[SOC 2 and OWASP LLM Top 10 readiness for an AI feature](SERVICES.md#soc-2-and-owasp-llm-top-10-readiness-for-an-ai-feature)** | A threat model and a control-gap list mapped to SOC 2, the OWASP LLM Top 10 and the NIST AI RMF. |

Each is a fixed price, quoted after the written intake. Proof and full scope for each are in [SERVICES.md](SERVICES.md).

**How I work:**

- **Written first.** Every engagement starts with a short written intake instead of a discovery call. You answer on your own time, and I reply with a written scope. Calls are welcome, never required.
- **Fixed scope, fixed price.** Deliverables and an acceptance checklist are agreed in writing before work starts, so we both know what done looks like.
- **Predictable replies.** I answer messages in set windows each weekday, US Eastern time, so you always know when to expect a reply.

**How I use AI.** I build with AI coding agents, run through vibey under the same tests and review gates I would hold a person to. I scope, review and sign off on every deliverable myself, and I will tell you which parts were agent-assisted. For sensitive work I switch off any platform or vendor setting that would let your code or messages train a model.

**Start with the [written intake](freelance/intake.md).** It takes about ten minutes, and I reply with a written scope and a fixed price. Send it by [email](mailto:adam@matthewsteinberger.com).

## Highlights

- **Platforms other teams adopted.** Sole architect of a policy-enforced LLM gateway that three product teams moved onto, and they retired the credentials their apps held. My platform library runs in 17+ repositories.
- **Identity at depth.** Sole author of two identity-governance-as-code control planes (40 resource kinds, multi-tenant, no stored tenant secrets) and advisor to a SOX-regulated enterprise of about 5,700 identities.
- **Handoffs that hold.** Co-led a 20-service AI payroll platform to production-ready architecture by day 45; the junior developer I trained alongside it now owns it.
- **Open source, in public.** Creator of vibey, whose chaos test crashes a fifth of its workers mid-job and passes only if no job is lost or run twice.

## Experience

### The Vibey Project (open source)
**Creator and maintainer** · Aug 2026 – Present · Greenville, SC

- **vibey** _(MIT; on PyPI as vibey-engine)_. A conductor that carries a change from a spec interview through design, build and review, handing work between Claude Code, OpenAI Codex, Cursor Agent, Google Antigravity and local open-weight models, and asking a person only for the decisions that are theirs to make. AI coding agents build it, and they answer to its own CI gates.
- **Nothing is lost when an agent dies.** Every decision, finding and handoff is a row in an append-only PostgreSQL ledger. Workers claim jobs under SKIP LOCKED leases, and a handoff to another vendor must pass a model-free no-loss check or it retries, escalates or waits for a person. A chaos test runs 500 jobs on 8 workers, crashes a fifth of them mid-job, and passes only if **no job is lost or run twice**.
- **Held to its own gates.** 100% branch-coverage floors in CI, 86 architecture decision records, and a Helm chart (KEDA, kopf operator) installed on minikube in CI. In its first two months: 596 merged pull requests and 25 releases. The design is a paper; the documentation is a book.

### The Vizius Group
**Senior Azure and AI Development Engineer** · Sep 2025 – Aug 2026 · Greenville, SC

- **AI governance gateway** _(sole architect, ~54k lines)_. One OpenAI-compatible API in front of Azure AI, Anthropic, OpenAI, Cursor, Grok and Gemini, with per-project allowlists and fallback policy, Redis rate limits, per-call cost attribution with hard spend caps, and an HMAC-signed, hash-chained, write-once audit trail. Callers authenticate with Entra ID over workload identity, so no API keys sit in the path; agent sandboxing, egress policy and SSRF checks map to the OWASP LLM Top 10 and NIST AI RMF. **Three product teams moved onto it** and retired their app-held credentials.
- **Identity governance as code** _(sole author, two control planes)_. A Kubernetes operator (kopf) that reconciles directory governance against Git-declared custom resources, with fully secretless multi-tenant auth and an LLM that drafts pull requests for judgment calls. A second platform manages 40 identity-provider resource kinds with drift classification: safe drift is fixed automatically, destructive changes wait for a pull request and a human approval, and any point in time can be restored. A versioned, idempotent sync API for 114+ directory groups **replaced a low-code workflow**.
- **AI payroll automation platform** _(co-lead, ~420k lines)_. Twenty microservices across four human-approved phases, with the final submission modeled as irreversible; RAG over the document store, AI-directed spreadsheet corrections and earnings review. I owned the Terraform, 20 Helm charts, GitOps and 10 CI/CD workflows, backed by 585 test modules. The architecture was **production-ready at day 45**, and the junior developer I trained in parallel now owns it.
- **Technical report platform** _(lead, ~54k lines)_. Turns electrical-testing instrument data into standards-aware client reports: mail-webhook ingestion with per-document fan-out, a multi-vendor parser seam, a deterministic deficiency analyzer with LLM review, and blocking data-quality gates. Added SAML 2.0 and Entra dual-issuer SSO, replaced a shared API key with per-user bearer auth, and wrote the SOC 2 readiness assessment, STRIDE threat model and ADRs. **Ended silent false-success deploys.**
- **Secretless DevSecOps.** OIDC workload identity federation for 20 CI workflows across 9 repositories; supply-chain pipelines with SAST, SCA, IaC and secret scanning, SBOMs, keyless signing and policy-as-code admission. My own security reviews **caught an auth bypass, path traversal, SSRF, a timing-unsafe comparison, query injection and an over-scoped CI credential before release**. Led a cross-tenant production migration onto OIDC and least-privilege RBAC.
- **Shared platform library.** The firm's Python library for logging, alerting, dead-letter consumers and the outbox pattern, through three major versions; **adopted by 17+ repositories** and four platforms. It lives on in the open as vibey-bootstrap, part of vibey.
- **Also.** A multi-system ticket relay (N-way sync, 653 tests, 93% coverage, mypy --strict); a multi-tenant observability portal; five architecture document sets, about 180 pages; the *Security-First Scrum* framework and training manuals; mentoring junior developers on three projects.

### The Apologist Project
**Volunteer Software Architect** · Apr 2026 – Present · Remote

- **Project Excite.** An adapter-based relay service that hands people from an AI chat to live volunteers on Chatwoot or EchoGlobal: an explicit session state machine with idempotent teardown, Redis-backed sessions, HMAC-verified webhooks and QStash-queued delivery. Shipped as split PR stacks with security hardening (DOMPurify, CORS allowlist, Sentry PII off, rate limiting).

### Adam Matthew Steinberger LLC
**Senior Software Engineering Consultant** · Mar 2025 – Aug 2025 · Greenville, SC

- **Two RAG chatbots, 30 days each.** One fully self-hosted for a non-profit (Mistral-7B, FAISS and vLLM, with Grafana and Prometheus on every token and no external dependencies); one cloud-based for a sales agency (Gemini RAG with API-driven web search).
- **Codebase review.** 59,000 lines across 190+ files reviewed in 10 hours; found 5% test coverage and missing auth middleware, and delivered a technical brief, executive summary and phased roadmap.

### Lima One Capital
**Senior Software Engineer** · May 2023 – Feb 2025 · Greenville, SC

- **Rearchitected the core integration layer** from legacy MuleSoft APIs into NestJS microservices (gRPC and REST) on PostgreSQL, with ETL pipelines and connectors across HubSpot, SharePoint, Snowflake and Salesforce.
- **Built Snow Portal**, a Snowflake job scheduler that replaced Alteryx at a fraction of the cost; full-stack .NET and React work on a mortgage-broker platform (credit-report integrations, pricing-engine APIs).

### Earlier experience

- **Transcat**, Senior Software Engineer (Apr 2022 – Jan 2023). Led the team delivering .NET Web APIs and a React front end for lab-equipment calibration.
- **LeaseTrack**, Senior Software Engineer (Jun 2021 – Apr 2022). Python and AWS Textract document parsing; a Java Spring Boot annotation system feeding an ML training pipeline.
- **Akmazio Software**, Founding Engineer (May 2020 – May 2021). Built the full C#/.NET and SQL Server backend and wrote the business plan; managed interns and a contractor.
- **Bestpass by Fleetworthy**, Software Engineer (Sep 2019 – Apr 2020). Introduced automated unit testing to a legacy toll-billing system that had none.
- **New York State Insurance Fund**, Software Engineer (Mar 2015 – Aug 2019). Migrated VB6 systems to C# MVC, refactored Oracle EDI integrations and mentored junior engineers.
- **Town and Country Computer Services**, Junior Software Engineer (Jul 2013 – Mar 2015). Insurance quoting, rating and reporting apps used all day by underwriters; client-facing from the first day.
- **GE HealthCare**, Junior Software Engineer (Aug 2012 – Feb 2013). A browser-based CT/MRI viewer with real-time 3D scrolling; built its full internationalization feature.

## Skills

- **AI & LLM systems:** Multi-vendor LLM gateways with cost and policy governance, agent sandboxing and egress policy, multi-agent orchestration, MCP servers, RAG (pgvector, FAISS, Azure AI Search, Pinecone), human-in-the-loop gating, structured outputs; Claude, Azure OpenAI/Foundry, GPT, Gemini, Mistral, vLLM, Ollama
- **Identity & access:** Microsoft Entra ID, Okta (core, IGA, Workflows), SAML 2.0, OIDC/OAuth 2.0, workload identity federation, RBAC (control and data plane), governance-as-code reconciliation, SOX-aligned access governance, GxP-classified functional specifications
- **Security & compliance:** Secretless delivery (OIDC federated credentials, managed identity, CSI-driver vault secrets); Trivy, Semgrep, CodeQL, Bandit, Gitleaks, Checkov, SBOM (Syft/CycloneDX), Cosign keyless signing, Kyverno/OPA admission; STRIDE threat modeling, SOC 2 readiness, OWASP LLM Top 10, NIST AI RMF
- **Platform & cloud:** Private AKS (workload identity, KEDA), Terraform, Bicep, Helm, Kustomize, Flux/Argo CD GitOps, GitHub Actions, Service Bus, Event Hubs, Key Vault, Private Endpoints, App Gateway + WAF, OpenTelemetry, PostgreSQL, Redis, Cosmos DB, AWS
- **Languages:** Python 3.12 (FastAPI, SQLAlchemy 2, Pydantic, kopf), TypeScript/NestJS, Next.js + React, C#/.NET, Java Spring Boot, SQL, KQL, Bash, gRPC/REST, OpenAPI

## Publications

- **[Ledger-Mediated Orchestration: Vendor-Independent Autonomous Software Delivery over a Pool of Coding Agents](https://the-vibey-project.github.io/vibey/main/paper.pdf)**. Paper describing vibey's design (not peer reviewed).
- **[Novice to Navigator: Your Guide to AI Chatbots for Business](https://vibewithadam.matthewsteinberger.com/novice-to-navigator)**. Plain-English guide to RAG chatbots for decision-makers; first edition free online (ISBN 979-8274310628).

## Education & certification

- **Skidmore College**, B.A., Computer Science (2010–2012)
- **Rensselaer Polytechnic Institute**, Electrical and Electronics Engineering coursework (2008–2010)
- **Certified ScrumMaster (CSM)**, Scrum Alliance (2021) · [certificate](scrum-certificate.pdf)

## Formats

| Audience | PDF | Word | Text |
|---|---|---|---|
| Open source | [PDF](adam-steinberger-resume.pdf) | [DOCX](adam-steinberger-resume.docx) | [TXT](adam-steinberger-resume.txt) |
| Non-profit | [PDF](adam-steinberger-resume-nonprofit.pdf) | [DOCX](adam-steinberger-resume-nonprofit.docx) | [TXT](adam-steinberger-resume-nonprofit.txt) |
| University & academia | [PDF](adam-steinberger-resume-academia.pdf) | [DOCX](adam-steinberger-resume-academia.docx) | [TXT](adam-steinberger-resume-academia.txt) |
| Government & military | [PDF](adam-steinberger-resume-government-military.pdf) | [DOCX](adam-steinberger-resume-government-military.docx) | [TXT](adam-steinberger-resume-government-military.txt) |
| Freelance & contract | [PDF](adam-steinberger-resume-freelance.pdf) | [DOCX](adam-steinberger-resume-freelance.docx) | [TXT](adam-steinberger-resume-freelance.txt) |
| Industry | [PDF](adam-steinberger-resume-industry.pdf) | [DOCX](adam-steinberger-resume-industry.docx) | [TXT](adam-steinberger-resume-industry.txt) |

Machine-readable: [resume.json](resume.json) (JSON Resume) · [llms.txt](llms.txt) · [profile.jsonld](profile.jsonld) (schema.org) · [CITATION.cff](CITATION.cff) · [Scrum certificate](scrum-certificate.pdf) · Everything else: [vibewithadam.matthewsteinberger.com/join-me](https://vibewithadam.matthewsteinberger.com/join-me)

---

Code [MIT](LICENSE) · résumé content [CC BY 4.0](LICENSE-CONTENT.md) · built by `tools/build_resume.py`. Found a broken link or a stale number? [Open an issue](https://github.com/adammatthewsteinberger/resume/issues); see [CONTRIBUTING.md](CONTRIBUTING.md).
