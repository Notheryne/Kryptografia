import six


f  = open("tekst.txt")
data = f.readlines()
f.close()


st = ""
for i in range(len(data[0])):
    st+= data[0][i]
s = st.strip('\n')



key = input("Define a key to cipher with: ")


translated = ""
for i in range(len(s)):
    if s[i].isalpha():
        
        if s[i].islower():
            x = ord(s[i]) - 97
            y = ord(key[i%len(key)]) - 97
            n = (x+y)%26
            translated += chr(n+97) 
    else:
        translated += s[i]


type(translated)
translated


f = open("tekst2.txt", "w")
f.write(translated)
f.close()

f  = open("tekst2.txt")
data = f.readlines()
f.close()

coded_text = data[0]

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def check_key(l, n):
    x = list(l)
    y = list(chunks(x, n))
    transy = [list(row) for row in six.moves.zip_longest(*y, fillvalue='-')]
    col_nums = []
    N = []
    for i in range(len(transy)):
        n1 = 0
        col = ''.join(transy[i])
        N.append(len(col))
        for j in range(26):
            letter = chr(97+j)
            n = col.count(letter)
            n1 += n*(n-1)
        col_nums.append(n1)
    this_I = []
    for i in range(len(col_nums)):
        this_I.append(col_nums[i]/(N[i]*(N[i]-1)))
    return this_I

english_I = 0.067

l = check_key(coded_text, 2)
print(l)

def find_key(l, n):
    co_index = []
    for i in range(1, n+1):
        co = check_key(l,i)
        co_index.append(co)
    for i in range(len(co_index)):
        x = sum(co_index[i])/len(co_index[i])
        if (x > english_I - 0.003) and (x < english_I + 0.003):
            print("Likely key length is: ", i+1)
            print("Column's coincidence indexes are: ", co_index[i])
        else:
            print("Supposed key length: ", i+1)
            print("Column's coincidence indexes are: ", co_index[i])

find_key(coded_text, 10)



