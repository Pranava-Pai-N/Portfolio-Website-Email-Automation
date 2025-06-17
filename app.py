from fastapi import FastAPI,Form
import smtplib
from fastapi.middleware.cors  import CORSMiddleware
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz


india = pytz.timezone("Asia/Kolkata")


app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    
)

@app.get("/")
async def root():
    return {"message":"FASTAPI is running !"}

@app.post("/feedback")
def send_feedback(name : str = Form(...),email : str = Form(...),message : str = Form(...)):
    subject = f"You have an Message from {name} !"
    msg = EmailMessage()
    msg["subject"] = subject
    msg["From"] = email
    msg["To"] = os.getenv("MY_EMAIL")
    
    
    current_time = datetime.now(india)
    formatted_time = current_time.strftime("%H:%M:%S")
    current_date = datetime.now(india).date().strftime("%d/%m/%Y")
    
    msg.set_content(
        f"""{name} visited your website and left a Feedback ! 
Reply to {email} at the earliest .You have recieved a new Feedback from {name} at {formatted_time} Hours on {current_date}
The feedback is given below :
        
        
{message}
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
    
             