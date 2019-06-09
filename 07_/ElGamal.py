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

def euler(x):
    #Euler totient function
    res = 0
    for i in range(x):
        if math.gcd(x, i) == 1:
            res += 1
    return res

def is_prime(x):
    #boolean True if prime, false if not prime
    if euler(x) == x-1:
        return True
    else:
        return False


def find_ord(a, b):
    # c = ord_{b} a
    # find multiplicative order
    if math.gcd(a, b) == 1:
        c = 1
        while c:
            if fem(a, c, b) == 1:
                return c
            c += 1

    else:
        print("Numbers aren't coprime!")

def prime_root(a, b):
    # check if a is a prime root of b
    if math.gcd(a, b) == 1:
        if find_ord(a, b) == euler(b):
            return True
        else:
            return False
    else:
        return False

def ElGamal(n, r, k, j, t):
    #cipher with ElGamal algorithm
    if is_prime(n):
        if prime_root(r, n):
            if k in range(1, n-1):
                res = "Podany tekst: {}".format(t)
                a = fem(r, k, n)
                public_key = ( n, r, a )
                private_key = ( n, r, a, k )
                res += "\nKlucz publiczny: {}".format(public_key)
                res += "\nKlucz prywatny: {}".format(private_key)
                if t < n:
                    c1 = fem(r, j, n)
                    c2 = (t * ( a ** j )) % n
                    ciphered_text = (c1, c2)
                    res += "\nZaszyfrowany tekst: {}".format(ciphered_text)

                    unciphered_text = (c2 * (c1 ** (n - 1 - k))) % n
                    res += "\nOdszyfrowany tekst: {}".format(unciphered_text)
                    res += "\n"
                    return res
                
                else:
                    return "Text can't be bigger than n."
            else:
                return "k is in wrong range."
        else:
            return "{} isn't a prime root of {}.".format(r, n)
    else:
        return "{} isn't prime!".format(n)

def test_elgamal():
    n = int(input("Input n: "))
    r = int(input("Input r: "))
    k = int(input("Input k: "))
    j = int(input("Input j: "))
    t = int(input("Input t: "))

    print(ElGamal(n, r, k, j, t))

test_elgamal()