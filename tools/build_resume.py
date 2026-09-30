#!/usr/bin/env python3
"""Single-source résumé builder.

One set of facts, several framings. Every output is derived from the data in this file,
so no format can drift from another:

    README.md                                 GitHub landing page (default framing)
    adam-steinberger-resume{-variant}.txt     plain text, for ATS paste boxes
    adam-steinberger-resume{-variant}.docx    Word, with document properties set
    adam-steinberger-resume{-variant}.pdf     via headless Chrome, with PDF metadata set
    resume.json                               JSON Resume (https://jsonresume.org/schema)
    llms.txt                                  plain summary for LLM crawlers (https://llmstxt.org)
    CITATION.cff                              "Cite this repository" metadata
    profile.jsonld                            schema.org Person, with the engagements as offers
    SERVICES.md                               fixed-scope engagements: scope, proof and price
    freelance/upwork.md, freelance/fiverr-pro.md   platform copy, checked against field limits

Variants change the title, summary, highlights, skill order and which bullets appear.
They never change a fact. Bullets are written once, in EXPERIENCE, and referenced by key.

Sources of truth: LinkedIn profile export (2026-08-18), vibewithadam.matthewsteinberger.com,
GitHub, PyPI, and the-vibey-project/vibey at 4714d09 (vibey figures measured 2026-09-30:
75 ADRs, 19 releases, 452 merged PRs, 140-plugin skills marketplace, chaos test at
tests/infrastructure/db/test_chaos.py, 100% branch-coverage floors in ci.yml). No invented
metrics. When a figure changes, change it here and rebuild.

Usage:
    python tools/build_resume.py [OUT_DIR] [--no-pdf]

PDF output needs Google Chrome (or set CHROME=/path/to/chrome) and pypdf for metadata.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
OUT = ARGS[0] if ARGS else "."
MAKE_PDF = "--no-pdf" not in sys.argv

REPO = "https://github.com/adammatthewsteinberger/resume"
RAW = "https://raw.githubusercontent.com/adammatthewsteinberger/resume/HEAD"
SITE = "https://vibewithadam.matthewsteinberger.com"
VIBEY = "https://github.com/the-vibey-project/vibey"
VIBEY_DOCS = "https://the-vibey-project.github.io/vibey/main/"
VIBEY_PYPI = "https://pypi.org/project/vibey-engine/"
PAPER_URL = "https://the-vibey-project.github.io/vibey/main/paper.pdf"
JOIN_ME = SITE + "/join-me"

# ---------------------------------------------------------------- identity
NAME = "Adam Matthew Steinberger"
EMAIL = "adam@matthewsteinberger.com"
PHONE = "+1-864-517-4117"
CITY, REGION, COUNTRY = "Greenville", "SC", "US"
PROFILES = [
    ("LinkedIn", "adammatthewsteinberger", "https://www.linkedin.com/in/adammatthewsteinberger/"),
    ("GitHub", "adammatthewsteinberger", "https://github.com/adammatthewsteinberger"),
]
CONTACT = [
    (f"{CITY}, {REGION} (US remote)", None),
    (PHONE, "tel:+18645174117"),
    (EMAIL, f"mailto:{EMAIL}"),
    ("linkedin.com/in/adammatthewsteinberger", PROFILES[0][2]),
    ("github.com/adammatthewsteinberger", PROFILES[1][2]),
    ("vibewithadam.matthewsteinberger.com", SITE),
]

# ---------------------------------------------------------------- experience (the canon)
# Inline markup: **bold** for the scannable handle and the outcome worth catching,
# *italic* for titles, _muted_ for qualifiers such as (sole architect, ~54k lines).
# Dates are YYYY-MM or YYYY; end=None means Present.
EXPERIENCE = [
    {
        "key": "vibey", "org": "The Vibey Project (open source)", "loc": "Greenville, SC",
        "role": "Creator and maintainer", "start": "2026-08", "end": None,
        "url": VIBEY, "kind": "project",
        "bullets": {
            "what": "**vibey** _(MIT; on PyPI as vibey-engine)_. A conductor that carries a change from a spec "
                    "interview through design, build and review, handing work between Claude Code, OpenAI Codex, "
                    "Cursor Agent, Google Antigravity and local open-weight models, and asking a person only for "
                    "the decisions that are theirs to make. Built with AI coding agents working inside its own CI gates.",
            "ledger": "**Nothing is lost when an agent dies.** Every decision, finding and handoff is a row in an "
                      "append-only PostgreSQL ledger. Workers claim jobs under SKIP LOCKED leases, and a handoff to "
                      "another vendor must pass a model-free no-loss check or it retries, escalates or waits for a "
                      "person. A chaos test runs 500 jobs on 8 workers, crashes a fifth of them mid-job, and passes "
                      "only if **no job is lost or run twice**.",
            "gates": "**Held to its own gates.** 100% branch-coverage floors in CI, 75 architecture decision records, "
                     "a Helm chart (KEDA, kopf operator) installed on minikube in CI, and 19 releases from 450+ merged "
                     "pull requests since August 2026. The design is written up as a paper and the documentation as a book.",
        },
    },
    {
        "key": "vizius", "org": "The Vizius Group", "loc": "Greenville, SC",
        "role": "Senior Azure and AI Development Engineer", "start": "2025-09", "end": "2026-08",
        "summary": "Cybersecurity consulting firm. Designed and shipped production platforms on private AKS for "
                   "manufacturing, health-tech, financial-services and SOX-regulated clients.",
        "bullets": {
            "gateway": "**AI governance gateway** _(sole architect, ~54k lines)_. One OpenAI-compatible API in front of "
                       "Azure AI, Anthropic, OpenAI, Cursor, Grok and Gemini, with per-project allowlists and fallback "
                       "policy, Redis rate limits, per-call cost attribution with hard spend caps, and an HMAC-signed, "
                       "hash-chained, write-once audit trail. Callers authenticate with Entra ID over workload identity, "
                       "so no API keys sit in the path; agent sandboxing, egress policy and SSRF checks map to the OWASP "
                       "LLM Top 10 and NIST AI RMF. **Three product teams moved onto it** and retired their app-held credentials.",
            "identity": "**Identity governance as code** _(sole author, two control planes)_. A Kubernetes operator (kopf) "
                        "that reconciles directory governance against Git-declared custom resources, with fully secretless "
                        "multi-tenant auth and an LLM that drafts pull requests for judgment calls. A second platform "
                        "manages 40 identity-provider resource kinds with drift classification: safe drift is fixed "
                        "automatically, destructive changes wait for a pull request and a human approval, and any point in "
                        "time can be restored. A versioned, idempotent sync API for 114+ directory groups **replaced a "
                        "low-code workflow**.",
            "payroll": "**AI payroll automation platform** _(co-lead, ~420k lines)_. Twenty microservices across four "
                       "human-approved phases, with the final submission modeled as irreversible; RAG over the document "
                       "store, AI-directed spreadsheet corrections and earnings review. I owned the Terraform, 20 Helm "
                       "charts, GitOps and 10 CI/CD workflows, backed by 585 test modules. The architecture was "
                       "**production-ready at day 45**, and the junior developer I trained in parallel now owns it.",
            "reports": "**Technical report platform** _(lead, ~54k lines)_. Turns electrical-testing instrument data into "
                       "standards-aware client reports: mail-webhook ingestion with per-document fan-out, a multi-vendor "
                       "parser seam, a deterministic deficiency analyzer with LLM review, and blocking data-quality gates. "
                       "Added SAML 2.0 and Entra dual-issuer SSO, replaced a shared API key with per-user bearer auth, and "
                       "wrote the SOC 2 readiness assessment, STRIDE threat model and ADRs. **Ended silent false-success deploys.**",
            "devsecops": "**Secretless DevSecOps.** OIDC workload identity federation for 20 CI workflows across 9 "
                         "repositories; supply-chain pipelines with SAST, SCA, IaC and secret scanning, SBOMs, keyless "
                         "signing and policy-as-code admission. My own security reviews **caught an auth bypass, path "
                         "traversal, SSRF, a timing-unsafe comparison, query injection and an over-scoped CI credential "
                         "before release**. Led a cross-tenant production migration onto OIDC and least-privilege RBAC.",
            "advisory": "**Regulated advisory.** Identity-governance advisory for a SOX-regulated enterprise of about "
                        "5,700 identities: a platform decision report, API/SDK/MCP coverage across eight platforms, "
                        "GxP-classified functional specifications and SOX-to-IAM risk mapping. Also a white paper on "
                        "export-control compliance and cloud enclave architecture, written from recorded expert "
                        "interviews, and an AI vendor-terms comparison for legal and procurement.",
            "library": "**Shared platform library.** The firm's Python library for logging, alerting, dead-letter "
                       "consumers and the outbox pattern, through three major versions; **adopted by 17+ repositories** "
                       "and four platforms. It now continues in the open as vibey-bootstrap, part of vibey.",
            "relay": "**Multi-system ticket relay** _(sole author, ~20k lines)_. N-way sync with no privileged hub: "
                     "version vectors, echo suppression, a conflict-policy engine, and edge HMAC verification with "
                     "per-tenant secrets in a vault. 653 tests at 93% coverage, mypy --strict clean, with property, "
                     "mutation and chaos tests showing convergence.",
            "also": "**Also.** A multi-system ticket relay (N-way sync, 653 tests, 93% coverage, mypy --strict); a "
                    "multi-tenant observability portal; five architecture document sets, about 180 pages; the "
                    "*Security-First Scrum* framework and training manuals; mentoring junior developers on three projects.",
        },
    },
    {
        "key": "apologist", "org": "The Apologist Project", "loc": "Remote",
        "role": "Volunteer Software Architect", "start": "2026-04", "end": None, "kind": "volunteer",
        "bullets": {
            "excite": "**Project Excite.** An adapter-based relay service that hands people from an AI chat to live "
                      "volunteers on Chatwoot or EchoGlobal: an explicit session state machine with idempotent "
                      "teardown, Redis-backed sessions, HMAC-verified webhooks and QStash-queued delivery. Shipped as "
                      "split PR stacks with security hardening (DOMPurify, CORS allowlist, Sentry PII off, rate limiting).",
        },
    },
    {
        "key": "llc", "org": "Adam Matthew Steinberger LLC", "loc": "Greenville, SC",
        "role": "Senior Software Engineering Consultant", "start": "2025-03", "end": "2026",
        "bullets": {
            "chatbots": "**Two RAG chatbots, 30 days each.** One fully self-hosted for a non-profit (Mistral-7B, FAISS "
                        "and vLLM, with Grafana and Prometheus on every token and no external dependencies); one "
                        "cloud-based for a sales agency (Gemini RAG with API-driven web search).",
            "review": "**Codebase review.** 59,000 lines across 190+ files reviewed in 10 hours; found 5% test coverage "
                      "and missing auth middleware, and delivered a technical brief, executive summary and phased roadmap.",
            "push": "**Web push notifications** for a non-profit: timezone-aware scheduling and personalization; "
                    "159 of 159 tests passing at 86% coverage, delivered in 5 billable hours against a 30-hour estimate.",
        },
    },
    {
        "key": "limaone", "org": "Lima One Capital", "loc": "Greenville, SC",
        "role": "Senior Software Engineer", "start": "2023-05", "end": "2025-02",
        "bullets": {
            "integration": "**Rearchitected the core integration layer** from legacy MuleSoft APIs into NestJS "
                           "microservices (gRPC and REST) on PostgreSQL, with ETL pipelines and connectors across "
                           "HubSpot, SharePoint, Snowflake and Salesforce.",
            "snow": "**Built Snow Portal**, a Snowflake job scheduler that replaced Alteryx at a fraction of the cost; "
                    "full-stack .NET and React work on a mortgage-broker platform (credit-report integrations, "
                    "pricing-engine APIs).",
        },
    },
]

EARLIER = [
    # org, role, location, start, end, one line
    ("Transcat", "Senior Software Engineer", "Rochester, NY", "2022-04", "2023-01",
     "Led the team delivering .NET Web APIs and a React front end for lab-equipment calibration."),
    ("LeaseTrack", "Senior Software Engineer", "Latham, NY", "2021-06", "2022-04",
     "Python and AWS Textract document parsing; a Java Spring Boot annotation system feeding an ML training pipeline."),
    ("Akmazio Software", "Founding Engineer", "Albany, NY", "2020-05", "2021-05",
     "Built the full C#/.NET and SQL Server backend and wrote the business plan; managed interns and a contractor."),
    ("Bestpass by Fleetworthy", "Software Engineer", "Albany, NY", "2019-09", "2020-04",
     "Introduced automated unit testing to a legacy toll-billing system that had none."),
    ("New York State Insurance Fund", "Software Engineer", "Albany, NY", "2015-03", "2019-08",
     "Migrated VB6 systems to C# MVC, refactored Oracle EDI integrations and mentored junior engineers."),
    ("Town and Country Computer Services", "Junior Software Engineer", "Schenectady, NY", "2013-07", "2015-03",
     "Insurance quoting, rating and reporting apps used all day by underwriters; client-facing from the first day."),
    ("GE HealthCare", "Junior Software Engineer", "Barrington, IL", "2012-08", "2013-02",
     "A browser-based CT/MRI viewer with real-time 3D scrolling; built its full internationalization feature."),
]

OPEN_SOURCE = [
    ("vibey", VIBEY,
     "Conductor for AI coding agents, five engine runners, the vibey-gh release tool and vibey-bootstrap. "
     "MIT; pip install vibey-engine. Contributors welcome."),
    ("vibey-skills", VIBEY,
     "A 140-plugin Claude Code skills marketplace, shipped inside vibey."),
]

PUBLICATIONS = [
    ("Ledger-Mediated Orchestration: Vendor-Independent Autonomous Software Delivery over a Pool of Coding Agents",
     "Paper describing vibey's design (not peer reviewed).", PAPER_URL, "2026"),
    ("Novice to Navigator: Your Guide to AI Chatbots for Business",
     "Plain-English guide to RAG chatbots for decision-makers; first edition free online (ISBN 979-8274310628).",
     SITE + "/novice-to-navigator", "2025"),
]

EDUCATION = [
    ("Skidmore College", "B.A., Computer Science", "2010", "2012"),
    ("Rensselaer Polytechnic Institute", "Electrical and Electronics Engineering coursework", "2008", "2010"),
]
CERTS = [("Certified ScrumMaster (CSM)", "Scrum Alliance", "2021")]

# ---------------------------------------------------------------- skills
SKILL_SETS = {
    "ai": ("AI & LLM systems",
           "Multi-vendor LLM gateways with cost and policy governance, agent sandboxing and egress policy, multi-agent "
           "orchestration, MCP servers, RAG (pgvector, FAISS, Azure AI Search, Pinecone), human-in-the-loop gating, "
           "structured outputs; Claude, Azure OpenAI/Foundry, GPT, Gemini, Mistral, vLLM, Ollama"),
    "identity": ("Identity & access",
                 "Microsoft Entra ID, Okta (core, IGA, Workflows), SAML 2.0, OIDC/OAuth 2.0, workload identity "
                 "federation, RBAC (control and data plane), governance-as-code reconciliation, SOX-aligned access "
                 "governance, GxP-classified functional specifications"),
    "security": ("Security & compliance",
                 "Secretless delivery (OIDC federated credentials, managed identity, CSI-driver vault secrets); Trivy, "
                 "Semgrep, CodeQL, Bandit, Gitleaks, Checkov, SBOM (Syft/CycloneDX), Cosign keyless signing, "
                 "Kyverno/OPA admission; STRIDE threat modeling, SOC 2 readiness, OWASP LLM Top 10, NIST AI RMF"),
    "platform": ("Platform & cloud",
                 "Private AKS (workload identity, KEDA), Terraform, Bicep, Helm, Kustomize, Flux/Argo CD GitOps, GitHub "
                 "Actions, Service Bus, Event Hubs, Key Vault, Private Endpoints, App Gateway + WAF, OpenTelemetry, "
                 "PostgreSQL, Redis, Cosmos DB, AWS"),
    "languages": ("Languages",
                  "Python 3.12 (FastAPI, SQLAlchemy 2, Pydantic, kopf), TypeScript/NestJS, Next.js + React, C#/.NET, "
                  "Java Spring Boot, SQL, KQL, Bash, gRPC/REST, OpenAPI"),
    "quality": ("Quality",
                "pytest, Hypothesis, mutation and chaos testing, contract and end-to-end tests, mypy --strict, ruff, "
                "import-linter-enforced onion architecture"),
    "data": ("Data & integration",
             "PostgreSQL, Snowflake, SQL Server, Oracle, MongoDB, Redis; ETL and API integrations (HubSpot, SharePoint, "
             "Salesforce, Microsoft Graph); event-driven pipelines (Service Bus, Event Hubs); data-quality gates"),
    "platform_fd": ("Platform & security",
                    "Kubernetes (AKS, KEDA), Terraform, Helm, GitOps, GitHub Actions; Entra ID, Okta, SAML/OIDC, workload "
                    "identity; STRIDE threat modeling, SOC 2 readiness, OWASP LLM Top 10"),
    "delivery": ("Delivery",
                 "Discovery, a written solution, decomposition into work, then a mentored handoff; executive summaries "
                 "for stakeholders; Scrum (CSM); author of Security-First Scrum"),
}

# ---------------------------------------------------------------- fixed-scope engagements (freelance)
# Five outcomes already delivered, each sold as a fixed scope. The client is the subject of
# every "problem" line; the proof is the evidence, and it may only restate numbers that already
# appear in the EXPERIENCE bullets named in "sources" (check_services() enforces this).
UPWORK_URL = None   # set to the public profile URL once it is live; rendered only when set
FIVERR_URL = None   # likewise, for the Fiverr Pro seller page
INTAKE = "freelance/intake.md"

# ---------------------------------------------------------------- pricing (yours to set)
# TODO(Adam): one entry per offer below. Each value is either None, which renders as
# "Fixed price, quoted after the written intake", or a (price, turnaround) pair such as
# ("from $2,500", "5 business days"). Price by the value of the outcome, not by an hourly
# benchmark (the playbook found hourly benchmarks disagree by up to 2x). Public prices here
# also appear on GitHub, in llms.txt and in the JSON-LD, so decide whether you want them
# public or platform-only before filling them in.
PRICING = {
    "review": None,
    "rag": None,
    "gateway": None,
    "identity": None,
    "readiness": None,
}

SERVICES = [
    {
        "key": "review",
        "portfolio": "Codebase review: 59,000 lines in 10 hours, with a phased roadmap",
        "name": "AI codebase and security review",
        "gig": "I will review your AI codebase for security gaps and give you a phased fix plan",
        "problem": "Your AI feature or fast-grown codebase is about to meet customers or an auditor, and you need to "
                   "know what will break or leak before they find it.",
        "pitch": "A severity-ranked findings report, a one-page executive summary and a phased roadmap.",
        "includes": [
            "Findings ranked by severity, each with the file, the risk and the fix",
            "A one-page executive summary for the people who won't read the report",
            "A phased roadmap: fix this week, fix this quarter, and what can wait",
            "A written walkthrough of the results, with a call if you want one",
        ],
        "proof": "Reviewed a 59,000-line codebase in 10 hours and found missing auth middleware and 5% test "
                 "coverage. My pre-release reviews have caught an auth bypass, path traversal and SSRF.",
        "sources": [("llc", "review"), ("vizius", "devsecops")],
    },
    {
        "key": "rag",
        "portfolio": "Self-hosted RAG chatbot in 30 days (Mistral-7B, FAISS, vLLM)",
        "name": "Production RAG chatbot in 30 days",
        "gig": "I will build a production RAG chatbot on your own documents in 30 days",
        "problem": "You want staff or customers to get answers from your own documents, running in weeks rather "
                   "than quarters, without your data leaving your control.",
        "pitch": "A chatbot that answers from your documents and cites them, with evaluation, monitoring and a handoff.",
        "includes": [
            "A chatbot that answers from your documents and shows the source for each answer",
            "An evaluation set of real questions, so quality is measured rather than guessed",
            "Monitoring on every request, plus a runbook for whoever owns it next",
            "Two tiers: cloud models, or fully self-hosted so no data leaves your servers",
        ],
        "proof": "Delivered two RAG chatbots in 30 days each: one fully self-hosted for a non-profit (Mistral-7B, "
                 "FAISS and vLLM, no external dependencies) and one cloud-based for a sales agency.",
        "sources": [("llc", "chatbots")],
    },
    {
        "key": "gateway",
        "portfolio": "LLM cost and policy gateway adopted by three product teams",
        "name": "LLM cost and policy gateway",
        "gig": "I will build an LLM gateway with spend caps and an audit trail for your teams",
        "problem": "Your teams call several AI vendors with keys scattered through their apps, and nobody can say "
                   "what it costs or who sent what.",
        "pitch": "One API in front of your AI vendors, with spend caps, allowlists and a tamper-evident audit trail.",
        "includes": [
            "One OpenAI-compatible API in front of the vendors you already use",
            "Per-project model allowlists, rate limits and hard spend caps",
            "A tamper-evident audit trail of every call and what it cost",
            "Sign-in through your identity provider, so apps hold no vendor keys",
        ],
        "proof": "Sole architect of a ~54k-line gateway in front of six vendors; three product teams moved onto it "
                 "and retired the credentials their apps held.",
        "sources": [("vizius", "gateway")],
    },
    {
        "key": "identity",
        "portfolio": "Identity governance as code: 40 resource kinds, no stored secrets",
        "name": "Okta and Entra ID governance fixes",
        "gig": "I will fix your Okta or Entra ID access governance and manage it from Git",
        "problem": "Access grew by hand. Now there are stale groups, admins nobody remembers granting, and an "
                   "access review each audit season that nobody fully trusts.",
        "pitch": "An access review, then groups, roles and policy managed from Git with drift detection.",
        "includes": [
            "An access review that names the risky grants",
            "Groups, roles and policies declared in Git and applied by a pipeline",
            "Drift detection: safe drift fixed automatically, risky changes held for approval",
            "A runbook your team can follow without me",
        ],
        "proof": "Sole author of two identity-governance-as-code control planes covering 40 resource kinds with no "
                 "stored tenant secrets; identity advisory for a SOX-regulated enterprise of about 5,700 identities.",
        "sources": [("vizius", "identity"), ("vizius", "advisory")],
    },
    {
        "key": "readiness",
        "portfolio": "SOC 2 readiness and STRIDE threat model for an AI report platform",
        "name": "SOC 2 and OWASP LLM Top 10 readiness for an AI feature",
        "gig": "I will assess your AI feature against SOC 2 and the OWASP LLM Top 10",
        "problem": "A customer's security questionnaire just asked how your AI feature handles prompt injection "
                   "and data leakage, and you need a straight answer backed by evidence.",
        "pitch": "A threat model and a control-gap list mapped to SOC 2, the OWASP LLM Top 10 and the NIST AI RMF.",
        "includes": [
            "A STRIDE threat model of the feature",
            "A control-gap list mapped to SOC 2, the OWASP LLM Top 10 and the NIST AI RMF",
            "A remediation plan in priority order",
            "Plain-language answers you can reuse in security questionnaires",
        ],
        "note": "This is readiness work, not an audit opinion; only a licensed CPA firm issues a SOC 2 report.",
        "proof": "Wrote the SOC 2 readiness assessment and STRIDE threat model for a report platform, and mapped an "
                 "AI gateway's controls to the OWASP LLM Top 10 and NIST AI RMF.",
        "sources": [("vizius", "reports"), ("vizius", "gateway")],
    },
]

# How engagements run. Each line is a professional practice a client can plan around.
WORKING_STYLE = [
    ("Written first.", "Every engagement starts with a short written intake instead of a discovery call. You answer "
                       "on your own time, and I reply with a written scope. Calls are welcome, never required."),
    ("Fixed scope, fixed price.", "Deliverables and an acceptance checklist are agreed in writing before work "
                                  "starts, so we both know what done looks like."),
    ("Predictable replies.", "I answer messages in set windows each weekday, US Eastern time, so you always know "
                             "when to expect a reply."),
    ("Risks in writing, early.", "If something threatens the date or the scope, you get a short written note with "
                                 "options the day I find it."),
    ("A few clients at a time.", "I take two or three engagements at once, so each one gets focused attention."),
    ("Handoffs that hold.", "Every engagement ends with documentation and a handoff your team can run without me."),
]

AI_USE = ("I build with AI coding agents, run through vibey under the same tests and review gates I would hold a "
          "person to. I scope, review and sign off on every deliverable myself, and I will tell you which parts were "
          "agent-assisted. For sensitive work I switch off any platform or vendor setting that would let your code "
          "or messages train a model.")

# Platform field limits. P = platform's own page; S = consistent secondary sources. Checked 2026-09-30.
LIMITS = {
    "upwork_title": 70,             # P: upwork.com/resources/freelancer-headlines
    "upwork_portfolio_title": 70,   # P: support.upwork.com, "How to enhance your freelancer profile"
    "upwork_overview": 5000,        # S
    "upwork_fold": 250,             # S: roughly what shows before "more" in search and previews
    "upwork_skills": 20,            # S
    "fiverr_title": 80,             # S, consistent across sources; includes the fixed "I will"
    "fiverr_description": 1200,     # S
}


SERVICES_NOTE = "Each is a fixed scope, starting with a written intake and an agreed acceptance checklist."


def price_line(key):
    p = PRICING.get(key)
    if not p:
        return "Fixed price, quoted after the written intake."
    price, turnaround = p
    return f"{price}, fixed. Typical turnaround: {turnaround}."


def check_services():
    """Fail the build if a proof line states a number its source bullets don't contain."""
    by_key = {e["key"]: e for e in EXPERIENCE}
    assert set(PRICING) == {s["key"] for s in SERVICES}, "PRICING keys must match SERVICES keys"
    for s in SERVICES:
        src = " ".join(by_key[k]["bullets"][b] for k, b in s["sources"])
        for n in re.findall(r"\d[\d,]*\d|\d", s["proof"]):
            assert n in src, f"service '{s['key']}': '{n}' in proof is not in its source bullets"
        for n in re.findall(r"\d[\d,]*\d|\d", s["portfolio"]):
            assert n in src, f"service '{s['key']}': '{n}' in portfolio title is not in its source bullets"
        assert len(s["gig"]) <= LIMITS["fiverr_title"], f"gig title too long: {s['gig']} ({len(s['gig'])})"
        assert len(s["portfolio"]) <= LIMITS["upwork_portfolio_title"], f"portfolio title too long: {s['portfolio']}"


