# NovaSpark Autonomous Marketing OS

A local-first operating system for NovaSpark's AI-assisted client acquisition and delivery workflow.

## Goal

Business data → lead research → qualified prospect → approved outreach → sales conversation → proposal → payment confirmation → onboarding → service delivery → QA → client report.

## Design principles

- Local-first: no domain, paid hosting, or paid AI API required for the core prototype.
- Human approval for financial commitments, contracts, pricing exceptions, and high-impact external actions.
- Deterministic tools for storage, validation, calculations, and workflow state.
- Agents reason within explicit roles and permissions.
- Client data is isolated by workspace.
- External integrations are adapters, not hard dependencies.

## Initial architecture

- `core/ceo`: Alex CEO orchestration.
- `core/planner`: objective decomposition and task planning.
- `core/orchestrator`: dependency-aware task execution.
- `core/approvals`: human approval gates.
- `core/execution`: execution lifecycle.
- `agents/`: specialist roles.
- `data/`: leads, clients, and projects.
- `memory/`: structured company/client memory.
- `workflows/`: reusable acquisition and delivery workflows.
- `dashboard/`: local operator interface.
- `database/`: local persistence.
- `tools/`: deterministic integrations.

## Safety boundaries

The system must not impersonate people, fabricate claims, promise guaranteed results, or send uncontrolled bulk outreach. External messaging must respect applicable platform rules and opt-out requirements.

## Development

The first milestone is a fully runnable local workflow using SQLite and a mock/local model adapter. Paid providers can be added later without replacing the core orchestration layer.
