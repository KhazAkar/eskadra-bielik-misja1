import os

import aiohttp

# import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool
from pydantic import BaseModel

BIELIK_MODEL_NAME = os.getenv("BIELIK_AGENTIC_MODEL_NAME", "Bielik-11B-v2.6")


class WeatherOutput(BaseModel):
    city: str
    temperature: str
    weather: str


# llm_root = LiteLlm(model=f"ollama_chat/{BIELIK_CHAT_MODEL_NAME}")
llm_agentic = LiteLlm(
    model=f"openai/{BIELIK_MODEL_NAME}",
    api_key="jan",
    api_base="http://localhost:1337/v1",
)


async def get_weather(city: str) -> WeatherOutput:
    """
    search for weather information in a given city.

    args:
        city: the city to search for weather information.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://wttr.in/{city}?format=j1") as response:
            weather_data = await response.json()
        return WeatherOutput(
            city=city,
            temperature=weather_data["current_condition"][0]["temp_C"],
            weather=weather_data["current_condition"][0]["weatherDesc"][0]["value"],
        )


search_weather_tool = FunctionTool(func=get_weather)

root_agent = Agent(
    name="weather_search",
    description="Jesteś agentem szukającym pogody w podanym przez użytkownika mieście, raz na podane miasto",
    instruction="""
    You are a weather search agent.
    Your task is to find the weather in the city provided by the user.
    Call the 'get_weather' function **ONCE** with the city name.
    After receiving the result, **IMMEDIATELY** respond to the user in the format:
    'Pogoda w [city] to [weather] i temperatura wynosi [temperature] stopni Celsjusza.'
    Replace [city], [weather], and [temperature] with the actual, translated to Polish values from the function result.
    Refrain from any other actions or explanations unless asked explicitly by user.
    """,
    model=llm_agentic,
    tools=[search_weather_tool],
)
