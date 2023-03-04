from django.utils.module_loading import import_string
from datetime import datetime, timedelta
from authentication.models import User
from idcp_project.celery import app


@app.task
def get_crawler_data(x):
    print("x")