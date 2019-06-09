import math

def sieve(n):

    prime = [True for i in range(n+1)]
    print(len(prime))
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

def test_sieve(inp = True, *args):
    if inp == True:
        i = input("Podaj pierwszą liczbę (i): ")
        j = input("Podaj drugą liczbę (j): ")
        i = int(i)
        j = int(j)
    else:
        i = args[0]
        j = args[1]
    try:
        x = sieve(3000000)
        return x[i-1], x[j-1]
    except:
        x = sieve(10000000)
        return x[i-1], x[j-1]

def euklides(a, b):
    global second
    global y
    global first
    global x
    global nwd

    if b == 0:
        nwd = a
        first = a
        return
    else:
        euklides(b, a%b)

    #print(y, "*", second, " + ", x, "*",  first)
    t = y
    y = (x - math.floor(a/b) * y)
    second = b
    x = t
    first = a
first = 0
x = 1
second = 0
y = 0
nwd = 0
def test_euklides(inp = True, *args):
    if inp == True:
        i = input("Podaj pierwszą liczbę: ")
        j = input("Podaj drugą liczbę: ")
        a = int(i)
        b = int(j)
    else:
        a = args[0]
        b = args[1]
    euklides(a, b)
    if inp == True:
        print("NWD({}, {}) = {}, x = {}, y = {}".format(a, b, nwd, x, y))
    return (nwd, x, y)

def get_x(e, m):
    x = -1
    a, x, y = test_euklides(False, e, m)
    while x < 0:
        x += m
    return x


def keygen():
    p, q = test_sieve()
    e = input("Podaj trzecią liczbę (e): ")
    e = int(e)
    n = p * q
    m = (p - 1) * (q - 1)
    d = get_x(e,m)
    public_key = (n, e)
    private_key = (n, d)
    print("Klucz publiczny: {}\nKlucz prywatny: {}".format(public_key, private_key))

#while True:
#    print("######### Generowanie klucza RSA #########")
#    keygen()


#print(test_euklides())
print(test_sieve())
