"""
Test script for Multi-Agent RAG Chatbot
Tests all components individually and together
"""
import os
from dotenv import load_dotenv

load_dotenv()


def test_environment():
    """Test environment variables"""
    print("\n=== Testing Environment Variables ===")
    required_vars = ["OPENAI_API_KEY", "GOOGLE_API_KEY"]
    optional_vars = ["GROQ_API_KEY", "OPENAI_MODEL", "GOOGLE_MODEL"]

    required_set = bool(os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if required_set:
        for var in required_vars:
            value = os.getenv(var)
            if value:
                print(f"✓ {var}: {'*' * 10}{value[-4:]}")
            else:
                print(f"⚠ {var}: Not set")
    else:
        print("✗ No valid OpenAI or Google API key found. Set either OPENAI_API_KEY or GOOGLE_API_KEY.")

    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: Set")
        else:
            print(f"⚠ {var}: Not set (Optional)")


def test_vector_store():
    """Test vector store initialization"""
    print("\n=== Testing Vector Store ===")
    try:
        from vector_store import VectorStoreManager

        manager = VectorStoreManager()
        print("✓ VectorStoreManager initialized")

        # Test loading documents
        domains = ["product", "policy", "tech"]
        for domain in domains:
            folder_path = f"./data/{domain}"
            if os.path.exists(folder_path):
                docs = manager.load_documents_from_folder(folder_path)
                print(f"✓ {domain}: Loaded {len(docs)} document chunks")
            else:
                print(f"✗ {domain}: Folder not found at {folder_path}")

        return True
    except Exception as e:
        print(f"✗ Vector Store Error: {e}")
        return False


def test_tools():
    """Test custom tools"""
    print("\n=== Testing Tools ===")
    try:
        from tools import get_tools

        tools = get_tools()
        print(f"✓ Loaded {len(tools)} tools")

        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:50]}...")

        # Test DuckDuckGo (optional, requires internet)
        print("\nTesting DuckDuckGo Search...")
        ddg_tool = tools[0]
        result = ddg_tool._run("Python programming")
        if result and "Error" not in result:
            print("✓ DuckDuckGo search working")
        else:
            print(f"⚠ DuckDuckGo result: {result[:100]}")

        # Test Salary Predictor
        print("\nTesting Salary Predictor...")
        salary_tool = tools[1]
        result = salary_tool._run(5.0, 2, "Software Engineer")
        if result and "Error" not in result:
            print("✓ Salary Predictor working")
            print(f"  Result: {result[:100]}...")
        else:
            print(f"✗ Salary Predictor error: {result}")

        return True
    except Exception as e:
        print(f"✗ Tools Error: {e}")
        return False


def test_agents():
    """Test agent initialization"""
    print("\n=== Testing Agents ===")
    try:
        from agents import AgentManager

        manager = AgentManager()
        agents = manager.list_agents()
        print(f"✓ Initialized {len(agents)} agents: {agents}")

        # Test each agent
        for agent_type in agents:
            agent = manager.get_agent(agent_type)
            if agent:
                print(f"✓ {agent_type.capitalize()} agent ready")
            else:
                print(f"✗ {agent_type.capitalize()} agent failed")

        return True
    except Exception as e:
        print(f"✗ Agents Error: {e}")
        return False


def test_router():
    """Test router and query processing"""
    print("\n=== Testing Router ===")
    try:
        from router import QueryRouter

        router = QueryRouter()
        print("✓ Router initialized")

        # Test queries
        test_queries = [
            ("What products do you offer?", "product"),
            ("What is your return policy?", "policy"),
            ("How do I troubleshoot?", "tech"),
        ]

        print("\nTesting query routing...")
        for query, expected_agent in test_queries:
            result = router.process_query(query)
            actual_agent = result["agent"]
            status = "✓" if actual_agent == expected_agent else "⚠"
            print(f"{status} '{query}' → {actual_agent} (expected: {expected_agent})")

        return True
    except Exception as e:
        print(f"✗ Router Error: {e}")
        return False


def test_full_system():
    """Test complete system integration"""
    print("\n=== Testing Full System ===")
    try:
        from router import QueryRouter

        router = QueryRouter()

        test_query = "Tell me about your products"
        print(f"\nQuery: {test_query}")

        result = router.process_query(test_query)

        print(f"✓ Agent Selected: {result['agent']}")
        print(f"✓ Response Length: {len(result['response'])} chars")
        print(f"✓ Context Retrieved: {len(result['context'])} chars")
        print(f"\nResponse Preview:\n{result['response'][:200]}...")

        return True
    except Exception as e:
        print(f"✗ Full System Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Agent RAG Chatbot - System Test")
    print("=" * 60)

    tests = [
        ("Environment", test_environment),
        ("Vector Store", test_vector_store),
        ("Tools", test_tools),
        ("Agents", test_agents),
        ("Router", test_router),
        ("Full System", test_full_system),
    ]

    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} test failed with exception: {e}")
            results[name] = False

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
