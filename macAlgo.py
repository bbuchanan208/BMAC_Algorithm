from preProcessing import *

class macAlgorithm:

    def __init__(self, text, pattern):
        self.attempts = 0
        self.comparisons = 0
        self.text = text
        self.text_len = len(text)
        self.pattern = pattern
        self.BrBc = build_bad_char_table(pattern)
        self.IbSv = build_IbSv_table(text, pattern)
        self.alphabetDict = {"A": 0, "C": 1, "G": 2, "T": 3}
        self.IbSv_constant = "IbSv"
        self.BrBc_constant = "BrBc"
        self.index_search_limit = len(text) - len(pattern) #this will
        self.results_array = []

    def iShouldTerminateSearch(self, j):
        if j > self.IbSv[-1]:
            return True
        return False

    def getMaxShiftValue(self, char1, char2, i, j):
        if char1 != -1:
            brBc_value = self.BrBc[self.alphabetDict[char1]][self.alphabetDict[char2]]
        else:
            brBc_value = 1
        if i >= len(self.IbSv):
            IbSv_value = 0
        else:
            IbSv_value = self.IbSv[i] - j
        if IbSv_value >= brBc_value:
            return (IbSv_value, self.IbSv_constant)
        return (brBc_value, self.BrBc_constant)

    def inefficentCompare(self, start_index, max_found_using):
        #  print("Starting index: " + str(start_index))
        if start_index > self.index_search_limit:
            return
        self.attempts += 1
        comparision_offset = 2
        new_index = start_index

        # First comparision only happens if we used the BrBc table
        if max_found_using == self.BrBc_constant:
            self.comparisons += 1
            if self.pattern[0] != self.text[start_index]:
                return
        new_index += 1

        # The second comparison
        self.comparisons += 1
        if self.pattern[1] != self.text[new_index]:
            return
        new_index += 1

        # The third comparision
        self.comparisons += 1
        if self.pattern[-1] != self.text[start_index + len(self.pattern) - 1]:
            return

        while comparision_offset < len(self.pattern):
            self.comparisons += 1
            if self.text[start_index + comparision_offset] != self.pattern[comparision_offset]:
                return
            comparision_offset += 1
        self.results_array.append(start_index)
#        print("Pattern found at " + str(start_index))
        return

    def shiftIbSv(self, i, j):
        #if i >= len(self.IbSv):
        #    return -1
        while i < len(self.IbSv):
            if not self.iNeedsToBeShifted(i, j):
                return i
            else:
                i += 1
        return i

    def iNeedsToBeShifted(self, i, j):
        return self.IbSv[i] < j

    def returnString(self):
        return "Original MAC Results: \n" + "Attempts: " + str(self.attempts) + "\n" + "Comparisons: " + str(self.comparisons)

    def start_pattern_search(self):
        # If the IbSv has nothing in it, there the pattern cannot occur.
        if len(self.IbSv) <= 0:
            print(self.returnString())
            return
#        self.patternSearch(i=1, j=self.IbSv[0])
        self.patternSearch(i=0, j=0)

    def patternSearch(self, i=0, j=0):
        while j <= self.index_search_limit:
            #print("J value: " + str(j))
            self.inefficentCompare(j, self.BrBc_constant)
            if j + len(self.pattern) > self.text_len - 2:
                first_char_one_right_of_search_window = -1
                second_char_two_right_of_search_window = -1
            else:
                first_char_one_right_of_search_window = self.text[j + len(self.pattern)]
                second_char_two_right_of_search_window = self.text[j + len(self.pattern) + 1]
            shift_value_and_type = self.getMaxShiftValue(first_char_one_right_of_search_window,
                                                         second_char_two_right_of_search_window, i, j)
            j += shift_value_and_type[0]
            i += 1
            i = self.shiftIbSv(i, j)
            if i == -1:
                print(self.returnString())
                return
        print(self.returnString())

