import chainlit as cl
from chainlit import user_session
import openai
from os.path import join, dirname
from dotenv import load_dotenv
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
os.getenv('OPENAI_API_KEY')

prompt = """
SQL tables (and columns):
* Customers(customer_id, signup_date)
* Streaming(customer_id, video_id, watch_date, watch_minutes)

A well-written SQL query that {input}:

"""

model_name = "text-davinci-003"

settings = {
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"]
}

@cl.on_message
async def main(message: str):
    formatted_prompt=prompt.format(input=message)
    # Prepare the message for streaming
    msg = cl.Message(
        content="",
        language="sql",
        prompt=prompt,
        llm_settings=cl.LLMSettings(model_name=model_name, **settings),
    )

    async for stream_resp in await openai.Completion.acreate(
        model=model_name, prompt=formatted_prompt, stream=True, **settings
    ):
        token = stream_resp.get("choices")[0].get("text")
        await msg.stream_token(token)

    await msg.send()

    

