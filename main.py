import time
import random
from KMP import KMP
from macAlgo import macAlgorithm
from macV2 import MACV2
import matplotlib.pyplot as plt

FILE_STRING_PATH = "dna.50MB"

def get_text_from_file(file_in):
    with open(file_in, 'r') as file:
        data = file.read().replace('\n', '')
    return_string = ""
    for e in data:
        if e in ["A", "C", "G", "T"]:
            return_string += e
    return return_string

def pattern_generator(length_of_pat):
    numDict = {0: "A", 1: "C", 2: "G", 3: "T"}
    number_list = []
    char_string = ""
    for x in range(length_of_pat):
        number_list.append(random.randint(0, 3))
    for e in number_list:
        char_string += numDict[int(e)]
    return char_string

MAC_Comps = []
MAC_Attempts = []
MAC_both = []
MAC_time = []

BMAC_comps = []
BMAC_attempts = []
BMAC_both = []
BMAC_time = []


def perform_test_on_pattern(text, pattern):
    #kmp_instance = KMP(text, pattern)
    mac_instance = macAlgorithm(text, pattern)
    BMAC_instance = MACV2(text, pattern)
    BMAC_instance.debug = False

    '''
    time_start = time.time()
    #kmp_instance.KMPSearch()
    time_stop = time.time()
    print("KMP took " + str(round(time_stop - time_start, 10)) + " seconds")
    print("")
    '''

    time_start = time.time()
    mac_instance.start_pattern_search()
    time_stop = time.time()
    print("MAC took " + str(round(time_stop - time_start, 2)) + " seconds")
    print("")
    MAC_Comps.append(mac_instance.comparisons)
    MAC_Attempts.append(mac_instance.attempts)
    MAC_both.append(mac_instance.attempts + mac_instance.comparisons)
    MAC_time.append(round(time_stop - time_start, 2))

    time_start = time.time()
    BMAC_instance.search()
    time_stop = time.time()
    print("BMAC took " + str(round(time_stop - time_start, 10)) + " seconds")
    print("")
    BMAC_comps.append(BMAC_instance.comparisons)
    BMAC_attempts.append(BMAC_instance.attempts)
    BMAC_both.append(BMAC_instance.attempts + BMAC_instance.comparisons)
    BMAC_time.append(round(time_stop - time_start, 2))



    #if kmp_instance.results_array == mac_instance.results_array == BMAC_instance.results_array:
    if mac_instance.results_array == BMAC_instance.results_array:
        print("The results were the same")
        print("")
        print("")
    else:
        print("The pattern was: " + str(pattern))
#        kmp_results = kmp_instance.results_array
        mac_results = mac_instance.results_array
        b_mac_result = BMAC_instance.results_array
#        kmp_results.sort()
        mac_results.sort()
        b_mac_result.sort()
#        print("KMP results:")
#        print(kmp_results)
        print("MAC results:")
        print(mac_results)
        print("B_MAC results:")
        print(b_mac_result)
#        for e in mac_results:
#            print(text[e:e+10])
        print("The results were different")

def build_plot(pattern_length, Y_coords_MAC, Y_coords_BMAC, both=True):

    plt.plot(pattern_length, Y_coords_MAC, "g", label="MAC")
    plt.plot(pattern_length, Y_coords_BMAC, "c", label="BMAC")
    plt.xlabel("Pattern Length")
    plt.legend(loc="best")
    if both:
        plt.ylabel("Number of Attempts and comparisons")
        plt.title("Number of Attempts and Comparisons Using DNA Sequence")
        plt.savefig("total_number_comp_attempts.png", dpi=300)
    else:
        plt.ylabel("Time in seconds")
        plt.title("Time for the Matching Phase to Complete Using DNA Sequence")
        plt.savefig("time_needed.png", dpi=300)
    plt.clf()

pattern_length = [3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]


#text = get_text_from_file(FILE_STRING_PATH)
#pattern = pattern_generator(10)
perform_test_on_pattern("A" *1000000, "AAA")

'''
TESTCASE_1 = "AAAAAAAAAA"  # LENGTH OF 10
TESTCASE_5 = "AAAAACAAAACC"
TESTCASE_3 = "AAAAAAACAAAAAAA"
TESTCASE_4 = "CAAAAACAAAAAAAAAC"
TESTCASE_2 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" # LENGTH OF 100
testcases = [TESTCASE_1, TESTCASE_2, TESTCASE_3, TESTCASE_4, TESTCASE_5]
PATTERN = "AAA"
'''
# print(text[1:40])

'''

for e in pattern_length:
    pat = pattern_generator(e)
    perform_test_on_pattern(text, pat)

#build_plot(pattern_length, MAC_both, BMAC_both, both=True)
#build_plot(pattern_length, MAC_time, BMAC_time, both=False)
print("MAC COMP, ATTMPS")
print(MAC_Comps)
print(MAC_Attempts)
print(MAC_both)
print(MAC_time)

print("BMAC COMPS, ATTMPS")
print(BMAC_comps)
print(BMAC_attempts)
print(BMAC_both)
print(BMAC_time)
'''
