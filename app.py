import streamlit as st
import pandas as pd
from src.game import Wordle


st.title("WORDLE")


with st.form("Wordle"):
    button = st.form_submit_button("Play")
    box = st.selectbox("Select the trial level :",["6","100"])
    if button:
        wordle = Wordle(int(box))
        chosen_word,game_diction = wordle.play()
        st.dataframe(pd.DataFrame.from_dict(game_diction))
        st.write(f"The actual word is : {wordle.wordle}")
        st.write(f"It took {len(game_diction['step_no'])} random search steps to find it")