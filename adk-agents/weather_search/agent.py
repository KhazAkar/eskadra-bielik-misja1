import os

import aiohttp

# import requests
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.function_tool import FunctionTool
from pydantic import BaseModel


class WeatherOutput(BaseModel):
    city: str
    temperature: str
    weather: str


llm_agentic = LiteLlm(
    model="openai/Bielik-11B-v2.6-Instruct",
    api_base=os.getenv("OPENAI_API_BASE", "http://localhost:8000"),
    api_key=os.getenv("OPENAI_API_KEY", "sk-no-key-required"),
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
