import os
import gradio as gr
from openai import OpenAI

# --- 1. Securely Get API Key ---
# This safely reads the key you set in your terminal.
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. "
                     "Please set it in your terminal.")

# --- 2. Initialize the (Modern) OpenAI Client ---
client = OpenAI(api_key=api_key)

# --- 3. Define the Chatbot's "Personality" ---
SYSTEM_MESSAGE = (
    "You are a financial expert that specializes in "
    "real estate investment and negotiation. "
    "Be helpful, insightful, and clear."
)

# --- 4. The Core Logic Function ---
# Gradio's ChatInterface will automatically pass the
# 'message' (what the user just typed) and
# 'history' (the list of [user, assistant] pairs).
def CustomChatGPT(message, history):
    
    # We must build the list of messages to send to the API
    messages_to_send = [{"role": "system", "content": SYSTEM_MESSAGE}]
    
    # Add the past conversation (history)
    for user_msg, assistant_msg in history:
        messages_to_send.append({"role": "user", "content": user_msg})
        messages_to_send.append({"role": "assistant", "content": assistant_msg})
    
    # Add the user's very last message
    messages_to_send.append({"role": "user", "content": message})
    
    try:
        # --- 5. Use the Updated client.chat.completions.create ---
        # We use stream=True to get the response word-by-word
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_to_send,
            stream=True  # This makes the response feel immediate
        )
        
        # 'yield' streams the response back to Gradio one token at a time
        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message += chunk.choices[0].delta.content
                yield partial_message  # Send the updated message to the UI
                
    except Exception as e:
        yield f"An error occurred: {str(e)}"

# --- 6. Create the Gradio Web UI ---
print("Launching Gradio Chatbot Interface...")
demo = gr.ChatInterface(
    fn=CustomChatGPT,
    title="Intelligent Chatbot: Real Estate Expert",
    chatbot=gr.Chatbot(height=600),
    textbox=gr.Textbox(placeholder="Ask me about real estate investment...", container=False, scale=7),
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear Conversation",
)

# --- 7. Launch the App ---
if __name__ == "__main__":
    # share=True creates a public, shareable link for your chatbot
    demo.launch(share=True)