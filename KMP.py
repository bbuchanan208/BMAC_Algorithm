class KMP:

    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.attempts = 1
        self.comparisons = 0
        self.pattern_length = len(self.pattern)
        self.text_length = len(self.text)
        self.lps = [0] * self.pattern_length
        self.computeLPSArray()
        self.results_array = []

    def return_results(self):
        return "KMP Results: \n" + "Attempts: " + str(self.attempts) + "\n" + "Comparisons: " + str(self.comparisons)

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

    # Python program for KMP Algorithm
    def KMPSearch(self):

        # create lps[] that will hold the longest prefix suffix
        # values for pattern
        j = 0  # index for pat[]

        i = 0  # index for txt[]
        while i < self.text_length:
            if j == 0:
                self.attempts += 1
            if self.pattern[j] == self.text[i]:
                self.comparisons += 1
                i += 1
                j += 1

            if j == self.pattern_length:
#                print("Found pattern at index " + str(i - j))
                self.results_array.append(i-j)
                j = self.lps[j - 1]

                # mismatch after j matches
            elif i < self.text_length and self.pattern[j] != self.text[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
            self.comparisons += 1
        print(self.return_results())



'''
ttxt = "abcxabcdabxabcdabcdabcy"
ppat = "abcdabcy"
test = KMP("AAAAAA", 'AAA')
print(test.lps)
'''


# This code is contributed by Bhavya Jain