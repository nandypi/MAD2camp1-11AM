from celery import Celery
from celery.schedules import crontab

app = Celery('celery_app', broker='redis://localhost:6379/0')

app.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

import time
from mail import send_mail
from models import db, User, Item
from app import app as flask_app

@app.task()
def background_task():
    # Your background task logic here
    for i in range(9):
        print("Background task is running...")
        time.sleep(1)
    # convert all items to csv
    with flask_app.app_context():
        items = Item.query.all()
    with open('static/export.csv', 'w') as f:
        f.write("id,name,description,image_url\n")
        for item in items:
            f.write(f"{item.id},{item.name},{item.description},{item.image_url}\n")
    body='''
<h1>CSV Export Completed</h1>
<p>The CSV export task has been completed successfully.</p>
<a href="http://localhost:5000/static/export.csv" download>Download CSV</a>
'''
    send_mail("admin@gmail.com", "CSV Export Completed", body)
    return "Background task completed!"

@app.task()
def daily_reminders():
    with flask_app.app_context():
        users = User.query.all()
    for user in users:
        body = f'''
<h1>Daily Reminder</h1>
<p>Hi {user.email},</p>
<p>This is a daily reminder. Click <a href="http://localhost:5000">here</a> to visit the app.</p>
'''
        send_mail(user.email, "Daily Reminder", body)
    return "Daily reminders sent!"

@app.task()
def monthly_report():
    with flask_app.app_context():
        users = User.query.all()
    for user in users:
        body = f'''
<h1>Monthly Report</h1>
<p>Hi {user.email},</p>
<p>This is your monthly report</p>
<table>
    <tr>
        <th>Item</th>
        <th>Description</th>
    </tr>
    <!-- Add your report data here -->
</table>
'''
        send_mail(user.email, "Monthly Report", body)
    return "Monthly report sent!"

from webhook import main

@app.task()
def greet_gspace():
    main(msg="Hello, Google Chat!")
    return "Greeting sent to Google Chat!"

app.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'celery_app.daily_reminders',
        'schedule': crontab(hour=11, minute=35),  # Every day at 9:00 AM
    },
    'monthly-report': {
        'task': 'celery_app.monthly_report',
        'schedule': crontab(day_of_month=27, hour=11, minute=35),  # On the 1st of every month at 10:00 AM
    },
    'greet-gspace': {
        'task': 'celery_app.greet_gspace',
        'schedule': crontab(hour=11, minute=40),  # Every day at 9:00 AM
    }
}