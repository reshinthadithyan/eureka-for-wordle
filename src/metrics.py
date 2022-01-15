from nltk import corpus,download
download('words')

def get_word_list()->list:

    return [ i for i in corpus.words.words() if len(i) == 5]



class Metrics:
    def __init__(self):
        self.score_dict = {
            "not_present" : 0,
            "wrong_pos" : 1,
            "right" : 2
        }
        self.word_list = get_word_list()

    def check_word(self,ref_word:str)->bool:
        """
        Returns True/False based on it's presence.
        """
        return ref_word in self.word_list
    
    def __call__(self,ref_word:str,pred_word:str)->dict:
        """
        Returns the position level score based on the comparison
        """
        score_dict = {}

        for letter_idx in range(5):
            pred_letter = pred_word[letter_idx]
            if pred_letter == ref_word[letter_idx]:
                score_dict[pred_letter] = 2
            elif pred_letter in ref_word:
                score_dict[pred_letter] = 1
            else:
                score_dict[pred_letter] = 0

        return score_dict

if __name__ == "__main__":
    print(len(get_word_list()))
    metric = Metrics()
    print(metric("apple","aplep"))