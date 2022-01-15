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
        tmp_super_list =  []
        for pos_letter_pair in pos_letter_pair_list:
            pos,letter,flag = pos_letter_pair[0],pos_letter_pair[1],pos_letter_pair[2]
            if flag == "G":
                if counter == 0:
                    for word in self.word_list:
                        if word[pos] == letter:
                            tmp.append(word)
                else:
                    tmp = [word for word in tmp if word[pos] == letter]
                counter = counter + 1
            else:
                tmp_super_list.append(tmp)
                if counter == 0:
                    for word in self.word_list:
                        if word[pos] == letter:
                            tmp_super_list[-1].append(word)
                else:
                     tmp_super_list[-1] = [word for word in  tmp_super_list[-1] if word[pos] == letter]
                counter = counter + 1   
        if len(tmp_super_list) != 0:
            return [ i for i in tmp_super_list if len(i) > 0]
        elif len(tmp) != 0 and len(tmp_super_list) == 0:                
            return [tmp]
        else:
            return [self.word_list]