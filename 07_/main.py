import math

def fem(a, b, c):
    # ( a ^ b ) % c
    #fast modulo for a ^ b
    bin_b = str(bin(b)[2:])
    a_exp = [a % c]
    for i in range(1, len(bin_b)):
        a_exp.append(a_exp[i-1] ** 2 % c)
    a_exp.reverse()
    
    result = 1

    for i in range(len(bin_b)):
        if bin_b[i] == "1":
            result *= a_exp[i]
    result = result % c

    return result

def sieve(n):

    prime = [True for i in range(n+1)]

    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * 2, n+1, p):
                prime[i] = False
        p += 1

    ans = []

    for p in range(2, n):
        if prime[p]:
            ans.append(p)
    return ans

def JHA(m, p, q):
    n1, n2, sp = 0, 0, 0
    vowels = ['a', 'e', 'i', 'u', 'o', 'A', 'E', 'I', 'U', 'O']
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W',
                'X', 'Y', 'Z', 'b', 'c', 'd', 'f', 'g', 'h', 'j',
                'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',
                'w', 'x', 'y', 'z']

    for i in m:
        if i in vowels:
            n1 += 1
        elif i in consonants:
            n2 += 1
        elif i == " ":
            sp += 1


    power = (7 * n1) - (3 * n2) + (sp * sp)

    return fem(q, power, p)

#input p, g, k, r, m

def public_info(p, k, g):
    primes = sieve(p-1)
    primes.reverse()
    q = 0
    for prime in primes:
        if (p - 1) % prime == 0:
            q = prime
            break
    if k > q:
        return "r can't be bigger than q."

    public_key = fem(g, k, p)
    deposit = (public_key, g, p, q)

    return q, deposit

def SG(m, p, k, g, r):
    q, deposit = public_info(p, k, g)
    print("p:", p, "\nq:", q, "\nk", k)
    
    if r < q:
        t = JHA(m, p, q)
        print("JHA:", t)
        print("g:", g)
        x = (fem(g, k, p)) % q
        y = (1 / r) * (t + ( k *  x ))
        print("r:", r)
        print("PRK:", deposit)
        return (x, y % q)
    else:
        return "r can't be bigger than q."

def get_text(filepath):
    with open(filepath, 'r') as wf:
        data = wf.read()
    return data

def test_SG():
    m = input("Input m: ")
    p = int(input("Input p: "))
    k = int(input("Input k: "))
    g = int(input("Input g: "))
    r = int(input("Input r: "))

    print(SG(m, p, k, g, r))

def test_SGfile():
    path = input("Input file path: ")
    m = get_text(path)
    print("Text from file:", m)
    p = int(input("Input p: "))
    k = int(input("Input k: "))
    g = int(input("Input g: "))
    r = int(input("Input r: "))

    print(SG(m, p, k, g, r))


while True:
    tx = input("File or input (f/i)")
    if tx == 'f':
        test_SGfile()
    elif tx == 'i':
        test_SG()
    else:
        break