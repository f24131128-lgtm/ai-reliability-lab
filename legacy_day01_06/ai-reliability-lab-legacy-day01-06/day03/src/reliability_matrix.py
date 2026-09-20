import csv, sys
from collections import defaultdict, Counter
from pathlib import Path

def norm(s): return " ".join(s.strip().lower().split())

def quadrant(acc, cons, threshold=.8):
    if acc >= threshold and cons >= threshold: return "又準又穩"
    if acc >= threshold and cons < threshold: return "準但不穩"
    if acc < threshold and cons >= threshold: return "穩但不準"
    return "又不準又不穩"

def main():
    path = Path(sys.argv[1]) if len(sys.argv)>1 else Path("data/demo_results.csv")
    groups=defaultdict(list)
    with path.open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            groups[r["question_id"]].append(r)

    all_acc=[]; all_cons=[]
    print("AI Reliability Lab — Day 3")
    print("="*66)
    print(f'{"Question":<10} {"Accuracy":>10} {"Consistency":>13}  Quadrant')
    print("-"*66)
    for q, rows in groups.items():
        exp=norm(rows[0]["expected"])
        acts=[norm(r["actual"]) for r in rows]
        acc=sum(a==exp for a in acts)/len(acts)
        cons=Counter(acts).most_common(1)[0][1]/len(acts)
        all_acc.append(acc); all_cons.append(cons)
        print(f"{q:<10} {acc:>9.0%} {cons:>12.0%}  {quadrant(acc,cons)}")
    print("-"*66)
    if all_acc:
        print(f"Mean       {sum(all_acc)/len(all_acc):>9.0%} {sum(all_cons)/len(all_cons):>12.0%}")
        print("\n提醒：Consistency 高不代表答案正確；Accuracy 高也不代表每次可靠。")

if __name__=="__main__":
    main()
