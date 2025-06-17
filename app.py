from fastapi import FastAPI,Form
import smtplib
from fastapi.middleware.cors  import CORSMiddleware
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime


app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    
)

current_time = datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")
current_date = datetime.now().date().strftime("%d/%m/%Y")

@app.get("/")
async def root():
    return {"message":"FASTAPI is running !"}

@app.post("/feedback")
def send_feedback(Name : str = Form(...),Email : str = Form(...),Feedback : str = Form(...)):
    subject = f"You have an Message from {Name} !"
    msg = EmailMessage()
    msg["subject"] = subject
    msg["From"] = Email
    msg["To"] = os.getenv("MY_EMAIL")
    
    msg.set_content(
        f"""{Name} visited your website and left a Feedback ! 
Reply to {Email} at the earliest .You have recieved a new Feedback from {Name} at {formatted_time} Hours on {current_date}
The feedback is given below :
        
        
        {Feedback}
        """
    )
    
    
    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(os.getenv("MY_EMAIL"),os.getenv("MY_APP_PASSWORD"))
            server.send_message(msg)
            return {"response":1}
    except Exception as e:
        return {"response":0}
    
             