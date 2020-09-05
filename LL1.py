# S~bPe
# P~AR
# R~AR/`
# A~a=E;
# E~FT
# T~+FT/`
# F~(E)/a/r


from collections import OrderedDict


def getGrammar():
    d = OrderedDict()
    f = open("grammar.txt", "r")

    print('Grammar\n'+f.read())

    f.seek(0)
    for line in f:
        k = ""
        for c in line:
            if c != "~" and k == "":
                d[c] = []
                k = c
            elif c != "~" and c != "\n":
                d[k].append(c)

    f.seek(0)
    nonterminal = []
    terminal = []
    for line in f:
        for c in line:
            if c not in d.keys() and c!= "~" and c!= "\n" and c!= "`" and c!= "/" and c not in terminal:
                terminal.append(c)
            if c>='A' and c<='Z' and c not in nonterminal:
                nonterminal.append(c)

    return d,nonterminal,terminal


def first(d, k):
    fir = ""
    v = d[k]
    j = 1
    for i in range(len(v)):
        if v[i] == "/":
            j = 1
        elif j == 1:
            if v[i] not in d.keys():
                if v[i] not in fir and v[i] != "/":
                    fir = fir + v[i]
                    j = 0
            else:
                a = list(first(d, v[i]))
                while "`" in a and i+1 < len(v) and v[i+1] != "/":
                    a.remove("`")
                    if v[i+1] not in d.keys():
                        a.append(v[i+1])
                    else:
                        a = list(set().union(a, first(d, v[i+1])))
                        i += 1
                a.extend(fir)
                fir = "".join(list(set(a)))
                j = 0
    return fir


def follow(d, n):
    fol = ""
    if n == "S":
        fol += "$"
    for k, v in d.items():
        for i in range(len(v)):
            if v[i] == n:
                if i == len(v) - 1:
                    fol += follow(d, k)
                elif i + 1 < len(v) and v[i + 1] not in d.keys() and v[i+1] != "/" and v[i+1] not in fol:
                    fol += v[i + 1]
                elif i + 1 < len(v) and v[i+1] != "/" and v[i+1] not in fol:
                    a = []
                    for j in fir[v[i + 1]]:
                        a.append(j)
                    if "`" in a:
                        a.remove("`")
                        a.append(follow(d, v[i+1]))
                    fol += "".join(list(set("".join(a))))
                elif k == "S":
                    fol += "$"
    return fol


def parsingTable(d,nonterminals,terminals,fir,fol):
    terminals.append('$')
    #make table
    pt = [ ["_"]*(len(terminals) + 1) for i in range(len(nonterminals) + 1) ]
    for i in range(len(pt)):
        for j in range(len(pt[0])):
            if i == 0 and j != 0:
                pt[i][j] = terminals[j-1]
            if i != 0 and j == 0:
                pt[i][j] = nonterminals[i-1]

    #fill table
    for i in range(1,len(pt)):
        for j in range(1,len(pt[0])):
            if pt[0][j] in fir[pt[i][0]]:
                key = pt[i][0]
                for k,v in d.items():
                    if k == key:
                        val = v

                c = 0
                gotAns = 0
                while c < len(val) and gotAns == 0:
                    if val[c] in nonterminals:
                        if pt[0][j] in fir[val[c]]:
                            rhs = ''
                            for k in range(c, len(val)):
                                if val[k] == '/':
                                    break
                                rhs += val[k]

                            ans = pt[i][0] + '~' + rhs
                            pt[i][j] = ans
                            gotAns = 1

                    elif val[c] == pt[0][j]:
                        rhs = ''
                        for k in range(c,len(val)):
                            if val[k] == '/':
                                break
                            rhs += val[k]

                        ans = pt[i][0] + '~' + rhs
                        pt[i][j] = ans
                        gotAns = 1

                    else:
                        while val[c] != '/' and c < len(val):
                            c += 1
                        if c < len(val):
                            c += 1

            elif pt[0][j] in fol[pt[i][0]] and '`' in fir[pt[i][0]]:
                pt[i][j] = pt[i][0] + '~`'

            elif pt[0][j] in fol[pt[i][0]]:
                pt[i][j] = 'sync'

            else:
                pass

    return pt


def parse(Inp,pt,terminals,nonterminals):
    print('Parsing: ',Inp)
    Stack = ['S','$']
    Action = []
    while Stack[0] != '$':
        print('Stack: ',Stack,'\tAction: ',Action)
        val = Inp[0]
        key = Stack[0]
        if key == val:
            Stack.pop(0)
            Inp = Inp[1:]
            Action.append('Match '+key)
            continue

        for l in range(len(pt)):
            if pt[l][0] == key:
                i = l

        for l in range(len(pt[0])):
            if pt[0][l] == val:
                j = l

        production = pt[i][j]
        if production == '_' or production == 'sync':
            print("Not Accepted")
            return
        Action.append(production)
        rhs = production[2:]
        Stack.pop(0)
        if rhs == '`':
            continue
        for k in range(len(rhs) - 1,-1,-1):
            Stack.insert(0,rhs[k])

    print('Stack: ',Stack,'\tAction: ',Action)
    print("Accepted")



d,nonterminals,terminals = getGrammar()
print("Dictionary:",d)

fir = OrderedDict()
for k, v in d.items():
    fir[k] = []
    fir[k].extend(first(d, k))
print("First:",fir)

fol = OrderedDict()
for k, v in d.items():
    fol[k] = []
    fol[k].extend(follow(d, k))
    fol[k] = list(set(fol[k]))
print("Follow:", fol)

pt = parsingTable(d,nonterminals,terminals,fir,fol)
print("Parsing Table")
for i in range(len(pt)):
    for j in range(len(pt[0])):
        print(pt[i][j],end="\t\t")
    print()

Input = 'ba=r+r;e$'
parse(Input,pt,terminals,nonterminals)
