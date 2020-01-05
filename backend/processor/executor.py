
def execute(inp, exprs):
    glb = {}
    outp = {}

    glb['inp'] = inp
    glb['outp'] = outp

    expr = ""
    for e in exprs:
        expr = expr + "    \n" + e
    exec(expr, glb)
    return glb['outp']


inp = [1, 2]
exprs = ["x = inp[0]", "y = inp[1]", "outp = x + y"]
print(execute(inp, exprs))