# ---------------------------------------------------------------- variants (the framings)
VARIANTS = {
    "default": {
        "stem": "adam-steinberger-resume",
        "label": "General",
        "title": "Staff Software Engineer · AI platforms, identity and agent infrastructure",
        "tagline": "I build AI platforms that other teams can safely build on: no stored secrets, every call on the "
                   "record, and a person signing off on anything that can't be undone.",
        "availability": "Available now for Staff+ engineering roles and for fixed-scope contract work. Based in "
                        "Greenville, SC; working US-remote.",
        "summary": "I've spent 13 years building production software for insurance, lending, healthcare and security "
                   "teams, and most recently the controls that let AI run safely inside them. My work is "
                   "identity-first: workload identity instead of stored keys, audit trails that can't be quietly "
                   "edited, and policy kept in Git where it can be reviewed. I write the architecture down before the "
                   "code, train the people who will own it, and hand over systems that keep running after I leave. "
                   "In my own time I maintain vibey, an open-source conductor for AI coding agents.",
        "highlights": [
            "**Platforms other teams adopted.** Sole architect of a policy-enforced LLM gateway that three product "
            "teams moved onto, retiring the credentials their apps held; my platform library is used by 17+ repositories.",
            "**Identity at depth.** Sole author of two identity-governance-as-code control planes (40 resource kinds, "
            "multi-tenant, no stored tenant secrets) and advisor to a SOX-regulated enterprise of about 5,700 identities.",
            "**Handoffs that hold.** Co-led a 20-service AI payroll platform to production-ready architecture by day 45; "
            "the junior developer I trained alongside it now owns it.",
            "**Open source, in public.** Creator of vibey, whose chaos test crashes a fifth of its workers mid-job and "
            "passes only if no job is lost or run twice.",
        ],
        "skills": ["ai", "identity", "security", "platform", "languages"],
        "bullets": {
            "vibey": ["what", "ledger", "gates"],
            "vizius": ["gateway", "identity", "payroll", "reports", "devsecops", "library", "also"],
            "llc": ["chatbots", "review"],
        },
        "keywords": ["Staff Software Engineer", "AI platform engineering", "agent orchestration", "LLM gateway",
                     "AI governance", "identity and access management", "workload identity", "secretless CI/CD",
                     "Kubernetes", "Python", "open source", "vibey", "RAG chatbot", "AI security review",
                     "freelance AI engineer"],
    },
    "freelance": {
        "stem": "adam-steinberger-resume-freelance",
        "label": "Freelance & contract",
        "title": "Independent AI Platform Engineer · fixed-scope AI, identity and security work",
        "tagline": "Senior engineering sold as a fixed scope: RAG chatbots, LLM gateways, identity governance and AI "
                   "security reviews, agreed in writing and handed over clean.",
        "availability": "Taking fixed-scope and contract engagements now. Based in Greenville, SC; working US-remote.",
        "summary": "I've spent 13 years building production software for insurance, lending, healthcare and security "
                   "teams, and I now offer that work as fixed-scope engagements. I've delivered two RAG chatbots in "
                   "30 days each, reviewed a 59,000-line codebase in 10 hours, and architected an AI gateway that "
                   "three product teams adopted. Each engagement starts with a written intake and an acceptance "
                   "checklist, and ends with documentation your team can run without me.",
        "highlights": [
            "**Fast from zero.** Two RAG chatbots delivered in 30 days each, one fully self-hosted so no data left "
            "the client's servers; a 59,000-line codebase reviewed in 10 hours with a phased roadmap.",
            "**Adoption, not demos.** Three product teams moved onto the AI gateway I architected; my platform "
            "library is used by 17+ repositories.",
            "**Security that holds up.** SOC 2 readiness, STRIDE threat models and OWASP LLM Top 10 mapping; "
            "pre-release reviews that caught an auth bypass, path traversal and SSRF.",
        ],
        "services": True,
        "order": ["llc", "vizius", "vibey", "apologist", "limaone"],
        "skills": ["ai", "security", "identity", "languages"],
        "bullets": {
            "llc": ["chatbots", "review", "push"],
            "vizius": ["gateway", "identity", "reports", "devsecops"],
            "vibey": ["what", "ledger"],
        },
        "keywords": ["freelance AI engineer", "AI consultant", "RAG chatbot", "LLM gateway", "AI security review",
                     "SOC 2 readiness", "OWASP LLM Top 10", "Okta", "Microsoft Entra ID", "fixed-price",
                     "Upwork", "Fiverr Pro", "Python"],
    },
    "platform-identity": {
        "stem": "adam-steinberger-resume-platform-identity",
        "label": "Platform & identity focus",
        "title": "Staff Software Engineer · AI platform, identity and regulated deployments",
        "tagline": "Secretless, auditable AI platforms for environments where compliance and security are "
                   "requirements from the first day.",
        "availability": "Available now for Staff+ roles in AI platform, identity and public-sector engineering. "
                        "Based in Greenville, SC; working US-remote.",
        "summary": "I've spent 13 years building production systems in regulated industries: insurance, lending, "
                   "healthcare and cybersecurity. I architect AI platforms whose identity, audit and supply-chain "
                   "controls hold up to review, with workload identity instead of stored secrets, hash-chained audit "
                   "trails, policy-as-code admission and governance reconciled from Git. I write the architecture down "
                   "before the code, train the people who inherit it, and hand off systems that keep running.",
        "highlights": [
            "**Platforms other teams adopted.** Sole architect of a policy-enforced LLM gateway that three product "
            "teams moved onto, retiring their app-held credentials; shared platform library adopted by 17+ repositories.",
            "**Identity at depth.** Sole author of two identity-governance-as-code control planes (40 resource kinds, "
            "multi-tenant, no stored tenant secrets) and identity advisory for a SOX-regulated enterprise of about 5,700 identities.",
            "**Handoffs that hold.** Co-led a 20-service platform to production-ready architecture by day 45; the junior "
            "developer trained in parallel now owns it.",
        ],
        "skills": ["identity", "security", "ai", "platform", "languages"],
        "bullets": {
            "vibey": ["what", "ledger", "gates"],
            "vizius": ["identity", "gateway", "devsecops", "advisory", "payroll", "reports", "library", "also"],
            "llc": ["chatbots", "review"],
        },
        "keywords": ["Staff Software Engineer", "identity and access management", "workload identity federation",
                     "AI platform", "public sector", "regulated environments", "SOC 2", "NIST AI RMF",
                     "supply-chain security", "Kubernetes", "Python"],
    },
    "forward-deployed": {
        "stem": "adam-steinberger-resume-forward-deployed",
        "label": "Forward-deployed focus",
        "title": "Forward Deployed AI Engineer · Enterprise AI, discovery to production",
        "tagline": "I embed with the business, break the messy problem into parts, and ship AI workflows the customer "
                   "can run after I leave.",
        "availability": "Available now for forward-deployed and customer-facing AI engineering roles. Based in "
                        "Greenville, SC; working US-remote.",
        "summary": "For 13 years I've turned unclear business problems into production systems for insurance, lending, "
                   "healthcare and industrial-testing teams, as an employee, a founding engineer and an independent "
                   "consultant. My method is steady: discovery, a written solution, decomposition into work, then a "
                   "handoff to someone I've mentored. Most recently I led AI platforms that put language models into "
                   "real operational work, such as payroll, engineering reports and identity governance, with a person "
                   "approving every step that can't be undone.",
        "highlights": [
            "**Shipped in customer reality.** Co-led a 20-service AI payroll platform to production-ready architecture "
            "by day 45, with human-approved phases and an irreversible final submission; the junior developer I trained "
            "alongside it now owns it.",
            "**Fast from zero.** Two RAG chatbots delivered in 30 days each for different clients; a 59,000-line "
            "codebase reviewed in 10 hours with a phased roadmap.",
            "**Adoption, not demos.** Three product teams moved onto the AI gateway I architected; my platform library "
            "is used by 17+ repositories.",
        ],
        "skills": ["ai", "data", "languages", "platform_fd", "delivery"],
        "bullets": {
            "vibey": ["what", "ledger", "gates"],
            "vizius": ["payroll", "reports", "gateway", "identity", "advisory", "also"],
            "llc": ["chatbots", "review", "push"],
        },
        "keywords": ["Forward Deployed Engineer", "Forward Deployed AI Engineer", "enterprise AI", "RAG",
                     "AI agents", "customer-facing engineering", "discovery to production", "data integration",
                     "Python", "TypeScript"],
    },
}

