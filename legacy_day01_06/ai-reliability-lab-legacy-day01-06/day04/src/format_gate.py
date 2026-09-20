import csv,json,sys
from pathlib import Path
def check(text,keys):
    try: obj=json.loads(text.strip())
    except: return False,"invalid_json"
    if not all(k in obj for k in keys): return False,"missing_key"
    return True,"ok"
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/demo_format_cases.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8-sig"))); passed=0
for r in rows:
    ok,why=check(r["output"],[x.strip() for x in r["required_keys"].split(",")])
    passed+=ok; print(r["case_id"],"PASS" if ok else "FAIL",why)
rate=passed/len(rows)
print(f"Format pass rate: {passed}/{len(rows)} = {rate:.0%}")
print("QUALITY GATE:","PASS" if rate==1 else "BLOCK")
