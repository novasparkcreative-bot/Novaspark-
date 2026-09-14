# NovaSpark Core

This directory contains the CEO, planning, orchestration, approval, and execution layers.

## Runtime contract

1. CEO receives an objective.
2. Planner decomposes it into tasks.
3. Orchestrator executes dependency-aware tasks.
4. Approval gates pause high-impact actions.
5. Execution records outcomes.
6. Memory stores reusable lessons and client context.
