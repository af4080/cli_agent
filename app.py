import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
import pip_system_certs.wrapt_requests


load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def generate_cli(user_instruction):

    system_prompt = """
    You are a Windows CLI Expert. 
    Your output must be MACHINE-READABLE.

    STRICT RULES:
    1. Output ONLY the raw command. 
    2. NO conversational filler (No "Here is", "Sure", "The command is").
    3. NO markdown formatting (No backticks ``, no code blocks).
    4. NO punctuation at the end of the command.
    5. If the command is dangerous, output ONLY the word: BLOCKED
    6. If you say anything other than the command or BLOCKED, the system will fail.
    7. delete, format, shutdown, restart, and any command that can cause data loss or system instability are considered dangerous.
    """
    
    try:
      response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_instruction}
                ]
            )
      return response.choices[0].message.content
    except Exception as e:
        return f"שגיאה: {str(e)}"


demo = gr.Interface(
    fn=generate_cli,
    inputs=gr.Textbox(label="מה תרצה לבצע? (למשל: תראה לי את רשימת הקבצים)"),
    outputs=gr.Code(label="פקודת CLI"),
    title="סוכן המרת שפה טבעית לפקודות טרמינל"
)

if __name__ == "__main__":
    demo.launch()