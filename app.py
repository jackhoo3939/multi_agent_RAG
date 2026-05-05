"""
Gradio Web Interface for Multi-Agent Chatbot
"""
import gradio as gr
from router import QueryRouter
from vector_store import setup_vector_stores
import os
from dotenv import load_dotenv

load_dotenv()


class ChatbotUI:
    """Gradio interface for the multi-agent chatbot"""

    def __init__(self):
        self.router = None
        self.chat_history = []

    def initialize_system(self):
        """Initialize vector stores and router"""
        try:
            if not os.path.exists("./chroma_db"):
                print("Initializing vector stores...")
                setup_vector_stores()

            print("Initializing router and agents...")
            self.router = QueryRouter()
            return "✓ System initialized successfully!"
        except Exception as e:
            return f"✗ Error initializing system: {str(e)}"

    def chat(self, message: str, history: list) -> tuple:
        """Process chat message and return response"""
        if not self.router:
            init_msg = self.initialize_system()
            if "Error" in init_msg:
                return history + [[message, init_msg]], ""

        try:
            result = self.router.process_query(message, self.chat_history)

            response_text = f"**[{result['agent'].upper()} Agent]**\n\n{result['response']}"

            history.append([message, response_text])
            self.chat_history.append({"role": "user", "content": message})
            self.chat_history.append({"role": "assistant", "content": result['response']})

            return history, ""

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            history.append([message, error_msg])
            return history, ""

    def clear_chat(self):
        """Clear chat history"""
        self.chat_history = []
        return [], ""

    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(title="Multi-Agent RAG Chatbot", theme=gr.themes.Soft()) as interface:
            gr.Markdown(
                """
                # 🤖 Multi-Agent RAG Chatbot
                Ask questions about **Products**, **Policies**, or **Technical Support**.
                The system will automatically route your question to the right specialist agent.

                ### Available Tools:
                - 🔍 DuckDuckGo Search (for current information)
                - 💰 Salary Predictor (for salary estimates)
                """
            )

            with gr.Row():
                with gr.Column(scale=4):
                    chatbot = gr.Chatbot(
                        label="Chat History",
                        height=500,
                        show_label=True
                    )

                    with gr.Row():
                        msg = gr.Textbox(
                            label="Your Message",
                            placeholder="Ask about products, policies, or technical support...",
                            scale=4
                        )
                        submit_btn = gr.Button("Send", variant="primary", scale=1)

                    with gr.Row():
                        clear_btn = gr.Button("Clear Chat", variant="secondary")

                with gr.Column(scale=1):
                    gr.Markdown(
                        """
                        ### Agent Types:
                        - **PRODUCT**: Product info, features, specs
                        - **POLICY**: Warranty, returns, delivery
                        - **TECH**: Technical support, troubleshooting

                        ### Example Questions:
                        - "What products do you offer?"
                        - "What is your return policy?"
                        - "How do I troubleshoot X?"
                        - "Search for latest tech trends"
                        - "Predict salary for 5 years experience"
                        """
                    )

            submit_btn.click(
                fn=self.chat,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )

            msg.submit(
                fn=self.chat,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )

            clear_btn.click(
                fn=self.clear_chat,
                outputs=[chatbot, msg]
            )

        return interface


def main():
    """Launch the Gradio app"""
    chatbot_ui = ChatbotUI()

    print("Initializing system...")
    init_result = chatbot_ui.initialize_system()
    print(init_result)

    interface = chatbot_ui.create_interface()

    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )


if __name__ == "__main__":
    main()

