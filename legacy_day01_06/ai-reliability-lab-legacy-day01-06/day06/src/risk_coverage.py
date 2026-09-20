import csv,sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/demo_risk_coverage.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8-sig"))); rows.sort(key=lambda r:float(r["confidence"]),reverse=True)
print("Threshold  Coverage  Risk")
for t in sorted({float(r["confidence"]) for r in rows},reverse=True):
 a=[r for r in rows if float(r["confidence"])>=t]; risk=sum(r["correct"]=="0" for r in a)/len(a)
 print(f"{t:>9.2f} {len(a)/len(rows):>9.0%} {risk:>6.0%}")
print("Demo confidence is synthetic; it is not calibrated LLM confidence.")
