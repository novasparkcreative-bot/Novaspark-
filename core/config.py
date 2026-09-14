from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "novaspark.db"

@dataclass(frozen=True)
class Settings:
    company_name: str = "NovaSpark Creative"
    ceo_name: str = "Alex"
    require_human_approval_for_outreach: bool = True
    require_human_approval_for_payment: bool = True

settings = Settings()