# Experience order per variant: open source first, because it is current and public.
ORDER = ["vibey", "vizius", "apologist", "llc", "limaone"]

# ---------------------------------------------------------------- helpers
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fmt_date(d):
    if d is None:
        return "Present"
    if len(d) == 4:
        return d
    y, m = d.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def span(start, end):
    return f"{fmt_date(start)} – {fmt_date(end)}"


def jobs(v):
    """(entry, [bullet text]) in display order for variant v."""
    by_key = {e["key"]: e for e in EXPERIENCE}
    out = []
    for k in v.get("order", ORDER):
        e = by_key[k]
        keys = v["bullets"].get(k, list(e["bullets"]))
        out.append((e, [e["bullets"][b] for b in keys]))
    return out


def skills(v):
    return [SKILL_SETS[k] for k in v["skills"]]


def split_list(s):
    """Split a skills string on top-level commas/semicolons (parentheses kept intact)."""
    items, depth, cur = [], 0, ""
    for ch in s:
        depth += ch == "("
        depth -= ch == ")"
        if ch in ",;" and depth == 0:
            items.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    return items


# Inline markup: **bold**, *italic*, _muted_.
_EM = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|(?<![\w/])_(.+?)_(?![\w/])")


def plain(s):
    return _EM.sub(lambda m: next(g for g in m.groups() if g is not None), s)


