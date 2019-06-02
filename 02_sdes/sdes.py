def get_message(mess):
    l_hex = mess.split(" ")
    for i in range(len(l_hex)):
        if len(l_hex[i]) == 1:
            l_hex[i] += "0"
    try:
        l_dec = [int(i, 16) for i in l_hex]
        l_bin = [str(bin(i))[2:] for i in l_dec]
        l_bin_8 = [b.zfill(8) for b in l_bin]
        assert all(len(b) == 8 for b in l_bin_8)
        return l_bin_8

    except ValueError:
        print("You did not enter a hexadecimal number!")

def perm(m, p):
    if isinstance(m, list):
        l_perm = []
        for i in m:
            new_str = ""
            for j in range(len(i)):
                new_str += i[p[j]]
            l_perm.append(new_str)
        return l_perm

    if isinstance(m, str):
        new_str = ""
        for i in range(len(p)):
            new_str += m[p[i]]
        return new_str

permutations = {"pw" : (1,5,2,0,3,7,4,6),
                "p10" : (2,4,1,6,3,9,0,8,7,5),
                "p_cross" : (4,5,6,7,0,1,2,3),
                "po" : (3,0,2,4,6,1,7,5),
                "sl1" : (1,2,3,4,0),
                "p10w8" : (5,2,6,3,7,4,9,8),
                "sl2" : (2,3,4,0,1),
                "p4w8" : (3,0,1,2,1,2,3,0),
                "p4" : (1,3,2,0)
                }

def generate_keys(k_p):
    k_p10 = perm(k_p, permutations["p10"])
    k_00 = k_p10[:5]
    k_11 = k_p10[5:]

    k_00 = perm(k_00, permutations["sl1"])
    k_11 = perm(k_11, permutations["sl1"])

    first_round_key = perm(k_00+k_11, permutations["p10w8"])

    k_00 = perm(k_00, permutations["sl2"])
    k_11 = perm(k_11, permutations["sl2"])

    second_round_key = perm(k_00+k_11, permutations["p10w8"])
    return first_round_key, second_round_key

def add_mod2(l, k):
    if isinstance(l, str):
        l = [l]
    if isinstance(k, str):
        k = [k]
    res = []

    for i in range(len(l)):
        for j in range(len(k)):
            s = ""
            for c in range(len(k[j])):
                s += str((int(l[i][c]) + int(k[j][c]))%2)
        res.append(s)
    return res

def sbox(t, n):
    if n == 1:
        SB = [[1,0,3,2],
            [3,2,1,0],
            [0,2,1,3],
            [3,1,3,2]]
    if n == 2:
        SB = [[0,1,2,3],
            [2,0,1,3],
            [3,0,1,0],
            [2,1,0,3]]
    if isinstance(t, str):
        m = [t]
    else:
        m = t

    res = []

    for i in m:
        f_l = i[0] + i[3]
        mid = i[1] + i[2]
        j = int(f_l, 2)
        c = int(mid, 2)

        if SB[j][c] == 0:
            s = "00"
        elif SB[j][c] == 1:
            s = "01"
        elif SB[j][c] == 2:
            s = "10"
        elif SB[j][c] == 3:
            s = "11"
        res.append(s)
    return res

def key_cipher(m, k_p, round, cord = None):
    rounds = {"first" : 0, "second" : 1, 1 : 0, 2 : 1}

    keys = generate_keys(k_p)
    if isinstance(m, str):
        m = [m]

    l_first = [i[:4] for i in m]
    l_second = [i[4:] for i in m]
    l_copy = [i[4:] for i in m]
    ls_p4w8 = []
    for i in l_second:
        ls_p4w8.append(perm(i, permutations["p4w8"]))
    xor = add_mod2(ls_p4w8, keys[rounds[round]])

    sb1 = [i[:4] for i in xor]
    sb2 = [i[4:] for i in xor]

    sb1 = sbox(sb1, 1)
    sb2 = sbox(sb2, 2)

    sb = [sb1[i] + sb2[i] for i in range(len(sb1))]
    sb = [perm(i, permutations["p4"]) for i in sb]
    sb = add_mod2(l_first, sb)

    sb = [sb[i] + l_copy[i] for i in range(len(sb))]
    if cord == "c":
        if round == "first" or round == 1:
            print("After first key: ", hex(int(sb[0], 2)))
        else:
            print("After second key: ", hex(int(sb[0], 2)))
    return sb

def cipher(txt, res):
    k_p = ("1100000011")
    res_hex = []
    res_bin = []
    for m in txt:
        m = perm(m, permutations["pw"])
        m = key_cipher(m, k_p, "first", "c")
        m = perm(m, permutations["p_cross"])
        m = key_cipher(m, k_p, "second", "c")
        m = perm(m, permutations["po"])
        for i in m:
            res_hex.append(hex(int(i, 2))[2:])
            res_bin.append(i)
    if res == "bin":
        return res_bin
    if res == "hex":
        for i in range(len(res_hex)):
            if len(res_hex[i]) == 1:
                res_hex[i] = "0" + res_hex[i]
        return ' '.join(res_hex)

def decipher(txt):
    k_p = ("1100000011")
    res = []
    for m in txt:
        m = perm(m, permutations["pw"])
        m = key_cipher(m, k_p, "second")
        m = perm(m, permutations["p_cross"])
        m = key_cipher(m, k_p, "first")
        m = perm(m, permutations["po"])
        for i in m:
            res.append(hex(int(i, 2))[2:])
    return ' '.join(res)

while(True):
    k_p = ("1100000011")
    keys = generate_keys(k_p)
    mess = input("Input your hexadecimal text: ")
    print("First round key: ", keys[0])
    print("Second round key: ", keys[1])
    m = get_message(mess)
    print("Your text, ciphered:   ", cipher(m, "hex"), '\n\n')
    print("Your text, deciphered: ",decipher(cipher(m,"bin")), '\n\n')
