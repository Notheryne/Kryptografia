def get_message(mess, n):
    l_hex = mess.split(" ")
    print(l_hex)
    try:
        l_dec = [int(i, 16) for i in l_hex]
        l_bin = [str(bin(i)[2:]) for i in l_dec]
        l_bin_n = [b.zfill(n) for b in l_bin]
        assert all(len(b) == n for b in l_bin_n)
        return l_bin_n

    except ValueError:
        print("You did not enter a hexadecimal number!")

def get_message16(mess):
    l_hex = mess.split(" ")
    try:
        l_dec = [int(i, 16) for i in l_hex]
        l_bin = [str(bin(i)[2:]) for i in l_dec]
        l_bin = ["0" * (4-len(i)) + i for i in l_bin]
        res = ""
        for i in l_bin:
            res += i

        while len(res) % 16 != 0:
            res += "0"
        return res

    except ValueError:
        print("You did not enter a hexadecimal number!")

def get_messagek(mess):
    l_hex = mess.split(" ")
    try:
        l_dec = [int(i, 16) for i in l_hex]
        l_bin = [str(bin(i)[2:]) for i in l_dec]
        l_bin = ["0" * (4-len(i)) + i for i in l_bin]
        res = ""
        for i in l_bin:
            res += i

        if len(res) > 16:
            print("Wrong key!")
            return

        else:
            while len(res) != 16:
                res += "0"

        return res

    except ValueError:
        print("You did not enter a hexadecimal number!")

def add_mod2(l, k):
    if isinstance(l, str):
        l = [l]
    if isinstance(k, str):
        k = [k]
    res = []
    while len(l[0]) != len(k[0]):
        if len(l[0]) > len(k[0]):
            k[0] = '0' + k[0]
        else:
            l[0] = '0' + l[0]
    for i in range(len(l)):
        for j in range(len(k)):
            s = ""
            for c in range(len(k[j])):
                s += str((int(l[i][c]) + int(k[j][c]))%2)
        res.append(s)
    return res

def chop(m, l = 4):
    res = []
    for i in range(0, len(m), l):
        res.append(m[i:l+i])
    return res

def matr_add(n, m):
    n = chop(n)
    m = chop(m)
    if len(n) != len(m):
        print("wrong dimensions")
    res = []
    for i in range(len(n)):
        res.append(add_mod2(n[i], m[i]))
    return res

def bitstring(x):  return bin(x)[2:]
def longdiv(lhs, rhs):
    rem = lhs
    div = rhs
    origlen = len(bitstring(div))

    # first shift left until the leftmost bits line up.
    count = 1
    while (div | rem) > 2*div:
        div <<= 1
        count += 1

    # now keep dividing until we are back where we started.
    quot = 0
    while count>0:
        quot <<= 1
        count -= 1
        divstr = bitstring(div)
        if (rem ^ div) < rem:
            quot |= 1
            rem ^= div
        div >>= 1
    return bitstring(rem)

def mul_poly(n, m):
    s1 = [int(i) for i in n]
    s2 = [int(i) for i in m]

    res = [0]*(len(s1)+len(s2)-1)
    for o1,i1 in enumerate(s1):
        for o2,i2 in enumerate(s2):
            res[o1+o2] += i1*i2

    res = [str(i%2) for i in res]
    res = ''.join(res)

    r = "10011"
    res = longdiv(int(res, 2), int(r, 2))
    if len(res) != 4:
        res = "0" * (4-len(res)) + res
    return res

#print(mul_poly("1011", "1111"))
def matr_mul(n, m):
    n = chop(n)
    m = chop(m)
    res = [add_mod2(mul_poly(n[0], m[0]), mul_poly(n[1], m[2]))[0],
            add_mod2(mul_poly(n[0], m[1]), mul_poly(n[1], m[3]))[0],
            add_mod2(mul_poly(n[2], m[0]), mul_poly(n[3], m[2]))[0],
            add_mod2(mul_poly(n[2], m[1]), mul_poly(n[3], m[3]))[0]
            ]

    return res




def zk(m):
    m = chop(m)
    zk_m = []
    for i in range(0, len(m), 4):
        zk_m.append(m[i])
        zk_m.append(m[i+1])
        zk_m.append(m[i+3])
        zk_m.append(m[i+2])
    return zk_m