def spans(s):
    pos = 0
    for m in _EM.finditer(s):
        if m.start() > pos:
            yield s[pos:m.start()], None
        if m.group(1) is not None:
            yield m.group(1), "b"
        elif m.group(2) is not None:
            yield m.group(2), "i"
        else:
            yield m.group(3), "muted"
        pos = m.end()
    if pos < len(s):
        yield s[pos:], None


def h(s):
    return html.escape(s, quote=True)


def rich(s):
    out = []
    for text, style in spans(s):
        t = html.escape(text, quote=False)
        out.append({"b": f"<b>{t}</b>", "i": f"<i>{t}</i>", "muted": f"<span class='muted'>{t}</span>"}.get(style, t))
    return "".join(out)


def files(v):
    s = v["stem"]
    return {"pdf": f"{s}.pdf", "docx": f"{s}.docx", "txt": f"{s}.txt", "html": f"{s}.html"}


# ---------------------------------------------------------------- README (default framing, FOSS first)
def md():
    v = VARIANTS["default"]
    L = [f"# {NAME}", "", f"**{v['title']}**", "", v["tagline"], ""]
    L.append(" · ".join(f"[{t}]({u})" if u else t for t, u in CONTACT))
    L.append("")
    L.append(f"[![vibey on PyPI](https://img.shields.io/pypi/v/vibey-engine?label=vibey)]({VIBEY_PYPI}) "
             f"[![Code: MIT](https://img.shields.io/badge/code-MIT-yellow.svg)](LICENSE) "
             f"[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)")
    L.append("")
    L.append(f"> {v['availability']}")
    L.append("")
    L.append("**[Contribute to vibey](#open-source)** · [Hire me for a fixed-scope project](#fixed-scope-engagements) · "
             "[Hire me full-time](#experience)")
    L.append("")
    L.append(v["summary"])
    L.append("")

    L += [
        "## Open source",
        "",
        f"**[vibey]({VIBEY})** is where most of my current work happens. If you've left an AI coding agent "
        "running overnight, you've met the gap it fills. An agent can finish a task, but it can't interview you "
        "until the spec is sharp, keep going when one vendor's credits run out, or remember what was decided after "
        "a crash. vibey keeps all of that in a PostgreSQL ledger instead of a chat session, and moves work between "
        "engines without losing an open question.",
        "",
        "```bash",
        "uv tool install vibey-engine    # or: pipx install vibey-engine",
        "```",
        "",
        f"Setup, including PostgreSQL, is in the [install guide]({VIBEY}#install). "
        f"The [design paper]({PAPER_URL}) explains why it works the way it does.",
        "",
        "**Good ways in, if you'd like to help:**",
        "",
        "- **Add an engine.** Each coding agent runs behind one engine contract, checked by a conformance suite "
        "(`vibey doctor --conformance`). Another agent CLI is a well-bounded first contribution.",
        "- **Write a skill.** vibey-skills is a 140-plugin Claude Code marketplace, and a plugin is mostly Markdown. "
        "If you know a field well, that knowledge is useful there.",
        "- **Try to break it.** Run it on a real repository and open an issue for whatever surprised you. "
        f"The [contributing guide]({VIBEY}/blob/develop/CONTRIBUTING.md) is command-level, and it treats anything "
        "unclear as a bug in the guide.",
        "",
        f"[Contributing]({VIBEY}/blob/develop/CONTRIBUTING.md) · [Open issues]({VIBEY}/issues) · "
        f"[Docs]({VIBEY_DOCS}) · [Volunteer with me]({JOIN_ME})",
        "",
        "**This repository is a small tool too.** [`tools/build_resume.py`](tools/build_resume.py) is one Python "
        "file that renders this page, the PDF, Word and text résumés, a [JSON Resume](resume.json) file and "
        "[`llms.txt`](llms.txt) from a single set of facts, so no format can drift from another. The code is MIT; "
        "fork it for your own résumé.",
        "",
    ]

    L += services_md_section(level=2) + [""]

    L += ["## Highlights", ""] + [f"- {b}" for b in v["highlights"]] + [""]

    L += ["## Experience", ""]
    for e, bullets in jobs(v):
        L.append(f"### {e['org']}")
        L.append(f"**{e['role']}** · {span(e['start'], e['end'])} · {e['loc']}")
        L.append("")
        L += [f"- {b}" for b in bullets]
        L.append("")
    L += ["### Earlier experience", ""]
    for org, role, loc, s, e, line in EARLIER:
        L.append(f"- **{org}**, {role} ({span(s, e)}). {line}")
    L.append("")

    L += ["## Skills", ""] + [f"- **{k}:** {t}" for k, t in skills(v)] + [""]

    L += ["## Publications", ""]
    for title, desc, url, _ in PUBLICATIONS:
        L.append(f"- **[{title}]({url})**. {desc}")
    L.append("")

    L += ["## Education & certification", ""]
    for school, deg, s, e in EDUCATION:
        L.append(f"- **{school}**, {deg} ({s}–{e})")
    for c, org, yr in CERTS:
        L.append(f"- **{c}**, {org} ({yr}) · [certificate](scrum-certificate.pdf)")
    L.append("")

    L += ["## Formats", "", "| Framing | PDF | Word | Text |", "|---|---|---|---|"]
    for key in VARIANTS:
        f = files(VARIANTS[key])
        L.append(f"| {VARIANTS[key]['label']} | [PDF]({f['pdf']}) | [DOCX]({f['docx']}) | [TXT]({f['txt']}) |")
    L.append("")
    L.append(f"Machine-readable: [resume.json](resume.json) (JSON Resume) · [llms.txt](llms.txt) · "
             f"[profile.jsonld](profile.jsonld) (schema.org) · [CITATION.cff](CITATION.cff) · "
             f"[Scrum certificate](scrum-certificate.pdf) · "
             f"Everything else: [{JOIN_ME.split('//')[1]}]({JOIN_ME})")
    L.append("")
    L.append("---")
    L.append("")
    L.append("Code [MIT](LICENSE) · résumé content [CC BY 4.0](LICENSE-CONTENT.md) · "
             "built by `tools/build_resume.py`. Found a broken link or a stale number? "
             f"[Open an issue]({REPO}/issues); see [CONTRIBUTING.md](CONTRIBUTING.md).")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- fixed-scope engagements: shared pieces
