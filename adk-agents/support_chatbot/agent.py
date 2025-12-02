import os

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm

BIELIK_MODEL_NAME = os.getenv(
    "BIELIK_MODEL_NAME", "SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M"
)


llm_model = LiteLlm(model=f"ollama_chat/{BIELIK_MODEL_NAME}")

support_mixxer = Agent(
    name="support_mixxer",
    description="Agent wsparcia klienta w języku polskim firmy SquirelSoft - program Mixxer.",
    instruction="""
    Jesteś agentem wsparcia dla firmy o nazwie SquirelSoft.
    Możesz również pomóc w problemach technicznych związanych wyłącznie z programem 'Mixxer'.
    Jeśli nie wiesz jak odpowiedzieć na pytanie, powiedz, że nie wiesz odpowiedzi.
    """,
    model=llm_model,
    output_key="mixxer",
)

support_jeger = Agent(
    name="support_jeger",
    description="Agent wsparcia klienta w języku polskim firmy SquirelSoft - program Jeger.",
    instruction="""
    Jesteś agentem wsparcia dla firmy o nazwie SquirelSoft.
    Możesz również pomóc w problemach technicznych związanych wyłącznie z programem 'Jeger'.
    Jeśli nie wiesz jak odpowiedzieć na pytanie, powiedz, że nie wiesz odpowiedzi.
    """,
    model=llm_model,
    output_key="jeger",
)

root_agent = SequentialAgent(
    name="support_chatbot",
    description="Czatbot wsparcia klienta firmy SquirelSoft.",
    sub_agents=[support_jeger, support_mixxer],
)
