# from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import BaseChatPromptTemplate
from langchain.agents import Tool, LLMSingleActionAgent, AgentExecutor, AgentOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from .config import Config
from typing import Dict, Any, List, Union
import re

queries_and_response = []

# def analyze_sentiment(sentences):
#     """
#     Analyzes the sentiment of a list of sentences using the FinBERT model.

#     :param sentences: A list of sentences to analyze.
#     :return: A list of dictionaries containing the sentiment analysis results for each sentence.
#     """
#     # Load the FinBERT model and tokenizer
#     finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
#     tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

#     # Create a sentiment analysis pipeline with the FinBERT model
#     nlp_pipeline = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

#     # Analyze sentiment of the provided sentences
#     results = nlp_pipeline(sentences)

#     return results


def run_duckduckgo_search(query):
    """
    Runs a search query using the DuckDuckGo search tool and returns the result.

    :param query: The search query string.
    :return: The search result as a string.
    """
    # Initialize the DuckDuckGo search tool
    search = DuckDuckGoSearchRun()

    # Run the search with the provided query
    result = search.run(query)

    return result


# Define custom output parser with detailed logging
class CustomOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        print("output--------")
        print(llm_output)
        print("output end--------")

        # Check if the agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )

        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)

        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")

        action = match.group(1).strip()
        action_input = match.group(2).strip()

        return AgentAction(
            tool=action,
            tool_input=action_input.strip(" ").strip('"'),
            log=llm_output,
        )

output_parser = CustomOutputParser()

# Define custom prompt template
class CustomPromptTemplate(BaseChatPromptTemplate):
    template: str
    tools: List[Tool]

    def format_messages(self, **kwargs) -> List[HumanMessage]:
        intermediate_steps = kwargs.pop("intermediate_steps", [])
        thoughts = ""

        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "

        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])

        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]

# Set up the template with history
template_with_history = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Answer the following questions as best you can. You have access to the following tools:

Search: to search stuff on the internet

**Your goal is to break down the question into multiple logical parts and search for the latest information related to each part separately. If required, use different word selections for searches to ensure comprehensive results. Finally, combine your findings and answer the original question, ensuring to include reasoning and sources for each part of your response. Always conclude with a "Final Answer" based on your findings. If sufficient information is not found, state that clearly.**

**Note: DO NOT REPEAT YOURSELF: Make sure your current search is different from past ones and do not form a cycle.**
**Strictly use the following format**!!!:

Question: {input}
Thought: Break down the question into multiple logical parts and decide what actions to take next.
Action: The action to take, should be one of [Search|Sentiment]
Action Input: The specific input to the action.
Observation: Result of the action (from web search, sentiment analysis, etc.).
...(This Thought/Action/Action Input/Observation process can repeat at most 4 times after that summarize and provide a relevant response)
Thought: Now, is this my answer? (Decide based on collected information)
Final Answer: The combined final answer to the original input question with reasoning and sources.
If sufficient information is not found, respond with:
Final Answer: I do not have sufficient information on this topic; I cannot provide an answer to this question.
In both cases, ensure that the information is presented according to best representation principles, and always include the name of the sources that were helpful in reaching this conclusion.

For example:

Question: What are the most favorable upcoming IPOs and why?

Thought: First, break down the question into parts: (1) Find the latest information on upcoming IPOs, (2) Determine the factors that make an IPO favorable, (3) Search for market sentiment regarding these IPOs.
Action: Search
Action Input: Latest upcoming IPOs in India 2024
Observation: List of upcoming IPOs...

Action: Search
Action Input: What factors make an IPO favorable?
Observation: Factors include...

Thought: Now, is this my answer? Combine the findings.
Final Answer: Based on the latest information, the most favorable upcoming IPOs are [IPO Names] due to factors such as [Factors]. Market sentiment suggests [Sentiment Analysis]. Sources: [source website Links]
If information is insufficient:
Final Answer: I do not have sufficient information on this topic; I cannot provide an answer to this question.
            Sources: [Only Name of the source websites]

Another example:
Question: How old is the CEO of Microsoft's wife?
Thought: First, I need to find out who the CEO of Microsoft is.
Action: Search
Action Input: Who is the CEO of Microsoft?
Observation: Satya Nadella is the CEO of Microsoft.
Thought: Now, is this my answer? No. Then I should find out Satya Nadella's wife.
Action: Search
Action Input: Who is Satya Nadella's wife?
Observation: Satya Nadella's wife's name is Anupama Nadella.
Thought: Now, is this my answer? No. Then, I need to check Anupama Nadella's age.
Action: Search
Action Input: How old is Anupama Nadella?
Observation: Anupama Nadella's age is 50.
Thought: I now know the final answer and now need to format it well.
Final Answer: Anupama Nadella is 50 years old.
            Sources: [Only Name of the source websites]

Previous conversation history:
{history}

### Input:
{input}

### Response:
{agent_scratchpad}"""

# Define tools
tools = [
    Tool(
        name="Search",
        func=run_duckduckgo_search,
        description="Useful for when you need to answer questions about current events"
    )
]

# Instantiate the prompt template with tools
prompt_with_history = CustomPromptTemplate(
    template=template_with_history,
    tools=tools,
    input_variables=["input", "intermediate_steps", "history"]
)

# Instantiate the LLM chain
llm_chain = LLMChain(
    llm= ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9, google_api_key = Config.GOOGLE_API_KEY),
    prompt=prompt_with_history
)

# Get tool names
tool_names = [tool.name for tool in tools]

# Define the agent
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)

# Define memory
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Define the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

# Function to run the agent
def run_agent(prompt):
    response = agent_executor.run(input=prompt)
    return response


def get_query_and_response(user_query: str):
  response = run_agent(user_query)
#   print(response)
  queries_and_response.append({"response": response, "query": user_query})
  return response


def clear_queries():
    global queries_and_response
    queries_and_response = []