def slug(s):
    """GitHub's heading anchor: lowercase, punctuation dropped, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", s.lower()).replace(" ", "-")


def channels_md():
    out = [f"[email](mailto:{EMAIL})"]
    if UPWORK_URL:
        out.append(f"[Upwork]({UPWORK_URL})")
    if FIVERR_URL:
        out.append(f"[Fiverr Pro]({FIVERR_URL})")
    return ", ".join(out[:-1]) + (" or " if len(out) > 1 else "") + out[-1]


def services_md_section(level=2, base="SERVICES.md"):
    """The compact version for the README; SERVICES.md carries the full catalog."""
    hh = "#" * level
    priced = any(PRICING.values())
    L = [f"{hh} Fixed-scope engagements", "",
         "If you need one of these outcomes, I have delivered it before. Each one is sold as a fixed scope, "
         "with the deliverables and an acceptance checklist agreed in writing before work starts.", ""]
    L += ["| Engagement | What you get |" + (" Price |" if priced else ""),
          "|---|---|" + ("---|" if priced else "")]
    for s in SERVICES:
        row = f"| **[{s['name']}]({base}#{slug(s['name'])})** | {s['pitch']} |"
        L.append(row + (f" {price_line(s['key'])} |" if priced else ""))
    L.append("")
    if not priced:
        L += ["Each is a fixed price, quoted after the written intake. Proof and full scope for each are in "
              f"[{base}]({base}).", ""]
    L += ["**How I work:**", ""] + [f"- **{h_}** {t}" for h_, t in WORKING_STYLE[:3]] + [""]
    L += [f"**How I use AI.** {AI_USE}", ""]
    L += [f"**Start with the [written intake]({INTAKE}).** It takes about ten minutes, and I reply with a written "
          f"scope and a fixed price. Send it by {channels_md()}."]
    return L


def services_page():
    L = ["# Fixed-scope AI engineering engagements", "",
         f"**{NAME}** · {VARIANTS['freelance']['title']}", "",
         "Five outcomes I have already delivered in production, each sold as a fixed scope. You get a written "
         "scope, a fixed price and an acceptance checklist before any work starts, and documentation your team "
         "can run without me when it ends.", "",
         "**Contents:** " + " · ".join(f"[{s['name']}](#{slug(s['name'])})" for s in SERVICES)
         + " · [How I work](#how-i-work) · [How I use AI](#how-i-use-ai) · [Start](#start)", ""]
    for s in SERVICES:
        L += [f"## {s['name']}", "", f"**The problem.** {s['problem']}", "", "**What you get:**", ""]
        L += [f"- {i}" for i in s["includes"]] + [""]
        if s.get("note"):
            L += [f"_{s['note']}_", ""]
        L += [f"**Proof.** {s['proof']}", "", f"**Price.** {price_line(s['key'])}", ""]
    L += ["## How I work", ""] + [f"- **{h_}** {t}" for h_, t in WORKING_STYLE] + [""]
    L += ["## How I use AI", "", AI_USE, ""]
    L += ["## Start", "",
          f"Answer the [written intake]({INTAKE}) and send it by {channels_md()}. I reply with a written scope, "
          "a fixed price and an acceptance checklist. If the brief is not a good fit, I will say so plainly and, "
          "where I can, point you to someone better suited.", "",
          f"The full résumé is in the [README](README.md); a résumé focused on contract work is "
          f"[here]({VARIANTS['freelance']['stem']}.pdf). This page is generated by `tools/build_resume.py` "
          "from the same facts as the résumé, so the two cannot disagree.", ""]
    return "\n".join(L)


def fenced(label, text, limit=None):
    count = f"{len(text):,}" + (f" / {limit:,}" if limit else "")
    return [f"**{label}** ({count} characters)", "", "```text", text, "```", ""]


def upwork_title():
    return "AI Platform Engineer | RAG, LLM Gateways, Okta/Entra & AI Security"


UPWORK_SKILLS = ["Retrieval Augmented Generation", "Large Language Model", "AI Agent Development", "Python",
                 "FastAPI", "PostgreSQL", "Kubernetes", "Microsoft Azure", "Microsoft Entra ID", "Okta",
                 "Identity & Access Management", "Application Security", "Security Assessment", "SOC 2",
                 "DevSecOps", "Terraform", "OpenAI API", "Claude", "TypeScript", "API Integration"]


def upwork_overview():
    hook = ("I put AI into production for teams that can't afford a leak: RAG chatbots on your own documents, LLM "
            "gateways with spend caps and audit trails, and security reviews that find the gaps first. 13 years in "
            "production; written-first, fixed-scope.")
    L = [hook, "", "What I deliver, each at a fixed price:"]
    L += [f"• {s['name']}: {s['pitch']}" for s in SERVICES]
    L += ["", "Proof:"] + [f"• {s['proof']}" for s in SERVICES]
    L += ["", "How I work:"] + [f"• {h_} {t}" for h_, t in WORKING_STYLE]
    L += ["", f"How I use AI: {AI_USE}", "",
          "Open source: I maintain vibey, an MIT-licensed conductor for AI coding agents, so you can read the code "
          "I write in public before you hire me.", "",
          "Message me with the outcome you need. I'll send a short written intake, then a fixed scope and price."]
    return hook, "\n".join(L)


def upwork_page():
    hook, overview = upwork_overview()
    title = upwork_title()
    assert len(title) <= LIMITS["upwork_title"], f"Upwork title {len(title)} > {LIMITS['upwork_title']}"
    assert len(hook) <= LIMITS["upwork_fold"], f"Upwork hook {len(hook)} > {LIMITS['upwork_fold']}"
    assert len(overview) <= LIMITS["upwork_overview"], f"Upwork overview {len(overview)} > {LIMITS['upwork_overview']}"
    assert len(UPWORK_SKILLS) <= LIMITS["upwork_skills"], "too many Upwork skills"
    L = ["# Upwork profile copy", "",
         "Generated by `tools/build_resume.py` from the same facts as the résumé. Paste each block into the "
         "matching field; the build fails if any block passes the platform's limit. Upwork restricts contact "
         "details before a contract starts, so this copy contains none.", "",
         "Platform rules this kit keeps: every proposal is written and sent by a person; no tool logs in or bids "
         "on my behalf; payments for Upwork clients stay on Upwork. Clients I already know come in as Direct "
         "Contracts.", ""]
    L += fenced("Title", title, LIMITS["upwork_title"])
    L += fenced(f"Overview. The first {len(hook)} characters show before \"more\"", overview,
                LIMITS["upwork_overview"])
    L += [f"**Skills** ({len(UPWORK_SKILLS)} / {LIMITS['upwork_skills']})", "", ", ".join(UPWORK_SKILLS), ""]
    L += ["## Portfolio items", ""]
    for s in SERVICES:
        L += fenced("Title", s["portfolio"], LIMITS["upwork_portfolio_title"])
        L += [f"{s['problem']} {s['proof']}", ""]
    L += ["## Project Catalog", ""]
    for s in SERVICES:
        L += [f"### {s['name']}", "", s["pitch"], ""] + [f"- {i}" for i in s["includes"]]
        L += ["", f"**Price.** {price_line(s['key'])}", ""]
    L += ["## Proposals", "", "Start from [proposal-template.md](proposal-template.md). Keep proposals to about "
          "150–250 words: their outcome in their words, one proof line, three steps, one question.", ""]
    return "\n".join(L)


def fiverr_description(s):
    text = (f"{s['problem']}\n\nWhat you get:\n" + "\n".join(f"• {i}" for i in s["includes"])
            + (f"\n\n{s['note']}" if s.get("note") else "")
            + f"\n\nProof: {s['proof']}\n\n"
            "How I work: you send a short written brief first, and calls are optional. Scope, price and an "
            "acceptance checklist are fixed before work starts. I use AI coding agents under my own review and "
            "will tell you which parts were agent-assisted.")
    assert len(text) <= LIMITS["fiverr_description"], f"Fiverr description for {s['key']}: {len(text)} chars"
    return text


def fiverr_page():
    L = ["# Fiverr Pro gig copy", "",
         "Generated by `tools/build_resume.py`. Apply through Fiverr Pro rather than the standard marketplace: "
         "Pro vetting weighs off-platform experience, so attach "
         f"[{VARIANTS['freelance']['stem']}.pdf](../{VARIANTS['freelance']['stem']}.pdf). Fiverr does not allow "
         "external links or contact details in gigs, so this copy contains none.", "",
         "Fiverr's AI guidelines ask for original, customized work, human judgment in every delivery, and "
         "disclosure of AI use when a buyer asks. Each description below discloses it up front.", ""]
    for n, s in enumerate(SERVICES, 1):
        L += [f"## Gig {n}: {s['name']}", ""]
        L += fenced("Title", s["gig"], LIMITS["fiverr_title"])
        L += fenced("Description", fiverr_description(s), LIMITS["fiverr_description"])
        L += [f"**Price.** {price_line(s['key'])}", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- plain text
def txt(v):
    L = [NAME.upper(), v["title"], v["tagline"], "", " | ".join(t for t, _ in CONTACT), "", v["availability"], ""]
    L += ["SUMMARY", v["summary"], "", "HIGHLIGHTS"] + [f"- {b}" for b in v["highlights"]] + [""]
    if v.get("services"):
        L += ["FIXED-SCOPE ENGAGEMENTS"] + [f"- {s['name']}: {s['pitch']}" for s in SERVICES]
        L += [f"{SERVICES_NOTE} Details and proof: {REPO}/blob/HEAD/SERVICES.md", ""]
    L.append("EXPERIENCE")
    for e, bullets in jobs(v):
        L += ["", f"{e['org']} | {e['loc']}", f"{e['role']} | {span(e['start'], e['end'])}"]
        L += [f"- {b}" for b in bullets]
    L += ["", "EARLIER EXPERIENCE"]
    L += [f"- {org}, {role}, {loc} ({span(s, e)}). {line}" for org, role, loc, s, e, line in EARLIER]
    L += ["", "SKILLS"] + [f"- {k}: {t}" for k, t in skills(v)]
    L += ["", "OPEN SOURCE"] + [f"- {n} ({u}): {d}" for n, u, d in OPEN_SOURCE]
    L.append(f"Volunteer with me: {JOIN_ME}")
    L += ["", "PUBLICATIONS"] + [f"- {t}. {d} ({u})" for t, d, u, _ in PUBLICATIONS]
    L += ["", "EDUCATION & CERTIFICATION"]
    L += [f"- {s}, {d} ({a}–{b})" for s, d, a, b in EDUCATION] + [f"- {c}, {o} ({y})" for c, o, y in CERTS]
    L.append("")
    return plain("\n".join(L))


# ---------------------------------------------------------------- JSON-LD / JSON Resume
def json_ld(v):
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": NAME,
        "jobTitle": v["title"].split(" · ")[0],
        "description": plain(v["tagline"]),
        "email": f"mailto:{EMAIL}",
        "telephone": PHONE,
        "url": SITE,
        "address": {"@type": "PostalAddress", "addressLocality": CITY, "addressRegion": REGION,
                    "addressCountry": COUNTRY},
        "sameAs": [u for _, _, u in PROFILES] + [SITE, REPO] + [u for u in (UPWORK_URL, FIVERR_URL) if u],
        "knowsAbout": v["keywords"],
        "makesOffer": [offer_ld(s) for s in SERVICES],
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": s} for s, *_ in EDUCATION],
        "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": c,
                           "recognizedBy": {"@type": "Organization", "name": o}} for c, o, _ in CERTS],
        "subjectOf": [{"@type": "CreativeWork", "name": t, "url": u} for t, _, u, _ in PUBLICATIONS]
                     + [{"@type": "SoftwareSourceCode", "name": "vibey", "codeRepository": VIBEY,
                         "license": "https://opensource.org/licenses/MIT"}],
    }


def offer_ld(s):
    o = {"@type": "Offer", "name": s["name"], "description": s["pitch"],
         "url": f"{REPO}/blob/HEAD/SERVICES.md#{slug(s['name'])}",
         "itemOffered": {"@type": "Service", "name": s["name"], "description": s["problem"],
                         "serviceType": "Software engineering consulting", "areaServed": "Remote"}}
    if PRICING.get(s["key"]):
        o["priceSpecification"] = {"@type": "PriceSpecification", "description": price_line(s["key"])}
    return o


def json_resume():
    v = VARIANTS["default"]
    by_key = {e["key"]: e for e in EXPERIENCE}

    def entry(e, bullets):
        d = {"name": e["org"], "position": e["role"], "location": e["loc"], "startDate": e["start"],
             "highlights": [plain(b) for b in bullets]}
        if e["end"]:
            d["endDate"] = e["end"]
        if e.get("summary"):
            d["summary"] = e["summary"]
        if e.get("url"):
            d["url"] = e["url"]
        return d

    work, volunteer, projects = [], [], []
    for e, bullets in jobs(v):
        if e.get("kind") == "project":
            projects.append({"name": "vibey", "description": plain(bullets[0]), "url": VIBEY,
                             "startDate": e["start"], "roles": [e["role"]],
                             "highlights": [plain(b) for b in bullets[1:]],
                             "keywords": ["agent orchestration", "PostgreSQL", "Python", "MIT"]})
        elif e.get("kind") == "volunteer":
            d = entry(e, bullets)
            volunteer.append({"organization": d.pop("name"), **d})
        else:
            work.append(entry(e, bullets))
    for org, role, loc, s, e, line in EARLIER:
        work.append({"name": org, "position": role, "location": loc, "startDate": s, "endDate": e, "summary": line})

    return {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": {
            "name": NAME, "label": v["title"], "email": EMAIL, "phone": PHONE, "url": SITE,
            "summary": v["summary"],
            "location": {"city": CITY, "region": REGION, "countryCode": COUNTRY},
            "profiles": [{"network": n, "username": u, "url": url} for n, u, url in PROFILES],
        },
        "work": work,
        "volunteer": volunteer,
        "projects": projects,
        "education": [({"institution": s, "studyType": d.split(", ")[0], "area": d.split(", ")[1]} if ", " in d
                       else {"institution": s, "area": d}) | {"startDate": a, "endDate": b}
                      for s, d, a, b in EDUCATION],
        "certificates": [{"name": c, "issuer": o, "date": y} for c, o, y in CERTS],
        "publications": [{"name": t, "summary": d, "url": u, "releaseDate": y} for t, d, u, y in PUBLICATIONS],
        "skills": [{"name": k, "keywords": split_list(t)} for k, t in skills(v)],
        "meta": {"canonical": f"{RAW}/resume.json", "version": "v1.0.0",
                 "lastModified": "2026-09-30"},
    }


# ---------------------------------------------------------------- llms.txt
def llms_txt():
    v = VARIANTS["default"]
    L = [f"# {NAME}", "", f"> {plain(v['title'])}. {plain(v['tagline'])}", ""]
    L += [plain(v["summary"]), "", v["availability"], ""]
    L += ["Key facts, each traceable to the résumé and to public repositories:"]
    L += [f"- {plain(b)}" for b in v["highlights"]]
    L += ["", "## Open source", ""]
    L.append(f"- [vibey]({VIBEY}): conductor for AI coding agents with an append-only PostgreSQL ledger; "
             "MIT; pip install vibey-engine")
    L.append(f"- [vibey documentation]({VIBEY_DOCS}): install, architecture, decision records")
    L.append(f"- [Ledger-Mediated Orchestration (paper)]({PAPER_URL}): vibey's design (not peer reviewed)")
    L.append(f"- [Contribute to vibey]({VIBEY}/blob/develop/CONTRIBUTING.md): how to start")
    L += ["", "## Fixed-scope engagements", "",
          "Available for contract work, each engagement a fixed scope with a written acceptance checklist. "
          "AI use is disclosed: " + AI_USE, ""]
    for s in SERVICES:
        L.append(f"- [{s['name']}]({REPO}/blob/HEAD/SERVICES.md#{slug(s['name'])}): {s['pitch']} "
                 f"Proof: {s['proof']}")
    L.append(f"- [Written intake]({REPO}/blob/HEAD/{INTAKE}): how an engagement starts")
    L += ["", "## Résumé", ""]
    L.append(f"- [Résumé (Markdown)]({REPO}/blob/HEAD/README.md): the full résumé, including open-source work")
    L.append(f"- [Résumé (JSON Resume)]({RAW}/resume.json): structured, machine-readable")
    L.append(f"- [Profile (schema.org JSON-LD)]({RAW}/profile.jsonld): Person, with the engagements as offers")
    for key in VARIANTS:
        vv = VARIANTS[key]
        L.append(f"- [{vv['label']} résumé (text)]({RAW}/{files(vv)['txt']}): {plain(vv['title'])}")
    L += ["", "## Contact", ""]
    L.append(f"- [Email](mailto:{EMAIL})")
    L += [f"- [{n}]({u})" for n, u in (("Upwork", UPWORK_URL), ("Fiverr Pro", FIVERR_URL)) if u]
    L += [f"- [{n}]({u})" for n, _, u in PROFILES]
    L.append(f"- [Personal site]({SITE})")
    L += ["", "## Optional", ""]
    L.append(f"- [Novice to Navigator]({SITE}/novice-to-navigator): plain-English book on RAG chatbots")
    L.append(f"- [Volunteer with Adam]({JOIN_ME})")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- CITATION.cff
def citation_cff():
    v = VARIANTS["default"]
    kw = "\n".join(f"  - {k}" for k in v["keywords"])
    return f"""# Citation metadata. GitHub renders this as "Cite this repository"; citation managers read it directly.
