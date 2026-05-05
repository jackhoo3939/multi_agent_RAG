"""
Router System using LangGraph
Routes user queries to appropriate specialized agents
"""
import os
from typing import TypedDict, Annotated, Literal
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from agents import AgentManager
from dotenv import load_dotenv

load_dotenv()


class RouterState(TypedDict):
    """State for the router graph"""
    query: str
    chat_history: list
    selected_agent: str
    agent_response: str
    context: str


class QueryRouter:
    """Routes queries to appropriate agents using LangGraph"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0
        )
        self.agent_manager = AgentManager()
        self.graph = self._build_graph()

    def _classify_query(self, state: RouterState) -> RouterState:
        """Classify the query and select appropriate agent"""
        classification_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a query classifier. Analyze the user's question and determine which agent should handle it.

Available agents:
- product: Questions about products, features, specifications, recommendations, product comparisons
- policy: Questions about warranty, returns, refunds, delivery, shipping, company policies
- tech: Questions about technical support, troubleshooting, technical issues, how-to guides

Respond with ONLY ONE WORD: product, policy, or tech"""),
            ("human", "{query}")
        ])

        chain = classification_prompt | self.llm
        response = chain.invoke({"query": state["query"]})
        selected_agent = response.content.strip().lower()

        if selected_agent not in ["product", "policy", "tech"]:
            selected_agent = "product"

        state["selected_agent"] = selected_agent
        return state

    def _route_to_agent(self, state: RouterState) -> RouterState:
        """Route to the selected agent and get response"""
        agent = self.agent_manager.get_agent(state["selected_agent"])

        if agent:
            result = agent.run(
                query=state["query"],
                chat_history=state.get("chat_history", [])
            )
            state["agent_response"] = result["output"]
            state["context"] = result["context"]
        else:
            state["agent_response"] = f"Error: Agent '{state['selected_agent']}' not available."
            state["context"] = ""

        return state

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(RouterState)

        workflow.add_node("classify", self._classify_query)
        workflow.add_node("route", self._route_to_agent)

        workflow.set_entry_point("classify")
        workflow.add_edge("classify", "route")
        workflow.add_edge("route", END)

        return workflow.compile()

    def process_query(self, query: str, chat_history: list = None) -> dict:
        """Process a user query through the router"""
        initial_state = {
            "query": query,
            "chat_history": chat_history or [],
            "selected_agent": "",
            "agent_response": "",
            "context": ""
        }

        result = self.graph.invoke(initial_state)

        return {
            "query": result["query"],
            "agent": result["selected_agent"],
            "response": result["agent_response"],
            "context": result["context"]
        }


if __name__ == "__main__":
    router = QueryRouter()
    test_query = "What is your return policy?"
    result = router.process_query(test_query)
    print(f"\nQuery: {result['query']}")
    print(f"Selected Agent: {result['agent']}")
    print(f"Response: {result['response']}")
