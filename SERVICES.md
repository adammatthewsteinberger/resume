# Fixed-scope AI engineering engagements

**Adam Matthew Steinberger** · Independent AI Platform Engineer · fixed-scope AI, identity and security work

Five outcomes I have already delivered in production, each sold as a fixed scope. You get a written scope, a fixed price and an acceptance checklist before any work starts, and documentation your team can run without me when it ends.

**Contents:** [AI codebase and security review](#ai-codebase-and-security-review) · [Production RAG chatbot in 30 days](#production-rag-chatbot-in-30-days) · [LLM cost and policy gateway](#llm-cost-and-policy-gateway) · [Okta and Entra ID governance fixes](#okta-and-entra-id-governance-fixes) · [SOC 2 and OWASP LLM Top 10 readiness for an AI feature](#soc-2-and-owasp-llm-top-10-readiness-for-an-ai-feature) · [How I work](#how-i-work) · [How I use AI](#how-i-use-ai) · [Start](#start)

## AI codebase and security review

**The problem.** Your AI feature or fast-grown codebase is about to meet customers or an auditor, and you need to know what will break or leak before they find it.

**What you get:**

- Findings ranked by severity, each with the file, the risk and the fix
- A one-page executive summary for the people who won't read the report
- A phased roadmap: fix this week, fix this quarter, and what can wait
- A written walkthrough of the results, with a call if you want one

**Proof.** Reviewed a 59,000-line codebase in 10 hours and found missing auth middleware and 5% test coverage. My pre-release reviews have caught an auth bypass, path traversal and SSRF.

**Price.** Fixed price, quoted after the written intake.

## Production RAG chatbot in 30 days

**The problem.** You want staff or customers to get answers from your own documents, running in weeks rather than quarters, without your data leaving your control.

**What you get:**

- A chatbot that answers from your documents and shows the source for each answer
- An evaluation set of real questions, so quality is measured rather than guessed
- Monitoring on every request, plus a runbook for whoever owns it next
- Two tiers: cloud models, or fully self-hosted so no data leaves your servers

**Proof.** Delivered two RAG chatbots in 30 days each: one fully self-hosted for a non-profit (Mistral-7B, FAISS and vLLM, no external dependencies) and one cloud-based for a sales agency.

**Price.** Fixed price, quoted after the written intake.

## LLM cost and policy gateway

**The problem.** Your teams call several AI vendors with keys scattered through their apps, and nobody can say what it costs or who sent what.

**What you get:**

- One OpenAI-compatible API in front of the vendors you already use
- Per-project model allowlists, rate limits and hard spend caps
- A tamper-evident audit trail of every call and what it cost
- Sign-in through your identity provider, so apps hold no vendor keys

**Proof.** Sole architect of a ~54k-line gateway in front of six vendors; three product teams moved onto it and retired the credentials their apps held.

**Price.** Fixed price, quoted after the written intake.

## Okta and Entra ID governance fixes

**The problem.** Access grew by hand. Now there are stale groups, admins nobody remembers granting, and an access review each audit season that nobody fully trusts.

**What you get:**

- An access review that names the risky grants
- Groups, roles and policies declared in Git and applied by a pipeline
- Drift detection: safe drift fixed automatically, risky changes held for approval
- A runbook your team can follow without me

**Proof.** Sole author of two identity-governance-as-code control planes covering 40 resource kinds with no stored tenant secrets; identity advisory for a SOX-regulated enterprise of about 5,700 identities.

**Price.** Fixed price, quoted after the written intake.

## SOC 2 and OWASP LLM Top 10 readiness for an AI feature

**The problem.** A customer's security questionnaire just asked how your AI feature handles prompt injection and data leakage, and you need a straight answer backed by evidence.

**What you get:**

- A STRIDE threat model of the feature
- A control-gap list mapped to SOC 2, the OWASP LLM Top 10 and the NIST AI RMF
- A remediation plan in priority order
- Plain-language answers you can reuse in security questionnaires

_This is readiness work, not an audit opinion; only a licensed CPA firm issues a SOC 2 report._

**Proof.** Wrote the SOC 2 readiness assessment and STRIDE threat model for a report platform, and mapped an AI gateway's controls to the OWASP LLM Top 10 and NIST AI RMF.

**Price.** Fixed price, quoted after the written intake.

## How I work

- **Written first.** Every engagement starts with a short written intake instead of a discovery call. You answer on your own time, and I reply with a written scope. Calls are welcome, never required.
- **Fixed scope, fixed price.** Deliverables and an acceptance checklist are agreed in writing before work starts, so we both know what done looks like.
- **Predictable replies.** I answer messages in set windows each weekday, US Eastern time, so you always know when to expect a reply.
- **Risks in writing, early.** If something threatens the date or the scope, you get a short written note with options the day I find it.
- **A few clients at a time.** I take two or three engagements at once, so each one gets focused attention.
- **Handoffs that hold.** Every engagement ends with documentation and a handoff your team can run without me.

## How I use AI

I build with AI coding agents, run through vibey under the same tests and review gates I would hold a person to. I scope, review and sign off on every deliverable myself, and I will tell you which parts were agent-assisted. For sensitive work I switch off any platform or vendor setting that would let your code or messages train a model.

## Start

Answer the [written intake](freelance/intake.md) and send it by [email](mailto:adam@matthewsteinberger.com). I reply with a written scope, a fixed price and an acceptance checklist. If the brief is not a good fit, I will say so plainly and, where I can, point you to someone better suited.

The full résumé is in the [README](README.md); a résumé focused on contract work is [here](adam-steinberger-resume-freelance.pdf). This page is generated by `tools/build_resume.py` from the same facts as the résumé, so the two cannot disagree.