# Generated by tools/build_resume.py. Format: Citation File Format 1.2.0.
cff-version: 1.2.0
message: If you reuse the résumé builder, please cite this repository. To cite vibey, cite the paper below.
title: "{NAME}: résumé and single-source résumé builder"
type: software
abstract: >-
  The résumé of {NAME} ({plain(v['title'])}) and the single-file Python builder that
  renders it to Markdown, plain text, Word, PDF, JSON Resume and llms.txt from one set of facts.
authors:
  - family-names: Steinberger
    given-names: Adam Matthew
    email: {EMAIL}
    website: {SITE}
license: MIT
repository-code: {REPO}
url: {SITE}
keywords:
{kw}
references:
  - type: software
    title: vibey
    authors:
      - family-names: Steinberger
        given-names: Adam Matthew
    repository-code: {VIBEY}
    url: {VIBEY_DOCS}
    license: MIT
  - type: article
    title: >-
      Ledger-Mediated Orchestration: Vendor-Independent Autonomous Software Delivery over
      a Pool of Coding Agents
    authors:
      - family-names: Steinberger
        given-names: Adam Matthew
    year: 2026
    url: {PAPER_URL}
    notes: Not peer reviewed.
"""


# ---------------------------------------------------------------- HTML (→ PDF)
CSS = """
@page { size: Letter; margin: 0.4in 0.45in; }
:root { --ink: #1b1f24; --muted: #59626d; --accent: #1f4e8c; --rule: #d5dbe3; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; color: var(--ink);
       font-size: 9pt; line-height: 1.24; margin: 0; }
