import os
from typing import Callable,Annotated, List, Dict, Any,Union
from operator import add
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.api_core import retry
from google.generativeai.types import RequestOptions
from tools import list_tables, get_table, sql_query
from logger import logger
import numpy as np

# Configure your Gemini API key (e.g., via an environment variable)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AgentState(BaseModel):
    messages: Annotated[list, add] = Field(default_factory=list)

class SQLResult(BaseModel):
    # Accept either a list of dictionaries or a dictionary.
    data: Union[List[Dict[str, Any]], Dict[str, Any]]


def convert_numpy_types(data):
    if isinstance(data, np.generic):  # handles numpy.int64, numpy.float64, etc.
        return data.item()
    elif isinstance(data, dict):
        return {key: convert_numpy_types(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    else:
        return data


class SQLiteAgent:
    def __init__(self, tools: list[Callable], model_name="gemini-2.0-flash-exp"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(
            self.model_name,
            tools=tools,
            system_instruction=(
                """You are a helpful agent that can query a SQLite database containing customer data. "
                These are the columns of Customers Table first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    gender TEXT,
                    age INTEGER,
                    registered TEXT,
                    orders INTEGER,
                    spent REAL,
                    job TEXT,
                    hobbies TEXT,
                    is_married INTEGER"""
                "Use the provided tools to get information about the database schema and data. "
                "Only use information from the database. When you call a tool, include the function name "
                "and arguments. Do not fabricate information."""
            )
        )
        self.tools = tools
        self.tool_mapping = {tool.__name__: tool for tool in self.tools}
        self.graph = None
        self.build_agent()

    def call_llm(self, state: AgentState):
        response = self.model.generate_content(
            state.messages,
            request_options=RequestOptions(
                retry=retry.Retry(initial=10, multiplier=2, maximum=60, timeout=300)
            ),
        )
        return {
            "messages": [
                type(response.candidates[0].content).to_dict(
                    response.candidates[0].content
                )
            ]
        }


    def use_tool(self, state: AgentState):
        assert any("function_call" in part for part in state.messages[-1]["parts"])
        tool_result_parts = []
        for part in state.messages[-1]["parts"]:
            print('Part:', part)
            if "function_call" in part:
                name = part["function_call"]["name"]
                print('Name:', name)
                func = self.tool_mapping[name]
                print('Func:', func)
                result = func(**part["function_call"]["args"])
                print('Result:', result)
                
                # Convert numpy types to native Python types
                converted_result = convert_numpy_types(result)
                
                # Wrap the converted result into our Pydantic model
                sql_result = SQLResult(data=converted_result)
                
                tool_result_parts.append(
                    {
                        "function_response": {
                            "name": name,
                            "response": sql_result.model_dump(mode="json"),
                        }
                    }
                )
        return {"messages": [{"role": "tool", "parts": tool_result_parts}]}




    @staticmethod
    def should_we_stop(state: AgentState) -> str:
        logger.debug(
            f"Entering should_we_stop function. Current message: {state.messages[-1]}"
        )  # Added log
        if any("function_call" in part for part in state.messages[-1]["parts"]):
            logger.debug(f"Calling tools: {state.messages[-1]['parts']}")
            return "use_tool"
        else:
            logger.debug("Ending agent invocation")
            return END

    def build_agent(self):
        builder = StateGraph(AgentState)
        builder.add_node("call_llm", self.call_llm)
        builder.add_node("use_tool", self.use_tool)
        builder.add_edge(START, "call_llm")
        builder.add_conditional_edges("call_llm", self.should_we_stop)
        builder.add_edge("use_tool", "call_llm")
        self.graph = builder.compile()

    def invoke(self, user_query: str) -> str:
        """
        Invoke the agent with a user query and return the final response.
        """
        initial_state = AgentState(messages=[{"role": "user", "parts": [user_query]}])
        print('Initial State...',initial_state)
        output_state = self.graph.invoke(initial_state)
        print('Output State...',output_state)
        final_message = output_state["messages"][-1]
        print('Final Message...',final_message)
        # Depending on the content structure, extract the text
        if "parts" in final_message and final_message["parts"]:
            return final_message["parts"][-1]["text"]
        else:
            return "No response generated."
