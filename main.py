import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from pprint import pprint

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


class Story(BaseModel):
    story_count: int = Field(description="Sub Story Number")
    story: str = Field(description="Sub Story")
    verse: str = Field(description="Corresponding verse for which the sub story is generated")
    image_prompts: str = Field(description="Prompts for generating images that display the story visually")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "story_count": self.story_count, 
            "story": self.story,
            "verse": self.verse,
            "image_prompts": self.image_prompts
            }


class Stories(BaseModel):
    stories: List[Story]


sub_stories = PydanticOutputParser(pydantic_object=Stories)

template = """
You are given the lyrics: 
'{lyrics}'
of the song named {song_title}.

You have to take each verse from the lyrics and understand the meaning from it and stitch a story with the meaning of the whole song and
divide them into sub stories which will form a meaningful video and are used to generate respective images for each sub story.

Consider this prompt from the user on how they want the images or stories to be framed: {prompt}

Make sure the stories and image prompts are as detailed as they can be to make sure it is easier when generating the images.

{format_instructions}
"""

prompt = PromptTemplate(
    input_variables={"lyrics", "song_title", "prompt"},
    template=template,
    partial_variables={"format_instructions": sub_stories.get_format_instructions}
    )

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
)

chain = prompt | llm | sub_stories

if __name__=="__main__":
    print("Generating Stories")

    LYRICS = """
    త్రిదళం త్రిగుణాకారం త్రినేత్రం చ త్రియాయుధమ్ ।
    త్రిజన్మ పాపసంహారం ఏకబిల్వం శివార్పణమ్ ॥

    త్రిశాఖైః బిల్వపత్రైశ్చ అచ్ఛిద్రైః కోమలైః శుభైః ।
    తవపూజాం కరిష్యామి ఏకబిల్వం శివార్పణమ్ ॥

    కోటి కన్యా మహాదానం తిలపర్వత కోటయః ।
    కాంచనం శైలదానేన ఏకబిల్వం శివార్పణమ్ ॥

    కాశీక్షేత్ర నివాసం చ కాలభైరవ దర్శనమ్ ।
    ప్రయాగే మాధవం దృష్ట్వా ఏకబిల్వం శివార్పణమ్ ॥

    ఇందువారే వ్రతం స్థిత్వా నిరాహారో మహేశ్వరాః ।
    నక్తం హౌష్యామి దేవేశ ఏకబిల్వం శివార్పణమ్ ॥

    రామలింగ ప్రతిష్ఠా చ వైవాహిక కృతం తథా ।
    తటాకానిచ సంధానం ఏకబిల్వం శివార్పణమ్ ॥

    అఖండ బిల్వపత్రం చ ఆయుతం శివపూజనమ్ ।
    కృతం నామ సహస్రేణ ఏకబిల్వం శివార్పణమ్ ॥

    ఉమయా సహదేవేశ నంది వాహనమేవ చ ।
    భస్మలేపన సర్వాంగం ఏకబిల్వం శివార్పణమ్ ॥

    సాలగ్రామేషు విప్రాణాం తటాకం దశకూపయోః ।
    యజ్ఞ్నకోటి సహస్రస్య ఏకబిల్వం శివార్పణమ్ ॥
    దంతి కోటి సహస్రేషు అశ్వమేధశతక్రతౌ చ ।
    కోటికన్యా మహాదానం ఏకబిల్వం శివార్పణమ్ ॥

    బిల్వాణాం దర్శనం పుణ్యం స్పర్శనం పాపనాశనమ్ ।
    అఘోర పాపసంహారం ఏకబిల్వం శివార్పణమ్ ॥

    సహస్రవేద పాటేషు బ్రహ్మస్తాపనముచ్యతే ।
    అనేకవ్రత కోటీనాం ఏకబిల్వం శివార్పణమ్ ॥

    అన్నదాన సహస్రేషు సహస్రోపనయనం తధా ।
    అనేక జన్మపాపాని ఏకబిల్వం శివార్పణమ్ ॥

    బిల్వాష్టకమిదం పుణ్యం యః పఠేశ్శివ సన్నిధౌ ।
    శివలోకమవాప్నోతి ఏకబిల్వం శివార్పణమ్ ॥
    """

    TITLE = "బిల్వాష్టకం"

    PROMPT = """This song is about Lord Shiva, and lord shiva is being purified with the bael leaves and I want that depiction to be
    strong. In all the images lord shiva has to be there. And if the idol of Lord Shiva is there, the physical form shouldn't be there
    and vice versa."""

    result = chain.invoke(
        {
            "lyrics": LYRICS,
            "song_title": TITLE,
            "prompt": PROMPT,
        }
    )

    print("Here are your stories:------------------------------------------>\n")
    pprint(result)  # This since telugu verse is being printed as escaped unicode characters 
    # in the terminal.

