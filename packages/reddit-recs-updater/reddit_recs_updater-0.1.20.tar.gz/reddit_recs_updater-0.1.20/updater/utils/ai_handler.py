import json
import os
import time
import asyncio
import datetime
from replit import db
from openai import AsyncOpenAI
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()  


# Returns json object
async def get_openai_response(sys_prompt, user_prompt, model, response_format, caller):
  client = AsyncOpenAI()
  start_time = time.time()
  try:
    completion = await asyncio.wait_for(client.chat.completions.create(
      model=model,
      response_format=response_format,
      temperature=0,
      messages=[
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': user_prompt}
      ]
    ), timeout=600)
    duration = time.time() - start_time
    if completion:
      prompt_tokens = completion.usage.prompt_tokens
      completion_tokens = completion.usage.completion_tokens
      total_tokens = completion.usage.total_tokens
      return json.loads(completion.choices[0].message.content)
  except asyncio.TimeoutError:
    print("OpenAI request timed out")
    return None
  except Exception as e:
    print(f"Error in get_openai_response for fn {caller}, model {model}: {str(e)}")
    return None


async def get_openai_response_struct(sys_prompt, user_prompt, model, response_format, caller):
  client = AsyncOpenAI()
  start_time = time.time()
  try:
    completion = await asyncio.wait_for(client.beta.chat.completions.parse(
      model=model,
      response_format=response_format,
      temperature=0,
      messages=[
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': user_prompt}
      ]
    ), timeout=600)
    duration = time.time() - start_time
    if completion:
      prompt_tokens = completion.usage.prompt_tokens
      completion_tokens = completion.usage.completion_tokens
      total_tokens = completion.usage.total_tokens
      return completion.choices[0].message.parsed
  except asyncio.TimeoutError:
    print("OpenAI request timed out")
    return None
  except Exception as e:
    print(f"Error in get_openai_response: {str(e)}")
    return None
          

# # Returns json object
# async def get_groq_response(sys_prompt, user_prompt, model, response_format):
#   client = AsyncGroq(api_key=os.environ['groq_api_key'])
#   # start_time = time.time()
#   try:
#     chat_completion = await asyncio.wait_for(client.chat.completions.create(
#       model=model,
#       response_format={ "type": response_format },
#       temperature=0,
#       messages=[
#         {'role': 'system', 'content': sys_prompt},
#         {'role': 'user', 'content': user_prompt}
#       ]
#     ), timeout=150)
#     # duration = time.time() - start_time
#     # log_llm_call('Groq', model, duration, sys_prompt, user_prompt)
#     return json.loads(chat_completion.choices[0].message.content)
#   except asyncio.TimeoutError:
#     print("Groq request timed out")
#     return None
#   except Exception as e:
#     print(f"Error in get_groq_response: {str(e)}")
#     return None