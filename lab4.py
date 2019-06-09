import math

def fem(a, b, c):
    # ( a ^ b ) % c
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

def inside_loop(d):
    x = math.floor(math.sqrt(d))
    if x == math.sqrt(d):
        print("Podwójny pierwiastek")
    else:
        x += 1

    while x < (d+1) / 2:
        y_squared = x*x - d
        y = math.sqrt(y_squared)
        if y_squared > 0 and math.floor(y) == y:
            d_prim = x+y
            d_bis = x-y
            return [d_prim, d_bis]
        else:
            x += 1

    return None

def fermat(a, verbose = False):
    powers = []
    two_k = 2
    while(two_k < a):
        powers.append(two_k)
        two_k *= 2
    diffs = {}
    for power in powers:
        diffs[power] = a / power


    for power, diff in diffs.items():
        if diff % 2 == 1:
            k = math.log(power, 2)
            d = diff

    try:
        res = inside_loop(d)
        if res == None:
            return "{} jest liczbą pierwszą.".format(a)

        primes = []
        for i in res:
            temp = inside_loop(i)

            if temp != None:
                res.append(temp[0])
                res.append(temp[1])
            else:
                primes.append(i)
                continue

        together = 2**k
        factors = {2. : int(k)}
        for i in primes:
            together *= i
            if i in factors:
                factors[i] += 1
            else:
                factors[i] = 1
        if verbose == True:
            print("Rozkład liczby {}:".format(a))
        for key, value in factors.items():
            if verbose == True:
                print("Dzielnik: {}, krotność: {}".format(key, value))

        if int(together) != a:
            if verbose == True:
                print("Something went wrong!")
                print(together)
            return None
        return factors
    except:
        print("Podałes liczbę nieparzystą lub pierwszą.")

def lucas(n):
    try:
        m = n-1
        nums = fermat(m, False)
        xi = []
        for key, value in nums.items():
            xi += [key]
        qs = []
        print(xi)
        for i in range(2, m):
            qs.append(i)

        for q in qs:
            matches = 0
            for x in xi:
                if fem(q, int(n/x), n)  != 1:
                    matches += 1
                else:
                    break
            if matches == len(xi):
                print("{} jest liczbą pierwszą.".format(n))
                return "{} jest liczbą pierwszą.".format(n)
        return "Liczba nie jest pierwsza."
    except:
        print("Podałeś liczbę parzystą.")

def lucas_zad(n, q):
    try:
        m = n - 1
        nums = fermat(m,False)
        xi = []
        for key, value in nums.items():
            xi += [key]

        matches = 0

        for x in xi:
            if fem(q, int(n/x), n) != 1:
                matches += 1

        if matches == len(xi):
            print("{} jest liczbą pierwszą ( q = {} ).".format(n, q))
            return "{} jest liczbą pierwszą ( q = {} ).".format(n, q)
        else:
            print("Test nie rozstrzyga, czy {} jest liczbą pierwszą ( q = {} ).".format(n, q))
            return "Test nie rozstrzyga, czy {} jest liczbą pierwszą. ( q = {} )".format(n, q)

    except:
        print("Podałes liczbę parzystą.")

def test_fem():
    print("######### Szybkie potęgowanie modulo #########")
    a = int(input("Podaj a: "))
    b = int(input("Podaj b: "))
    c = int(input("Podaj c :"))
    print("(a ^ b) % c ==", fem(a, b, c))

def test_fermat():
    print("######### Algorytm Fermata #########")
    a = int(input("Podaj a: "))
    fermat(a, True)

def test_lucas():
    n = int(input("Podaj n: "))
    q = int(input("Podaj q: "))
    lucas_zad(n, q)
test_lucas()
