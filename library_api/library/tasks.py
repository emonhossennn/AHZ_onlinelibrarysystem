
from celery import shared_task
from .models import Book
import time

@shared_task
def long_running_task(book_id):
    time.sleep(10)
    book = Book.objects.get(id=book_id)
    print(f"Background Task Completed for Book: {book.title}")

from .tasks import long_running_task

def perform_create(self, serializer):
    book = serializer.save()
    long_running_task.delay(book.id)
