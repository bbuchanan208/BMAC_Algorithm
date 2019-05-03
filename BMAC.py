from preProcessing import *

class MACV2:


    def __init__(self, text, pattern):
        self.attempts = 0
        self.comparisons = 0
        self.text = text
        self.text_len = len(text)
        self.pattern_length = len(pattern)
        self.pattern = pattern
        self.BrBc = build_bad_char_table(pattern)
        self.IbSv = build_IbSv_table(text, pattern)
        self.alphabetDict = {"A": 0, "C": 1, "G": 2, "T": 3}
        self.IbSv_constant = "IbSv"
        self.BrBc_constant = "BrBc"
        self.KMP_constant = "KMP"
        self.index_search_limit = len(text) - len(pattern) #this will
        self.results_array = []
        self.lps = [0] * self.pattern_length
        self.computeLPSArray()
        self.text_pointer = 0
        self.pattern_pointer = 0
        self.IbSvPointer = 0
        self.debug = True
        self.temp_text_pointer = 0



    def returnString(self):
        return "BuchMAC Results: \n" + "Attempts: " + str(self.attempts) + "\n" + "Comparisons: " + str(self.comparisons)

    def computeLPSArray(self):
        len_of_prev_longest_sufix = 0  # length of the previous longest prefix suffix
        i = 1

        # the loop calculates lps[i] for i = 1 to M-1
        while i < self.pattern_length:
            if self.pattern[i] == self.pattern[len_of_prev_longest_sufix]:
                len_of_prev_longest_sufix += 1
                self.lps[i] = len_of_prev_longest_sufix
                i += 1
            else:
                # This is tricky. Consider the example.
                # AAACAAAA and i = 7. The idea is similar
                # to search step.
                if len_of_prev_longest_sufix != 0:
                    len_of_prev_longest_sufix = self.lps[len_of_prev_longest_sufix - 1]

                    # Also, note that we do not increment i here
                else:
                    self.lps[i] = 0
                    i += 1

    def search(self):
        if len(self.IbSv) == 0:
            print("No instances of the pattern exist in the text")
        else:
            self.text_pointer = self.IbSv[0]
            self.pattern_pointer = 1
        if self.debug:
            print("text_pointer=" + str(self.text_pointer))
            print("Index_search_limit =" + str(self.index_search_limit))
        while self.text_pointer <= self.index_search_limit:

            # do a comparison
            self.KMPComparision()

            # if the comparison succeeds
            mac_jump_loc = self.get_jump_location_using_MAC()
            if mac_jump_loc == 0:
                if self.debug: print("BrBc is no longer valid:")
                KMP_jump_loc = self.calc_text_ptr_if_KMP_jump()
                if KMP_jump_loc == self.IbSv[-1]:
                    self.text_pointer = KMP_jump_loc
                    self.KMPComparision()
                break
            KMP_jump_loc = self.calc_text_ptr_if_KMP_jump()
            self.choose_best_jump_method(mac_jump_loc, KMP_jump_loc)
            if self.debug: print("")
        print(self.returnString())

    def KMPComparision(self):

        self.temp_text_pointer = self.text_pointer
        self.attempts += 1
        additional_index = self.pattern_pointer
        #        while self.temp_text_pointer < self.text_len:
        while additional_index < self.pattern_length:
            self.comparisons += 1  # First comparision below
            if self.pattern[self.pattern_pointer] == self.text[self.temp_text_pointer + additional_index]:
                self.pattern_pointer += 1
                additional_index += 1
                if additional_index == self.pattern_length:
                    # The entire pattern has been matched, we add the original text pointer to the results array
                    self.results_array.append(self.text_pointer)
                    if self.debug: print("Pattern found at: " + str(self.text_pointer))
                    self.pattern_pointer = self.lps[self.pattern_pointer - 1]
                    self.temp_text_pointer += additional_index
                    break

            else:
                # The pattern has not matched and we need to calculate the best place to restart the search
                if self.debug: print("No match when starting at index:" + str(self.text_pointer))
                if self.pattern_pointer != 0:
                    self.pattern_pointer = self.lps[self.pattern_pointer - 1]
                    self.temp_text_pointer = self.text_pointer + additional_index
                    break
                else:
                    self.temp_text_pointer += additional_index + 1
                    break

    def choose_best_jump_method(self, MAC_jump_location, KMP_jump_location):
        if self.debug:
            print("MAC: j=" + str(MAC_jump_location) + "   jt=" + str(MAC_jump_location + 1))
            print("KMP: j=" + str(KMP_jump_location) + "   jt=" + str(KMP_jump_location + self.pattern_pointer))
        MAC_first_comparison = MAC_jump_location + 1
        if self.temp_text_pointer > MAC_first_comparison:
            self.text_pointer = KMP_jump_location
            if self.debug:
                print("KMP is chosen")
        else:
            self.text_pointer = MAC_first_comparison - 1
            self.pattern_pointer = 1
            if self.debug:
                print("MAC was chosen")

    def jump_location_of_kmp(self):
        '''
        This function uses the temporary pointer to calculate the location that KMP would jump the text pointer to
        IE: this is the start (0th index) of the search window
        :return:
        '''
        return self.temp_text_pointer - self.pattern_pointer

    def start_location_of_kmp(self):
        return self.temp_text_pointer

    def getJumpLocUsingBrBc(self):
        return_index = self.text_pointer
        if self.text_pointer <= self.index_search_limit - 2:
            first_char_right_of_search_window = self.text_pointer + self.pattern_length
            sec_char_right_of_search_window = self.text_pointer + self.pattern_length + 1
            if self.debug:
                print("BrBC Char 1: " + str(self.text[first_char_right_of_search_window]))
                print("BrBC Char 2: " + str(self.text[sec_char_right_of_search_window]))
            first_char_right_of_search_window = self.alphabetDict[self.text[first_char_right_of_search_window]]
            sec_char_right_of_search_window = self.alphabetDict[self.text[sec_char_right_of_search_window]]
            return_index += self.BrBc[first_char_right_of_search_window][sec_char_right_of_search_window]
            if self.debug : print("BrBc return index: " + str(return_index))
            if return_index >= self.text_len:
                print("END SEARCH")
            return return_index
        else:
            if self.debug: print("BrBc return index: " + str(0))
            return 0

    def getJumpLocUsingIbSv(self, BrBc_starting_index):

        self.IbSvPointer += 1
        while self.IbSvPointer < len(self.IbSv):
            if self.IbSv[self.IbSvPointer] >= BrBc_starting_index:
                if self.debug: print("IbSvPointer: " + str(self.IbSvPointer))
                return self.IbSv[self.IbSvPointer]
            else:
                self.IbSvPointer += 1
        if self.debug: print("There are no more occurances of the pattern")
        return 0

    def get_jump_location_using_MAC(self):
        '''
        :return: The start index of the text pointer.
        NOTE: The first comparision starts one after this
        '''
        BrBc_index = self.getJumpLocUsingBrBc()
        return self.getJumpLocUsingIbSv(BrBc_index)

    def max_mac(self):
        pass

    def calc_text_ptr_if_KMP_jump(self):
        return self.temp_text_pointer - self.pattern_pointer

        pass

    def silly_test(self):
        i = 0
        while i <1000:
            print(i)
            if i == 10:
                break
            i +=1
        print("It broke")
