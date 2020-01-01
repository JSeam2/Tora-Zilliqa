
def execute(inp, expr):
    glb = {}
    outp = {}

    glb['inp'] = inp
    glb['outp'] = outp

    exec(expr, glb)
    return glb['outp']


inp = [1, 2]
expr = "x = inp[0]    \ny = inp[1]    \noutp = x + y"
print(execute(inp, expr))
