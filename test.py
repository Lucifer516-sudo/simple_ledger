



def foo(text: str) -> str:
    return "Rs. " + text

def foo2(text: str) -> str:
    return "Rs. " + text + ".00"

def foo3(text: str) -> str:
    return "Rupees. " + text + " only /-"

col = [
        foo,
        foo2,
        foo3,
]

rows = [
        ["10","20","30"],
        ["100","200","300"],
        ["1000","2000","3000"],
]

"""
loop - 1:
c1(r11)
c1(r21)
c1(r31)
c1(rn1)

loop-2:
c2(r12)
...
General formula:
    Cn(Rmn)
---------------

"""
for n in range(len(col)):
    for m in range(len(rows)):
        rows[m][n] = col[n](rows[m][n])
        print(f"C{n}(R{m}{n})")
print(f"rows:\n {rows}")