def sbox(x, m):
    if x == "E":
        box = {
        '0000' : '1110',
        '0001' : '0100',
        '0010' : '1101',
        '0011' : '0001',
        '0100' : '0010',
        '0101' : '1111',
        '0110' : '1011',
        '0111' : '1000',
        '1000' : '0011',
        '1001' : '1010',
        '1010' : '0110',
        '1011' : '1100',
        '1100' : '0101',
        '1101' : '1001',
        '1110' : '0000',
        '1111' : '0111',
        }

    if x == "D":
        box = {
        '0000' : '1110',
        '0001' : '0011',
        '0010' : '0100',
        '0011' : '1000',
        '0100' : '0001',
        '0101' : '1100',
        '0110' : '1010',
        '0111' : '1111',
        '1000' : '0111',
        '1001' : '1101',
        '1010' : '1001',
        '1011' : '0110',
        '1100' : '1011',
        '1101' : '0010',
        '1110' : '0000',
        '1111' : '0101',
        }

    m = chop(m)
    new = []
    for i in range(len(m)):
        new.append(box[m[i]])
    return new

def generate_keys(k):
    frk = []
    k = chop(k)
    frk.append(add_mod2(add_mod2(k[0], sbox("E", k[3])), "0001"))
    onezero = add_mod2(k[2], frk[0][0])
    frk.append(add_mod2(k[1], onezero))
    frk.append(onezero)
    frk.append(add_mod2(k[3], frk[1]))
    frk = [i[0] for i in frk]

    srk = []
    srk.append(add_mod2(add_mod2(frk[0], sbox("E", frk[3])), "0010"))
    onezero = add_mod2(frk[2], srk[0][0])
    srk.append(add_mod2(frk[1], onezero))
    srk.append(onezero)
    srk.append(add_mod2(frk[3], srk[1]))
    srk = [i[0] for i in srk]

    return frk,srk

def cipher(t, kp):
    m = '0011001000100011'
    frk, srk = generate_keys(kp)
    frk = ''.join(frk)
    print("First round key: ", frk)
    srk = ''.join(srk)
    print("Second round key: ", srk)
    t = add_mod2(t, kp)[0]
    t = sbox("E", t)
    t = ''.join(t)
    t = zk(t)
    t = ''.join(t)
    t = matr_mul(m,t)
    t = ''.join(t)
    t = add_mod2(t, frk)[0]
    t = sbox("E", t)
    t = ''.join(t)
    t = zk(t)
    t = ''.join(t)
    t = add_mod2(t, srk)[0]

    return t

def decipher(s, kp):
    m = '0011001000100011'
    frk, srk = generate_keys(kp)
    frk = ''.join(frk)
    srk = ''.join(srk)
    s = add_mod2(s, srk)[0]
    s = zk(s)
    s = ''.join(s)
    s = sbox("D", s)
    s = ''.join(s)
    s = add_mod2(s, frk)[0]
    s = matr_mul(m, s)
    s = ''.join(s)
    s = zk(s)
    s = ''.join(s)
    s = sbox("D", s)
    s = ''.join(s)
    s = add_mod2(s, kp)[0]

    return s

def first_ex():
    a = input("Input your first hexadecimal four-bit expression: ")
    a = get_message(a, 4)

    b = input("Input your second hexadecimal four-bit expression: ")
    b = get_message(b, 4)

    c = mul_poly(a,b)
    print("{} (*) {} == {}".format(a[0],b[0],c))

    sboxE = sbox("E", c)
    print("SBoxE({}) == {}".format(c, sboxE))

    sboxD = sbox("D", c)
    print("SBoxD({}) == {}".format(c, sboxD))

def second_ex():
    t = input("Input your text: ")
    t = get_message16(t)

    text = []
    for i in range(0, len(t), 16):
        text.append(t[i:i+16])

    k = input("Input your key: ")
    k = get_messagek(k)

    print("Your message: ", t)
    print("Your key: ", k)
    all_ciphered_bin = []
    all_ciphered_hex = []
    print(len(text))
    for i in text:
        all_ciphered_bin.append(cipher(i, k))
        all_ciphered_hex.append(hex(int(all_ciphered_bin[-1], 2)))

    print("Ciphered text: ", all_ciphered_hex)
    #print(all_ciphered_hex)

    #all_deciphered_bin = []
    #all_deciphered_hex = []

    #for i in all_ciphered_bin:
        #all_deciphered_bin.append(cipher(i, k))

    #print(all_deciphered_bin)
    #for i in all_deciphered_bin:
        #all_deciphered_hex.append(hex(int(i, 2)))

    #print("Deciphered text: ", all_deciphered_hex)
while True:
    second_ex()
