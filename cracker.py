import argparse
import hashlib

class Crack_pwd:
    
    def __init__(self, hashelist):
        print("Cracking the pwd now")
        self.hashes = self.get_hash(hashelist)

    
    def get_hash(self, hasheslist):
        hash_list = []
        file = open(hasheslist, 'r')
        for line in file:
            hash_list.append(line)
        print("size of the list of hashelist: " + str(len(hash_list)))
        return list(hash_list)

    def find_common_hash(self, wordlist):
        wordlist = list(wordlist)
        size = len(wordlist)
        print("The size of the wordlist is " + str(size))
        k = 0
        
        while (k < size):
            word = wordlist[k].replace('\n', '')
            sha = hashlib.sha1(word.encode())
            if (self.check_hash(str(sha.hexdigest()).upper()) == 1):
                print(word + "  is a password with sha: " + str(sha.hexdigest().upper()))
                self.add_result(word, str(sha.hexdigest()).upper())
            k = k + 1

    def check_hash(self, hash_to_test):
        hash_list = self.hashes

        for hashes in hash_list:
            if hashes.replace('\n', '').upper() == hash_to_test:
                print(str(hashes).replace('\n', '') + "is same as than :" + str(hash_to_test))
                return(1)
            else:
                #print(str(hashes) + "is different than :" + str(hash_to_test))
                return(0)

    def add_result(self, word, sha):
        f = open("resulkt", "a")
        f.write(word + "\t is corresponding to this sha: " + sha + "\n")
        f.close


    

class Pwd_dict:

    def __init__(self, wordlist, hasheslist):
        self.word_list = self.get_wordlist(wordlist)
        #words_collection = []
        size = len(self.word_list)
        pwd_cracker = Crack_pwd(hasheslist)
        #size = 327
        k = 0

        while k < size:
            print("Working on word: " + str(k) + " over " + str(size))
            tmp_words_collection = []
            tmp_words_collection += self.get_all_cases_possibilities(self.word_list[k])
            #tmp_words_collection += self.get_all_duo_combination(k)
            tmp_words_collection += self.add_year_and_symbols(tmp_words_collection)
            print("Trying to find the Hash -> ")
            pwd_cracker.find_common_hash(tmp_words_collection)
            k = k + 1
        
        print("done")

    def upload_dict(self, words_collection):
        f = open("new_dic.txt", "a")
        for word in words_collection:
            f.write(word)
        f.close
    
    def get_wordlist(self, wordlist):
        word_list = []
        file = open(wordlist, 'r')
        for line in file:
            word_list.append(line)
        print("size of the list of words: " + str(len(word_list)))
        return list(word_list)

    def add_year_and_symbols(self, word_collection):
        word_with_years_symbol = []

        sym = self.add_symbols(word_collection)
        print("1/4 done")
        year = self.add_years(word_collection)
        print("2/4 done")
       # year_over_sym = self.add_years(sym)
        print("3/4 done")
        #sym_over_year = self.add_symbols(year)
        print("4/4 done")

        word_with_years_symbol = sym + year #+ year_over_sym + sym_over_year
        return(word_with_years_symbol)


    def add_years(self, word_collection):
        word_with_years = []
        size = len(word_collection)
        k = 0

        while (k < size):
            year = 1990
            while (year <= 2000):
                right = word_collection[k].replace('\n', '') + str(year) + '\n'
                left = str(year) + word_collection[k].replace('\n', '') + '\n'
                word_with_years.append(right)
                word_with_years.append(left)
                year = year + 1
            k = k + 1
        return(word_with_years)

    def add_symbols(self, word_collection):
        symbols = "!@#$%?+-<>.)(*&"
        list_symbols = list(symbols)
        size_list_symbols = len(list_symbols)
        word_with_symbols = []
        size = len(word_collection)
        k = 0

        while (k < size):
            index = 0 
            while (index < size_list_symbols):
                right = word_collection[k].replace('\n', '') + list_symbols[index]
                left = list_symbols[index] + word_collection[k].replace('\n', '')
                other_index = 0
                word_with_symbols.append(right + '\n')
                word_with_symbols.append(left + '\n')
                while other_index < size_list_symbols:
                    right = list_symbols[other_index] + right
                    left = left + list_symbols[other_index]
                    word_with_symbols.append(right + '\n')
                    word_with_symbols.append(left + '\n')
                    other_index = other_index + 1
                index = index + 1
            k = k + 1
        return(word_with_symbols)
    
    def get_all_duo_combination(self, pos):
        res = []
        word_collection = []
        initial_word = self.word_list[pos]
        k = pos + 1
        size = len(self.word_list)
        #size = 327
        
        while k < size:
            left = self.word_list[k].replace('\n', '') + initial_word.replace('\n', '')
            left = left + '\n'
            right = initial_word.replace('\n', '') + self.word_list[k].replace('\n', '')
            right = right + '\n'
            word_collection.append(left)
            word_collection.append(right)
            k = k + 1
        
        #for word in word_collection:
            #res += self.get_all_cases_possibilities(word)
        return (word_collection)

    def get_all_cases_possibilities(self, word):
        word_as_list = list(word)
        derived_words = []
        size = len(word_as_list)
        pos = 0
        if (size > 12):
            size = 12
        derived_words.append(''.join(word_as_list))
        while pos < size:
            tmp_derived_words = derived_words[:]
            for words in tmp_derived_words:
                word_as_list = list(words)
                if (word_as_list[pos].isalpha() == True):
                    word_as_list[pos] = word_as_list[pos].upper()
                    derived_words.append(''.join(word_as_list))
            pos = pos + 1
        return derived_words
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crack a password list with a word_list.")
    parser.add_argument('wordlist', metavar="wordlist")
    parser.add_argument('pwdlist', metavar="pdwlist")
    args = parser.parse_args()
    cracked_dict = Pwd_dict(args.wordlist, args.pwdlist)