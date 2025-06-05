from typing import Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.chat_history import InMemoryChatMessageHistory


class FlightAgent:
    def __init__(self,  model_name: str = "gpt-4.1-nano-2025-04-14", thread_id: str = "test-session"):
        self.api_key=''
        self.model_name = model_name
        self.thread_id = thread_id
        self.model = ChatOpenAI(model=self.model_name, temperature=0.0, api_key=self.api_key)
        self.memory = MemorySaver()
        self.tools = self._define_tools()
        self.system_prompt = self._define_system_prompt()
        self.agent = self._create_agent()

    def _define_tools(self) -> List:
        '''Define the tools that the agent can use to perform tasks related to flight booking and management.
        Returns List'''
        @tool
        def book_flight(flight_number: str, date_departure: str, num_people: Optional[int] = 1,
                        date_return: Optional[str] = None) -> str:
            '''Book a flight with the given flight number, departure date, number of people, and return date.
            Args:
                flight_number (str): The flight number to book.
                date_departure (str): The departure date .
                num_people (Optional[int]): The number of passengers. Defaults to 1.
                date_return (Optional[str]): The return date . Defaults to None.'''
            return (
                f"Flight {flight_number} successfully booked from {date_departure} to {date_return} "
                f"for {num_people} passenger(s)."
            )

        @tool
        def check_flight_details(source: str, destination: str, date_departure: str, date_return: str,
                                 num_people: int) -> str:
            '''Check flight details including available flights, prices, and timings.
            Args:
                source (str): The departure city.
                destination (str): The destination city.
                date_departure (str): The departure date.
                date_return (str): The return date.
                num_people (int): The number of passengers.'''
            return (
                f"Available flight: AY123 | Price: $450/person | Start Time: 09:00 | Reaching Time: 18:00\n"
                f"Return Flight: AY124 | Price: $400/person | Start Time: 10:00 | Reaching Time: 19:00"
            )

        @tool
        def check_flight_status(flight_number: str) -> str:
            """Checks flight status weather it is on time or delayed or cancelled."""
            
            return (
                f"Your flight{flight_number} is on time. " 
                
            )
        @tool 
        def cancel_flight(pnr_number: str) -> str:
            """Cancel the flight with given pnr_number. PNR is a unique identifier for the flight booking."""
    
            return (
                f"Your flight with {pnr_number} has been cancelled. " 
                
            )
        @tool
        def reschedule_flight(pnr_number: str, date_to_be_changed) -> str:
            """Reschedule the flight on  given date_to_be_changed and pnr_number. PNR is a unique identifier for the flight booking."""
            
            return (
                f"Your flight has been rescheduled to {date_to_be_changed} with {pnr_number} " 
                
            )


        return [book_flight, check_flight_details, check_flight_status, cancel_flight, reschedule_flight]

    def _define_system_prompt(self) -> str:
        '''Define the system prompt that guides the agent's behavior and responses.'''
        msg =  """You are AYKA - airline AI assistant of United Airline. Your task is to assist users in:
            - Booking flights
            - Checking flight details and prices
            - Checking flight status
            - Cancelling flights
            - Rescheduling flights

            Instructions:
            1. You must use only tools to complete the tasks.
            2. You can introduce yourself as AYKA, the AI airline assistant.
            3. If the user asks for unrelated information, politely inform them you can only assist with flight-related queries."""
        return msg

    def _create_agent(self):
        '''Create the agent using the defined model, system prompt, and memory.'''
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt=self.system_prompt,
            checkpointer=self.memory
        )

    def get_response(self, user_message: str):
        config = {"configurable": {"thread_id": 'test-session'}}
        return self.agent.invoke({"messages": [("user", user_message)]}, config)
