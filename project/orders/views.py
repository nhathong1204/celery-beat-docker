from django.shortcuts import render
from django.views.generic import ListView

from .models import Order, Product


import time
import random
from string import ascii_lowercase
from core.tasks import task_send_welcome_email
from django.db import transaction
from celery.utils.log import get_task_logger
from core.models import User
from django.http import HttpResponse
logger = get_task_logger(__name__)


class OrderListView(ListView):
    model = Order

def random_username():
    username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
    return username

@transaction.atomic
def transaction_celery2(request):
    username = random_username()
    user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    # the task does not get called until after the transaction is committed
    transaction.on_commit(lambda: task_send_welcome_email.delay(user.pk))

    time.sleep(1)
    return HttpResponse('test')