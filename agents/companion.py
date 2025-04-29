from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

class CognitiveCareAgent:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        @tool 
        def call_caregiver(situation: str) -> str:
            """
            Call if the user is in distress or needs immediate assistance.

            args:
                situation (str): A thorough description of the situation that requires caregiver assistance.
            """
            return "Calling your caregiver..."

        @tool
        def get_time() -> str:
            """
            Get the current time.
            """
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                    You are an expert in cognitive health and Alzheimer's prevention who provides medical advice and companionship to users
                    suffering from Alzheimer's disease. You are friendly, empathetic, and knowledgeable. Your goal is to provide personalized 
                    recommendations based on the user's profile and questions as well as to engage in meaningful conversations to help them feel less isolated.

                    """
                ),
                MessagesPlaceholder(variable_name = "messages", optional = True),
                ("user", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
                
            ]
            )

        tools = [get_time, call_caregiver]
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def generate_response(self, user_input, user_profile):
        # Build the context dynamically
        #context = f"The user is {user_profile['age']} years old and follows the {user_profile['diet']} diet."

        # Combine the prompt
        '''full_prompt = (
            f"{context}\n"
            f"User's question: {user_input}\n"
            "Provide advice considering their lifestyle."
        )'''

        # Use the agent executor
        result = self.executor.invoke({"input": user_input, "messages": st.session_state.messages})
        return result["output"]  # Adjust based on actual output format


if __name__ == "__main__":
    # Example usage
    agent = CognitiveCareAgent()
    user_input = "What should I do to improve my cognitive health?"
    response = agent.generate_response(user_input, [])
    print(response)