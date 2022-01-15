import random
from src.metrics import get_word_list


class Cerebrum:
    def __init__(self,vowel_knowledge:int=2) -> None:
        self.word_list = get_word_list()
        self.init_word_list = self.get_vowelled_word_list(vowel_knowledge)
    
    def get_vowelled_word_list(self,nos_vowels:int)->list:
        """
        Returns a list of words with the given number of vowels.
        """
        vowels = set(["a","e","i","o","u"])
        tmp_list = []
        for word in self.word_list:
            ind_word_set = set(list(word))
            if len(list(vowels.intersection(ind_word_set))) > nos_vowels:
                tmp_list.append(word)
        return tmp_list

    def random_first_choice(self)->str:
        return random.choice(self.init_word_list)

    def random_n_choice(self,hash_output:list[list])->str:
        if len(hash_output) == 1:
            return random.choice(hash_output[0])
        else:
            sub_hash = random.choice(hash_output)
            return random.choice(sub_hash)

if __name__ == "__main__":
    cerebrum = Cerebrum()
    print(len(cerebrum.init_word_list))