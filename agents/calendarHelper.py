from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
import streamlit as st

from dotenv import load_dotenv
import os

from .tools.calendar_tools import init_calendar_service, get_time, get_events, set_event, delete_event
from .tools.google_authenticator import initialize_service



load_dotenv()

class CalendarAgent:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        service = initialize_service()
        init_calendar_service(service)
        
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                    You are a friendly and autonomous Google Calendar assistant who helps users manage their schedules effectively

                    You must follow several rules:
                    1. You must be polite and helpful
                    2. You must provide accurate information
                    3. You must not output the time code

                    If you see that there is an event at the desired time, you should think if you have to delete the event or not. There shouldn't be 2 events at

                    Don't ask follow up questions, take the responsibility into your own hands on what is the best option in case of colision.

                    """
                ),
                MessagesPlaceholder(variable_name = "messages", optional = True),
                ("user", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
            )

        tools = [
            get_time,
            get_events,
            set_event,
            delete_event
        ]
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    
    def generate_response(self, user_input):

        # Use the agent executor
        result = self.executor.invoke({"input": user_input, "messages": st.session_state.messages})
        return result["output"]  # Adjust based on actual output format

