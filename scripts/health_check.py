import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODULES = [
    "database.db",
    "core.ai.adapter",
    "core.orchestrator.engine",
    "core.orchestrator.worker",
    "core.sales.lead_pipeline",
    "core.sales.outreach",
    "core.approvals.gates",
    "core.client.client_lifecycle",
    "core.client.project_manager",
    "core.pipeline",
    "api.server",
    "api.worker_server",
    "dashboard.app",
]


def main():
    failures = []
    for name in MODULES:
        try:
            importlib.import_module(name)
            print(f"OK  {name}")
        except Exception as exc:
            failures.append((name, str(exc)))
            print(f"ERR {name}: {exc}")
    if failures:
        print(f"\nHealth check failed: {len(failures)} module(s)")
        raise SystemExit(1)
    print(f"\nHealth check passed: {len(MODULES)} modules import successfully.")


if __name__ == "__main__":
    main()
