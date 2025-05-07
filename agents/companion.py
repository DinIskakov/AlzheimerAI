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

from .calendarHelper import CalendarAgent

load_dotenv()

class CognitiveCareAgent:
    def __init__(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        profile = st.session_state.get("user_profile", {})
        medical = ', '.join(profile["medical_conditions"]) if profile["medical_conditions"] else "None"

        if "calendar_agent" not in st.session_state:
            st.session_state.calendar_agent = CalendarAgent()


        @tool 
        def modify_calendar(query: str) -> str:
            """
            Call this tool whenever the user wants to know something about their calendar or change something in it.
            The query should be the action related to the calendar that the user wants to perform.
            args:
                query (str): The action related to the calendar that the user wants to perform.
            """
            try:
                result = st.session_state.calendar_agent.generate_response(query)
                if result:
                    return result
                return "Failed to modify calendar. Please try again."
            
            except Exception as e:
                return f"Error modifying calendar: {str(e)}"

        @tool 
        def call_caregiver(situation: str) -> str:
            """
            Call if the user is in distress or needs immediate assistance.

            args:
                situation (str): A thorough description of the situation that requires caregiver assistance.
            """
            return "Calling your caregiver..."

        
        early = """You are interacting with an individual recently diagnosed with early-stage Alzheimer’s disease. 
                    They retain significant independence and are seeking guidance on managing their condition. 
                    Your role is to: 
                    - Provide information on lifestyle adjustments that may slow disease progression.
	                - Assist in planning for future care needs, including legal and financial considerations.
	                - Encourage participation in social and mentally stimulating activities.
	                - Offer emotional support to help them cope with their diagnosis.

                    Maintain a tone that is supportive, informative, and empowering, focusing on the individual’s strengths and abilities."""
        
        middle = """You are engaging with an individual in the middle stage of Alzheimer’s disease. 
                    They are experiencing increased memory loss and may require assistance with daily activities. 
                    Your responsibilities include:
                    - Offering strategies to manage behavioral changes and communication difficulties.
                    - Providing guidance on establishing structured routines to enhance daily functioning.
                    - Supporting caregivers by sharing techniques to handle challenges such as wandering or agitation.
                    - Emphasizing the importance of safety measures within the home environment.

                    Ensure your responses are compassionate, practical, and tailored to the evolving needs of both the individual and their caregivers.
                    """
        
        late = """You are providing support to an individual in the late stage of Alzheimer’s disease, where they require full-time care and have limited communication abilities. 
                    Your focus should be on:
                    - Ensuring comfort through sensory stimulation, such as music and gentle touch.
                    - Guiding caregivers on maintaining the individual’s dignity and quality of life.
                    - Advising on managing physical health concerns, including nutrition and mobility.
                    - Offering emotional support to caregivers coping with the demands of end-stage care.
                    

                    Adopt a tone that is gentle, empathetic, and centered on preserving the individual’s comfort and dignity"""
        
        stage = profile.get("stage", "early")
        stage_prompts = {
            "early": early,
            "middle": middle,
            "late": late
        }
        stage_guide = stage_prompts.get(stage, early)
        
        base_prompt = """
                    You are an expert in cognitive health and Alzheimer's prevention who provides medical advice and companionship to users
                    suffering from Alzheimer's disease. You are friendly, empathetic, and knowledgeable. Your goal is to provide personalized 
                    recommendations based on the user's profile and questions as well as to engage in meaningful conversations to help them feel less isolated.
                    """
        
        context_prompt = f"""
                        {base_prompt}


                        {stage_guide}

                        User Profile:
                        - Age: {profile['age']}
                        - Sleep: {profile['sleep_hours']} hrs/night
                        - Physical Activity: {profile['activity_level']}
                        - Cognitive Engagement: {profile['cognitive_engagement']}
                        - Medical Conditions: {medical}

                        Adapt your tone and suggestions based on the user's diagnosis stage and cognitive capacity.
                        """
        
        system_prompt = system_prompt = f"""
                        {base_prompt}

                        Stage-Specific Guidelines:
                        {stage_guide}

                        {context_prompt}

                        You have access to the following tools:
                            1. **Modify Calendar**: Use this tool to help the user manage their calendar and schedule appointments.
                            Call this tool with the query related to the calendar actions the user wants to perform.
                            It can delete, set, or get events from the calendar.
                            2. **Call Caregiver**: Use this tool if the user is in distress or needs immediate assistance.
                            If through conversation you believe that the user is in a worse state than they say, call this tool.

                        The app also contains an activities page where the user can find brain stimulating activities to do,
                        you can refer to this page and suggest activities to the user. The activities include:
                        - Language Learning
                        - Memory Puzzles
                        - Mathematical Puzzles
                        """
        

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    system_prompt
                ),
                MessagesPlaceholder(variable_name = "messages", optional = True),
                ("user", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
                
            ]
            )

        tools = [call_caregiver, modify_calendar]
        agent = create_tool_calling_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def generate_response(self, user_input, user_profile):
        # Build the context dynamically
        #context = f"The user is {user_profile['age']} years old and follows the {user_profile['diet']} diet."

        # Combine the prompt
        
        # Use the agent executor
        result = self.executor.invoke({"input": user_input, "messages": st.session_state.messages})
        return result["output"]  # Adjust based on actual output format


if __name__ == "__main__":
    # Example usage
    agent = CognitiveCareAgent()
    user_input = "What should I do to improve my cognitive health?"
    response = agent.generate_response(user_input, [])
    print(response)