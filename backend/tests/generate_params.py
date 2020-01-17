def generate_params(s, inputs):
    inp = []
    for i in range(0, len(inputs)):
        s = s.replace(str(inputs[i]), "inp["+str(i)+"]")
        inp.append(inputs[i])
    lines = s.split('\n')
    exprs = []
    for line in lines:
        if line != '' and line != '    ' and not line.startswith('#'):
            exprs.append(line)
    return {"exprs": exprs, "inputs": inp}


if __name__ == "__main__":
    script = """

x = 1
y = 2

outp = x + y

"""
    print(generate_params(script, [1, 2]))
