import streamlit as st
from main import chain
import pandas as pd
from pprint import pprint


def get_stories(
        song_title: str, 
        lyrics: str,
        prompt: str
        ) -> pd.DataFrame:

    stories = chain.invoke(
        {
            "song_title": song_title,
            "lyrics": lyrics,
            "prompt": prompt
        }
    )

    pprint(stories)
    print("-----------------------------------------------------------")
    print(type(stories.stories))
    print("-----------------------------------------------------------")

    # for story in stories:
    #     print("-----------------------------------------------------------")
    #     print(type(story))
    #     print("-----------------------------------------------------------")
    #     print(type(story[0]))
    #     print("-----------------------------------------------------------")
    #     print(len(story))
    #     print("-----------------------------------------------------------")
    #     print(story)

    df = pd.DataFrame([story.model_dump() for story in stories.stories])

    # st.dataframe(df)

    return df 
        


st.title("Story Generator for Songs")
song_title = st.text_area(
    label="Song Title",
    placeholder="Enter the title of your song.",
    height=68
    )
lyrics = st.text_area(
    label="Lyrics",
    placeholder="Enter the lyrics of the song here",
    height=200
    )
prompt = st.text_area(
    label="Prompt (Optional)",
    placeholder="Any Special Instructions on what the story and the Images Prompts should be focussed on? (Optional)",
    height=100
    )

if not prompt:
    prompt = "No Special Instruction given, generate accordingly."

if st.button(label="Generate"):
    df = get_stories(song_title, lyrics, prompt)

    st.dataframe(df, hide_index=True)



