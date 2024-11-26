import json
import logging
import uuid

from django.conf import settings
from django.urls import reverse
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment
from django.test import RequestFactory

#create a logger
logger = logging.getLogger(__name__)
loggerr.setLevel(logging.DEBUG)

# Create a file handler for logging
file_handler = logging.FileHandler('mpesa.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler for logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

@csrf_exempt
def initiate_payment(request):
    logger.info('initiate_payment')
    if request.method == 'POST':
        try:
            request_body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
            logger.debug(f'request_body: {request_body}')
            if request.content_type == 'application/json':
                data = json.loads(request_body)
            else:
                data = dict(request.POST)

            phone_number = data.get('phone_number')
            amount = data.get('amount')
            order_id = data.get('order_id')
            if order_id is None:
                order_id = str(uuid.uuid4())
                logger.info(f"Generate unique order_id: {order_id}")
            full_name = data.get('full_name')
            email = data.get('email')
            country = data.get('country')
            state = data.get('state')
            payment_method = data.get('payment_method')

            if not amount:
                logger.warning('Amount is required')
                return JsonResponse({'error': 'Amount is required'}, status=400)

            amount = float(amount)
            logger.debug(f'Phone number: {phone_number}, Amount: {amount}, Order Id: {order_id}')

            client = MpesaClient()
            account_reference = str(order_id)
            transaction_desc = 'Payment for order {}'.format(order_id)
            ngrok_url = settings.NGROK_URL

            if ngrok_url:
                callback_url = f'{ngrok_url}{reverse("mpesa:mpesa-callback")}'
            else:
                callback_url = reques.build_absolute_uri(reverse('mpesa-callback')) 
                
                   