h1 { font-size: 20pt; line-height: 1.1; margin: 0; letter-spacing: -0.2px; }
.title { font-size: 11.5pt; font-weight: 600; color: var(--accent); margin: 2pt 0 0; }
.tagline { color: var(--muted); margin: 2pt 0 5pt; }
.contact { margin: 0 0 3pt; }
.contact a, a { color: var(--accent); text-decoration: none; }
.avail { font-weight: 600; margin: 0 0 4pt; }
h2 { font-size: 9.5pt; text-transform: uppercase; letter-spacing: 0.8px; color: var(--accent);
     border-bottom: 1px solid var(--rule); padding-bottom: 1.5pt; margin: 6pt 0 2.5pt;
     break-after: avoid; page-break-after: avoid; }
p { margin: 0 0 3pt; }
ul { margin: 1pt 0 3pt; padding-left: 12pt; }
li { margin: 0 0 1.2pt; }
.job { margin: 0 0 3pt; }
.early { font-size: 8.6pt; }
.job-head { display: flex; justify-content: space-between; align-items: baseline;
            break-after: avoid; page-break-after: avoid; }
.org { font-weight: 700; font-size: 10pt; }
.loc, .dates, .muted { color: var(--muted); font-weight: 400; }
.dates { white-space: nowrap; }
.role { font-style: italic; margin: 0 0 1pt; break-after: avoid; page-break-after: avoid; }
li b { font-weight: 700; }
.skills li { list-style: none; margin-left: -12pt; }
"""


def html_doc(v):
    L = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
         f"<title>{h(NAME)} · {h(v['title'].split(' · ')[0])}</title>",
         f"<meta name='author' content='{h(NAME)}'>",
         f"<meta name='description' content='{h(plain(v['tagline']))}'>",
         f"<meta name='keywords' content='{h(', '.join(v['keywords']))}'>",
         f"<script type='application/ld+json'>{json.dumps(json_ld(v), ensure_ascii=False)}</script>",
         f"<style>{CSS}</style></head><body>"]
    L.append(f"<header><h1>{h(NAME)}</h1><div class='title'>{h(v['title'])}</div>"
             f"<div class='tagline'>{rich(v['tagline'])}</div>")
    L.append("<div class='contact'>" + " &nbsp;·&nbsp; ".join(
        f"<a href='{h(u)}'>{h(t)}</a>" if u else h(t) for t, u in CONTACT) + "</div>")
    L.append(f"<div class='avail'>{h(v['availability'])}</div></header>")
    L.append(f"<h2>Summary</h2><p>{rich(v['summary'])}</p>")
    L.append("<h2>Highlights</h2><ul>" + "".join(f"<li>{rich(b)}</li>" for b in v["highlights"]) + "</ul>")
    if v.get("services"):
        L.append("<h2>Fixed-scope engagements</h2><ul>"
                 + "".join(f"<li><b>{h(s['name'])}.</b> {h(s['pitch'])}</li>" for s in SERVICES)
                 + f"</ul><p>{h(SERVICES_NOTE)} Details and proof: "
                 f"<a href='{h(REPO)}/blob/HEAD/SERVICES.md'>github.com/adammatthewsteinberger/resume/SERVICES.md</a></p>")
    L.append("<h2>Experience</h2>")
    for e, bullets in jobs(v):
        L.append("<div class='job'><div class='job-head'>"
                 f"<span class='org'>{h(e['org'])} <span class='loc'>· {h(e['loc'])}</span></span>"
                 f"<span class='dates'>{h(span(e['start'], e['end']))}</span></div>"
                 f"<div class='role'>{h(e['role'])}</div><ul>"
                 + "".join(f"<li>{rich(b)}</li>" for b in bullets) + "</ul></div>")
    L.append("<h2>Earlier experience</h2><p class='early'>" + " &nbsp;·&nbsp; ".join(
        f"<b>{h(org)}</b>, {h(role)} <span class='muted'>({h(s[:4])}–{h(e[:4])})</span>. {h(line)}"
        for org, role, loc, s, e, line in EARLIER) + "</p>")
    L.append("<h2>Skills</h2><ul class='skills'>" + "".join(
        f"<li><b>{h(k)}:</b> {rich(t)}</li>" for k, t in skills(v)) + "</ul>")
    L.append("<h2>Open source &amp; publications</h2><ul>"
             + "".join(f"<li><b><a href='{h(u)}'>{h(n)}</a></b>. {h(d)}</li>" for n, u, d in OPEN_SOURCE)
             + "".join(f"<li><b><a href='{h(u)}'>{h(t)}</a></b>. {h(d)}</li>" for t, d, u, _ in PUBLICATIONS)
             + "</ul>")
    L.append("<h2>Education &amp; certification</h2><p>" + " &nbsp;·&nbsp; ".join(
        [f"<b>{h(s)}</b>, {h(d)} ({a}–{b})" for s, d, a, b in EDUCATION]
        + [f"<b>{h(c)}</b>, {h(o)} ({y})" for c, o, y in CERTS]) + "</p>")
    L.append("</body></html>")
    return "".join(L)


def chrome_path():
    for p in (os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")):
        if p and os.path.exists(p):
            return p
    return None


def pdf(v, html_path, pdf_path):
    chrome = chrome_path()
    if not chrome:
        print(f"  skipped {pdf_path}: Chrome not found (set CHROME=...)")
        return
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    with tempfile.TemporaryDirectory() as profile:
        # Headless Chrome sometimes lingers after printing, so wait for a complete PDF
        # (size stable and ending in %%EOF), then stop the process ourselves.
        proc = subprocess.Popen([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                                 "--no-first-run", "--no-default-browser-check", "--disable-extensions",
                                 f"--user-data-dir={profile}", f"--print-to-pdf={os.path.abspath(pdf_path)}",
                                 "file://" + os.path.abspath(html_path)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        last, deadline = -1, time.time() + 90
        while time.time() < deadline:
            time.sleep(0.5)
            if proc.poll() is not None and os.path.exists(pdf_path):
                break
            if os.path.exists(pdf_path):
                size = os.path.getsize(pdf_path)
                with open(pdf_path, "rb") as fh:
                    fh.seek(max(0, size - 1024))
                    done = b"%%EOF" in fh.read()
                if done and size == last:
                    break
                last = size
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
    if not os.path.exists(pdf_path):
        raise RuntimeError(f"Chrome did not produce {pdf_path}")
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("  pypdf not installed: PDF written without metadata")
        return
    writer = PdfWriter(clone_from=PdfReader(pdf_path))
    writer.add_metadata({"/Title": f"{NAME}: {v['title']}", "/Author": NAME,
                         "/Subject": plain(v["tagline"]), "/Keywords": ", ".join(v["keywords"]),
                         "/Creator": "tools/build_resume.py"})
    with open(pdf_path, "wb") as f:
        writer.write(f)


# ---------------------------------------------------------------- DOCX
def docx_doc(v, path):
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    ACCENT, MUTED = RGBColor(0x1F, 0x4E, 0x8C), RGBColor(0x59, 0x62, 0x6D)
    d = Document()
    for s in d.sections:
        s.top_margin = s.bottom_margin = Inches(0.55)
        s.left_margin = s.right_margin = Inches(0.6)
    base = d.styles["Normal"]
    base.font.name = "Calibri"
    base.font.size = Pt(10)
    base.paragraph_format.space_after = Pt(2)

    def link(par, url, text):
        r_id = par.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                                  is_external=True)
        hl = OxmlElement("w:hyperlink"); hl.set(qn("r:id"), r_id)
        run = OxmlElement("w:r"); rpr = OxmlElement("w:rPr")
        c = OxmlElement("w:color"); c.set(qn("w:val"), "1F4E8C"); rpr.append(c)
        run.append(rpr); t = OxmlElement("w:t"); t.text = text; run.append(t); hl.append(run)
        par._p.append(hl)

    def heading(text):
        p = d.add_paragraph(); r = p.add_run(text.upper()); r.bold = True; r.font.size = Pt(10.5)
        r.font.color.rgb = ACCENT
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(2)
        ppr = p._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
        for k, val in (("w:val", "single"), ("w:sz", "4"), ("w:space", "1"), ("w:color", "D5DBE3")):
            b.set(qn(k), val)
        bdr.append(b); ppr.append(bdr)

    def add_rich(par, text):
        for t, style in spans(text):
            r = par.add_run(t)
            if style == "b":
                r.bold = True
            elif style == "i":
                r.italic = True
            elif style == "muted":
                r.font.color.rgb = MUTED

    def bullet(text):
        p = d.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(1.5)
        add_rich(p, text)
        return p

    p = d.add_paragraph(); r = p.add_run(NAME); r.bold = True; r.font.size = Pt(20)
    p = d.add_paragraph(); r = p.add_run(v["title"]); r.bold = True; r.font.size = Pt(11.5); r.font.color.rgb = ACCENT
    p = d.add_paragraph(); r = p.add_run(plain(v["tagline"])); r.font.color.rgb = MUTED
    p = d.add_paragraph()
    for i, (t, u) in enumerate(CONTACT):
        if i:
            p.add_run("  ·  ")
        link(p, u, t) if u else p.add_run(t)
    p = d.add_paragraph(); r = p.add_run(v["availability"]); r.bold = True

    heading("Summary"); add_rich(d.add_paragraph(), v["summary"])
    heading("Highlights")
    for b in v["highlights"]:
        bullet(b)
    if v.get("services"):
        heading("Fixed-scope engagements")
        for s in SERVICES:
            bullet(f"**{s['name']}.** {s['pitch']}")
        p = d.add_paragraph(SERVICES_NOTE + " Details and proof: ")
        link(p, f"{REPO}/blob/HEAD/SERVICES.md", "SERVICES.md")
    heading("Experience")
    for e, bullets in jobs(v):
        p = d.add_paragraph(); p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(e["org"]); r.bold = True; r.font.size = Pt(10.5)
        p.add_run(f"  ·  {e['loc']}").font.color.rgb = MUTED
        p.paragraph_format.tab_stops.add_tab_stop(Inches(7.3), alignment=2)
        p.add_run(f"\t{span(e['start'], e['end'])}").font.color.rgb = MUTED
        p = d.add_paragraph(); p.paragraph_format.space_after = Pt(1); p.paragraph_format.keep_with_next = True
        r = p.add_run(e["role"]); r.italic = True
        for b in bullets:
            bullet(b)
    heading("Earlier experience")
    for org, role, loc, s, e, line in EARLIER:
        bullet(f"**{org}**, {role} _({span(s, e)})_. {line}")
    heading("Skills")
    for k, t in skills(v):
        bullet(f"**{k}:** {t}")
    heading("Open source & publications")
    for n, u, desc in OPEN_SOURCE:
        p = d.add_paragraph(style="List Bullet"); link(p, u, n); p.add_run(f". {desc}")
    for t, desc, u, _ in PUBLICATIONS:
        p = d.add_paragraph(style="List Bullet"); link(p, u, t); p.add_run(f". {desc}")
    heading("Education & certification")
    for s, deg, a, b in EDUCATION:
        bullet(f"**{s}**, {deg} ({a}–{b})")
    for c, o, y in CERTS:
        bullet(f"**{c}**, {o} ({y})")

    cp = d.core_properties
    cp.author = NAME
    cp.title = f"{NAME}: {v['title']}"
    cp.subject = plain(v["tagline"])
    kept = []  # Word caps this property at 255 characters; keep whole keywords, in priority order
    for k in v["keywords"]:
        if len(", ".join(kept + [k])) > 255:
            break
        kept.append(k)
    cp.keywords = ", ".join(kept)
    d.save(path)


# ---------------------------------------------------------------- write
def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)


check_services()
os.makedirs(os.path.join(OUT, "freelance"), exist_ok=True)
write("README.md", md())
write("SERVICES.md", services_page())
write("freelance/upwork.md", upwork_page())
write("freelance/fiverr-pro.md", fiverr_page())
write("profile.jsonld", json.dumps(json_ld(VARIANTS["default"]), indent=2, ensure_ascii=False) + "\n")
write("resume.json", json.dumps(json_resume(), indent=2, ensure_ascii=False) + "\n")
write("llms.txt", llms_txt())
write("CITATION.cff", citation_cff())
for key, v in VARIANTS.items():
    f = files(v)
    write(f["txt"], txt(v))
    write(f["html"], html_doc(v))
    docx_doc(v, os.path.join(OUT, f["docx"]))
    if MAKE_PDF:
        pdf(v, os.path.join(OUT, f["html"]), os.path.join(OUT, f["pdf"]))
    print(f"wrote {key}: {', '.join(sorted(f.values()))}")
print("wrote README.md, SERVICES.md, freelance/, profile.jsonld, resume.json, llms.txt, CITATION.cff →", OUT)
