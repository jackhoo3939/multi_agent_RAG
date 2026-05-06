"""
Multi-Agent System with RAG
Defines three specialized agents: Product, Policy, and Tech Support
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.chat_models import ChatGooglePalm, ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from vector_store import VectorStoreManager
from tools import get_tools

load_dotenv()


class RAGAgent:
    """Base class for RAG-enabled agents"""

    def __init__(
        self,
        agent_type: str,
        vector_store: Chroma,
        tools: List = None,
        model_name: str = None
    ):
        self.agent_type = agent_type
        self.vector_store = vector_store
        self.tools = tools or []

        if os.getenv("GOOGLE_API_KEY"):
            self.llm = ChatGooglePalm(
                model_name=model_name or os.getenv("GOOGLE_MODEL", "models/chat-bison-001"),
                temperature=0.7,
                google_api_key=os.getenv("GOOGLE_API_KEY"),
            )
        else:
            self.llm = ChatOpenAI(
                model=model_name or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                temperature=0.7,
            )

        self.prompt = self._create_prompt()
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def _create_prompt(self) -> ChatPromptTemplate:
        """Create agent-specific prompt"""
        system_messages = {
            "product": (
                "You are a Product Specialist agent. "
                "Your expertise is in product information, features, specifications, and recommendations. "
                "Use the provided context from the knowledge base to answer questions accurately. "
                "If you need current market information, use the duckduckgo_search tool. "
                "For salary-related questions about product roles, use the salary_predictor tool."
            ),
            "policy": (
                "You are a Policy Specialist agent. "
                "Your expertise is in company policies including warranty, returns, refunds, and delivery. "
                "Use the provided context from the knowledge base to answer questions accurately. "
                "Always cite specific policy details when answering. "
                "If policies have changed recently, use the duckduckgo_search tool to find updates."
            ),
            "tech": (
                "You are a Technical Support agent. "
                "Your expertise is in troubleshooting, technical issues, and providing solutions. "
                "Use the provided context from the knowledge base to answer questions accurately. "
                "If you need current technical information or solutions, use the duckduckgo_search tool. "
                "For salary questions about tech roles, use the salary_predictor tool."
            )
        }

        return ChatPromptTemplate.from_messages([
            ("system", system_messages.get(self.agent_type, "You are a helpful assistant.")),
            ("system", "Context from knowledge base:\n{context}"),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context from vector store"""
        docs = self.vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context if context else "No relevant context found."

    def run(self, query: str, chat_history: List = None) -> Dict[str, Any]:
        """Run the agent with RAG context"""
        context = self.retrieve_context(query)

        result = self.agent_executor.invoke({
            "input": query,
            "context": context,
            "chat_history": chat_history or []
        })

        return {
            "agent": self.agent_type,
            "output": result["output"],
            "context": context
        }


class AgentManager:
    """Manages all specialized agents"""

    def __init__(self):
        self.vector_manager = VectorStoreManager()
        self.tools = get_tools()
        self.agents = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all agents with their vector stores"""
        domains = ["product", "policy", "tech"]

        for domain in domains:
            try:
                vector_store = self.vector_manager.get_vector_store(
                    collection_name=f"{domain}_collection"
                )
                self.agents[domain] = RAGAgent(
                    agent_type=domain,
                    vector_store=vector_store,
                    tools=self.tools
                )
                print(f"✓ {domain.capitalize()} agent initialized")
            except Exception as e:
                print(f"⚠ Warning: Could not initialize {domain} agent: {e}")

    def get_agent(self, agent_type: str) -> RAGAgent:
        """Get a specific agent"""
        return self.agents.get(agent_type)

    def list_agents(self) -> List[str]:
        """List all available agents"""
        return list(self.agents.keys())

