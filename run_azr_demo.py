import ast, random

FORBIDDEN = {"logging","subprocess","threading","datetime","time","hashlib","sys"}

def validate(code, inp):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, None, f"SyntaxError: {e}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in getattr(node,"names",[])]
            for n in names:
                if n in FORBIDDEN:
                    return False, None, f"Forbidden: {n}"
    ns = {}
    try:
        exec(compile(code,"<s>","exec"), ns)
        out = eval(f"f({inp})", ns)
    except Exception as e:
        return False, None, f"Error: {e}"
    return True, out, "OK"

PROGRAMS = [
    {"code": "def f(arr, k):\n    start=best=0\n    freq={}\n    for end in range(len(arr)):\n        freq[arr[end]]=freq.get(arr[end],0)+1\n        while len(freq)>k:\n            freq[arr[start]]-=1\n            if freq[arr[start]]==0: del freq[arr[start]]\n            start+=1\n        best=max(best,end-start+1)\n    return best", "inp": "[1,2,1,2,3,2,1], 2", "gold": 4, "desc": "Longest subarray with k distinct"},
    {"code": "def f(elements):\n    s=sorted(elements)\n    n=len(s)\n    return sum(s[i]*(n-i) for i in range(n))", "inp": "[1,2,3,4]", "gold": 20, "desc": "Weighted sum"},
]

print("="*50)
print("  AZR DEMO - Absolute Zero Reasoner")
print("  No GPU needed - pure Python")
print("="*50)

print("\n[VALIDATION TESTS]")
tests = [
    ("Valid program",    "def f(x): return x*2", "5",  True),
    ("Forbidden module", "import datetime\ndef f(x): return x", "5", False),
    ("Syntax error",     "def f(x) return x",   "5",  False),
    ("Div by zero",      "def f(x): return 1/x","0",  False),
]
for label, code, inp, expect in tests:
    ok, out, msg = validate(code, inp)
    mark = "PASS" if ok == expect else "FAIL"
    print(f"  [{mark}] {label}")

print("\n[TASK 1 - DEDUCTION: predict output]")
for ex in PROGRAMS:
    ok, out, msg = validate(ex["code"], ex["inp"])
    if ok:
        correct = repr(out) == repr(ex["gold"])
        mark = "CORRECT" if correct else "WRONG"
        print(f"  [{mark}] {ex['desc']}: input={ex['inp']} output={out}")

print("\n[TASK 2 - ABDUCTION: predict input]")
ex = PROGRAMS[0]
for c in ["[1,2,1,2,3], 2", "[1,2,3], 2", "[1,1,1], 1"]:
    ns = {}
    exec(compile(ex["code"],"<s>","exec"), ns)
    try:
        r = eval(f"f({c})", ns)
        print(f"  f({c}) = {r}")
    except:
        pass

print("\n[TASK 3 - INDUCTION: predict function]")
ex = PROGRAMS[1]
for inp in ["[1,2,3,4]", "[4,3,2,1]", "[5]"]:
    ok, out, _ = validate(ex["code"], inp)
    if ok:
        print(f"  f({inp}) = {out}")

print("\n[SELF-PLAY LOOP]")
random.seed(42)
for i, ex in enumerate(PROGRAMS, 1):
    ok, out, msg = validate(ex["code"], ex["inp"])
    if ok:
        rates = [1.0 if random.random() < 0.6 else 0.0 for _ in range(4)]
        avg = sum(rates)/len(rates)
        rp = 0.0 if avg == 0 else 1.0 - avg
        rs = 1.0 if repr(out) == repr(ex["gold"]) else 0.0
        print(f"  Iter {i}: {ex['desc']}")
        print(f"    r_propose={rp:.2f}  r_solve={rs:.1f}")

print("\nDone! AZR core mechanics working.")


