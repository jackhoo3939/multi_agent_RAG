"""
Configuration Checker
Validates system setup before running the application
"""
import os
import sys
from pathlib import Path


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.11+)")
        return False


def check_env_file():
    """Check if .env file exists"""
    if os.path.exists(".env"):
        print("✓ .env file exists")
        return True
    else:
        print("⚠ .env file not found")
        print("  → If you are using GitHub secrets or environment variables, this is okay")
        print("  → Otherwise run: cp .env.example .env")
        return False


def check_api_keys():
    """Check if API keys are set"""
    from dotenv import load_dotenv
    load_dotenv()

    keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    }

    has_required = bool(keys["OPENAI_API_KEY"] or keys["GOOGLE_API_KEY"])

    for key, value in keys.items():
        if value and value != f"your_{key.lower()}_here":
            print(f"✓ {key} is set")
        else:
            if key == "OPENAI_API_KEY":
                print("⚠ OPENAI_API_KEY not set (Optional if GOOGLE_API_KEY is provided)")
            elif key == "GOOGLE_API_KEY":
                print("⚠ GOOGLE_API_KEY not set (Optional if OPENAI_API_KEY is provided)")
            else:
                print(f"⚠ {key} not set (Optional)")

    if not has_required:
        print("✗ No valid OpenAI or Google API key found. Set either OPENAI_API_KEY or GOOGLE_API_KEY.")

    return has_required


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "langchain",
        "langgraph",
        "chromadb",
        "gradio",
        "duckduckgo_search",
        "openai",
        "joblib",
        "sklearn",
    ]

    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} not installed")
            all_installed = False

    if not all_installed:
        print("\n  → Run: pip install -r requirements.txt")

    return all_installed


def check_data_folders():
    """Check if data folders exist with documents"""
    domains = ["product", "policy", "tech"]
    all_exist = True

    for domain in domains:
        folder = Path(f"data/{domain}")
        if folder.exists():
            txt_files = list(folder.glob("*.txt"))
            if txt_files:
                print(f"✓ data/{domain}/ ({len(txt_files)} documents)")
            else:
                print(f"⚠ data/{domain}/ (no .txt files)")
                all_exist = False
        else:
            print(f"✗ data/{domain}/ not found")
            all_exist = False

    return all_exist


def check_model_file():
    """Check if salary model exists"""
    if os.path.exists("salary_model.joblib"):
        print("✓ salary_model.joblib exists")
        return True
    else:
        print("⚠ salary_model.joblib not found (Salary predictor won't work)")
        return False


def check_vector_store():
    """Check if vector store is initialized"""
    if os.path.exists("chroma_db"):
        print("✓ chroma_db/ exists (vector store initialized)")
        return True
    else:
        print("⚠ chroma_db/ not found")
        print("  → Run: python vector_store.py")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Multi-Agent RAG Chatbot - Configuration Check")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("API Keys", check_api_keys),
        ("Dependencies", check_dependencies),
        ("Data Folders", check_data_folders),
        ("Model File", check_model_file),
        ("Vector Store", check_vector_store),
    ]

    print("\n📋 Checking Configuration...\n")

    results = {}
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"✗ Error: {e}")
            results[name] = False

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    critical_checks = ["Python Version", "API Keys", "Dependencies"]
    critical_passed = all(results.get(check, False) for check in critical_checks)

    if critical_passed:
        print("✅ All critical checks passed!")
        print("\n🚀 Ready to run: python app.py")
    else:
        print("❌ Some critical checks failed.")
        print("\n📝 Please fix the issues above before running the application.")

    optional_checks = ["Environment File", "Model File", "Vector Store"]
    optional_passed = all(results.get(check, False) for check in optional_checks)

    if not optional_passed:
        print("\n⚠️  Optional components missing:")
        if not results.get("Vector Store", False):
            print("   - Run: python vector_store.py")
        if not results.get("Model File", False):
            print("   - Salary predictor tool will be unavailable")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
