import openai
import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

openai.api_key = os.environ.get('OPENAI_API_KEY')

def save_png(repo_id: str):

    chat = ChatOpenAI(model="gpt-4", temperature=0.5)
    print("reading json model")
    with open(f"json_models/{repo_id}.json") as json_file:
        data = json.load(json_file)
        json_content = json.dumps(data)

    print("fetching prompt")
    with open("prompts/plantuml_generator.txt") as plantuml_prompt_file:
        plantuml_prompt = plantuml_prompt_file.read()

    messages = [
        SystemMessage(
            content=plantuml_prompt
        ),
        HumanMessage(
            content=json_content
        ),
    ]

    print("writing plantuml diagram")
    with open(f"plantuml_diagrams/{repo_id}.pu", "w+") as output_file:
        output_file.write(chat(messages).content)

    print("converting plantuml to png")
    os.system(f"java -jar plantuml.jar plantuml_diagrams/{repo_id}.pu")
    os.system(f"mv plantuml_diagrams/{repo_id}.png diagram_pngs/{repo_id}.png")
