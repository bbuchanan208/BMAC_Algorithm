from suffix_trees import STree


def build_bad_char_table(pattern, alphabet="ACGT"):
    return_list = []
    m = len(alphabet)
    for i in range(m):
        return_list.append([-1] * m)
    for i in range(m):
        for j in range(m):
            return_list[i][j] = helper(alphabet[i], alphabet[j], pattern)
    return return_list



def helper(a,b, pattern):
    m = len(pattern)
    listy = []
    if pattern[m-1] == a:
        listy.append(1)
    for i in range(m + 1):
        try:
            if pattern[i] == a and pattern[i + 1] == b:
                listy.append(m-i)
        except:
            pass
    if pattern[0] == b:
        listy.append(m + 1)
    else:
        listy.append(m+2)
    return min(listy)

def build_index_table(text, alphabet="ACGT"):
    myDict = {}
    for e in alphabet:
        myDict[e] = []
    i = 0
    while i < len(text):
        letter = text[i]
        myDict[letter].append(i)
        i += 1
    return myDict

def build_IbSv_table(text, pattern):
    return_table = []
    top_limit = len(text) - len(pattern)
    index_table = build_index_table(text)
    list_of_interest = index_table[pattern[0]]
    for e in list_of_interest:
        if e <= top_limit:
            return_table.append(e)
    return return_table

def better_index_table(text, pattern, alphabet="ACGT"):
    top_limit = len(text) - len(pattern)
    r_list = []
    i = 0
    while i < top_limit:
        if text[i] == pattern[0] and text[i + len(pattern) - 1] == pattern[len(pattern) - 1]:
            r_list.append(i)
        i += 1
    return r_list

txt = "ATCTAACATCATAACCCTAATTGGCAGAGAGAGAATCAATCGAATCA"
p = "GCAGAGAG"


#print(build_IbSv_table(txt, p))
#print(better_index_table(txt, p))
#st = STree.STree(p)
#print(st.find_all("AG"))