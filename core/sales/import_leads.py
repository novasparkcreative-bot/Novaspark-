import csv
from pathlib import Path
from core.sales.lead_pipeline import add_lead

REQUIRED = {"business_name"}


def import_csv(path: str):
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)
    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = {x.strip() for x in (reader.fieldnames or [])}
        missing = REQUIRED - fields
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
        ids = []
        for row in reader:
            if not (row.get("business_name") or "").strip():
                continue
            ids.append(add_lead(
                row["business_name"], row.get("website", ""), row.get("industry", ""),
                row.get("location", ""), row.get("contact", ""), row.get("notes", "")
            ))
    return ids


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Import NovaSpark leads from CSV")
    parser.add_argument("csv_file")
    args = parser.parse_args()
    ids = import_csv(args.csv_file)
    print(f"Imported {len(ids)} leads")
