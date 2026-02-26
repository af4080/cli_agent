import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
import pip_system_certs.wrapt_requests

# טעינת המפתח הסודי מקובץ .env
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), # ודאי שבקובץ .env רשום GROQ_API_KEY
    base_url="https://api.groq.com/openai/v1",
)

def generate_cli(user_instruction):
    # כאן מתחילה הנדסת הפרומפטים!
    system_prompt = """
    You are a professional CLI assistant. 
    Convert the user's natural language instruction into a valid terminal command.
    Return ONLY the command itself. No explanations, no markdown formatting.
    """
    
    try:
      response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # או הדגם הספציפי שיש לך אליו גישה
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_instruction}
                ]
            )
      return response.choices[0].message.content
    except Exception as e:
        return f"שגיאה: {str(e)}"

# יצירת ממשק המשתמש עם Gradio
demo = gr.Interface(
    fn=generate_cli,
    inputs=gr.Textbox(label="מה תרצה לבצע? (למשל: תראה לי את רשימת הקבצים)"),
    outputs=gr.Code(label="פקודת CLI"),
    title="סוכן המרת שפה טבעית לפקודות טרמינל"
)

if __name__ == "__main__":
    demo.launch()