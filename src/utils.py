from itertools import count
from metrics import get_word_list,Metrics

import logging
import random
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class WordHash:
    def __init__(self) -> None:
        self.word_list = get_word_list()
    
    def slice_pos(self,pos_letter_pair_list:list)->list:
        counter = 0
        tmp = []
        for pos_letter_pair in pos_letter_pair_list:
            print(pos_letter_pair)
            pos,letter,flag = pos_letter_pair[0],pos_letter_pair[1],pos_letter_pair[2]
            if counter == 0:
                for word in self.word_list:
                    if word[pos] == letter:
                        tmp.append(word)
            else:
                tmp = [word for word in tmp if word[pos] == letter]
            counter = counter + 1
        return tmp
        


class Wordle:
    def __init__(self) -> None:
        self.steps = 6
        self.word_list = get_word_list()
        self.letter_list = list("abcdefghijklmnopqrstuvwxyz")
        self.wordle = "panic"#DEBUG(reshinth) random.choice(self.word_list)
        logger.info(f"The selected Word is {self.wordle}")
        self.evaluator = Metrics()

    def deduct_vocab(self,score_dict:dict):
        """
        Returns True if the word is present in the vocab.
        """
        for letter in score_dict:
            if score_dict[letter] == 0:
                del self.letter_list[self.letter_list.index(letter)]
        logger.info(self.letter_list)

    def preprocess_pos_word(self,pos_score_dict:dict):
        """
        Flag : G -> Sure, Y -> Probable
        """
        pos_slice_list = []
        for ind in range(len(pos_score_dict)):
            letter = list(pos_score_dict.keys())[ind]
            score = pos_score_dict[letter]
            if score == 2:
                pos_slice_list.append([ind,letter,"G"])
            if score == 1:
                for possible_index in range(5):
                    if possible_index != ind:
                        pos_slice_list.append([possible_index,letter,"Y"])

        return pos_slice_list
    def single_step(self,pred_word:str):
        pos_score_dict = self.evaluator(self.wordle,pred_word)
        #Fresh Vocabulary
        self.deduct_vocab(pos_score_dict)

        return pos_score_dict
    

if __name__ == "__main__":
    wordle_module = Wordle()
    pos_score_dict = wordle_module.single_step("cants")
    print(pos_score_dict)
    slice_pos_list = wordle_module.preprocess_pos_word(pos_score_dict)
    print(slice_pos_list)
    hash = WordHash()
    print(hash.slice_pos(slice_pos_list))