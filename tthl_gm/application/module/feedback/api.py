from django.contrib import admin
from feedback.models import UserFeedback

def insert_feedback(data):
    feedback = UserFeedback(id=0,name=data["name"],email=data["email"],message=data["message"],send_time=data["time"],response_flag=False)
    feedback.save

def update_flag(email,message):
    UserFeedback.objects.filter(email=email).filter(message=message).update(response_flag=True)

