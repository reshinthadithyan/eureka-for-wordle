from itertools import count
from src.metrics import get_word_list,Metrics
import logging
import random
from src.utils import WordHash
from src.agent import Cerebrum


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





class Wordle:
    def __init__(self,steps_to_be_tried=6) -> None:
        self.steps = steps_to_be_tried
        self.word_list = get_word_list()
        self.letter_list = list("abcdefghijklmnopqrstuvwxyz")
        self.wordle = random.choice(self.word_list)
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
        game_diction = {"step_no":[],"chosen_word":[],"status":[]}
        for step in range(self.steps):
            logger.info(f"Step {step}")
            if step == 0:
                chosen =  self.sixth_sense.random_first_choice()
                logger.info(f"Chosen word is {chosen}")
                pos_score_dict = self.single_step(chosen)
                slice_pos_list = self.hash.slice_pos(self.preprocess_pos_word(pos_score_dict))
                game_diction["chosen_word"].append(chosen)
                game_diction["step_no"].append(step)
                game_diction["status"].append("CONTINUE")
            else:

                chosen = self.sixth_sense.random_n_choice(slice_pos_list)
                logger.info(f"Chosen word is {chosen}")
                pos_score_dict = self.single_step(chosen)
                slice_pos_list = self.hash.slice_pos(self.preprocess_pos_word(pos_score_dict))
                game_diction["chosen_word"].append(chosen)
                game_diction["step_no"].append(step)
                if chosen != self.wordle:
                    game_diction["status"].append("CONTINUE")
                elif chosen == self.wordle:
                    game_diction["status"].append("IMPRESSIVE")
                    logger.info(f"The word is {chosen}")
                    break
        return chosen,game_diction





if __name__ == "__main__":
    pass
    # pos_score_dict = wordle_module.single_step("cants")
    # print(pos_score_dict)
    # slice_pos_list = wordle_module.preprocess_pos_word(pos_score_dict)
    # print(slice_pos_list)
    # hash = WordHash()
    # print(hash.slice_pos(slice_pos_list))
