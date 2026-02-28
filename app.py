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
   
    prompt_path = os.path.join("prompts", "prompt_v3.md")
    
    try:

        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip()
            
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_instruction}
            ]
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return "שגיאה: קובץ הפרומפט לא נמצא בתיקיית PROMPTS"
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