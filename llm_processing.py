import logging
import os

from utils import ConfigLoader

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.agents import Tool, AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

logger = logging.getLogger(__name__)

with open("./configuration/openai/openai_secret", 'r') as f:
    os.environ['OPENAI_API_KEY'] = f.read()

class ModelAgent:
    """Langchain model agent."""

    def __init__(self, config_path: str = None):
        if config_path is not None:
            self.load_config()
            return
        self.tools: list[Tool] = []
        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are very powerful assistant, but don't know current events",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                }
                | self.prompt
                | self.llm_with_tools
                | OpenAIToolsAgentOutputParser()
        )

        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def process(self, query: str) -> str:
        """Processes user's query."""
        return self.executor.run(query)


    def load_config(self):
        pass


if __name__ == '__main__':
    from langchain_experimental.tools import PythonREPLTool

    model = ModelAgent()
    model.add_tool(PythonREPLTool())
    model.process("""Write script, which solves the task and execute it with provided inputs.
                     Task: Given two integer arrays nums1 and nums2, return an array of their intersection.
                      Each element in the result must be unique and you may return the result in any order.
                     Inputs: nums1 = [1,2,2,1], nums2 = [2,2]""")
