from itertools import count
from metrics import get_word_list,Metrics
import logging
import random
from utils import WordHash
from agent import Cerebrum


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)






class Wordle:
    def __init__(self) -> None:
        self.steps = 100
        self.word_list = get_word_list()
        self.letter_list = list("abcdefghijklmnopqrstuvwxyz")
        self.wordle = "panic"#DEBUG(reshinth) random.choice(self.word_list)
        self.sixth_sense = Cerebrum()
        self.hash = WordHash()
        logger.info(f"The Word to be found is {self.wordle}")
        self.evaluator = Metrics()

    def deduct_vocab(self,score_dict:dict):
        """
        Returns True if the word is present in the vocab.
        """
        for letter in score_dict:
            if score_dict[letter] == 0:
                if letter in self.letter_list:
                    del self.letter_list[self.letter_list.index(letter)]

    def preprocess_pos_word(self,pos_score_dict:dict):
        """
        Flag : G -> Sure, Y -> Probable
        """
        pos_slice_list_g = []
        pos_slice_list_y = []
        for ind in range(len(pos_score_dict)):
            letter = list(pos_score_dict.keys())[ind]
            score = pos_score_dict[letter]
            if score == 2:
                pos_slice_list_g.append([ind,letter,"G"])
            if score == 1:
                for possible_index in range(5):
                    if possible_index != ind:
                        pos_slice_list_y.append([possible_index,letter,"Y"])

        return pos_slice_list_g + pos_slice_list_y

    def single_step(self,pred_word:str):
        pos_score_dict = self.evaluator(self.wordle,pred_word)
        self.deduct_vocab(pos_score_dict)

        return pos_score_dict

    def play(self)->str:
        for step in range(self.steps):
            logger.info(f"Step {step}")
            if step == 0:
                chosen =  self.sixth_sense.random_first_choice()
                logger.info(f"Chosen word is {chosen}")
                pos_score_dict = self.single_step(chosen)
                slice_pos_list = self.hash.slice_pos(wordle_module.preprocess_pos_word(pos_score_dict))
            else:

                chosen = self.sixth_sense.random_n_choice(slice_pos_list)
                logger.info(f"Chosen word is {chosen}")
                pos_score_dict = self.single_step(chosen)
                slice_pos_list = self.hash.slice_pos(wordle_module.preprocess_pos_word(pos_score_dict))
                if chosen == self.wordle:
                    break
                    logger.info(f"The word is {chosen}")
        return chosen





if __name__ == "__main__":
    wordle_module = Wordle()
    # pos_score_dict = wordle_module.single_step("cants")
    # print(pos_score_dict)
    # slice_pos_list = wordle_module.preprocess_pos_word(pos_score_dict)
    # print(slice_pos_list)
    # hash = WordHash()
    # print(hash.slice_pos(slice_pos_list))
    print(wordle_module.play())