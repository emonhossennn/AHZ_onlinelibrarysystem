from celery import shared_task
from .models import Book
from datetime import datetime, timedelta

@shared_task
def archive_old_books():
    ten_years_ago = datetime.now().date() - timedelta(days=365*10)
    Book.objects.filter(published_date__lt=ten_years_ago, is_archived=False).update(is_archived=True)
