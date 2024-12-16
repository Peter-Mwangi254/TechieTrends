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
logger.setLevel(logging.DEBUG)

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

            amount = int(amount)
            logger.debug(f'Phone number: {phone_number}, Amount: {amount}, Order Id: {order_id}')

            client = MpesaClient()
            account_reference = str(phone_number)
            transaction_desc = 'Payment for order {}'.format(order_id)
            ngrok_url = settings.NGROK_URL

            if ngrok_url:
                callback_url = f'{ngrok_url}/mpesa-callback/'
            else:
                callback_url = request.build_absolute_uri(reverse('mpesa-callback'))
                
            response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            logger.info("Payment initiated successfully")
            response_data = response.json() if hasattr(response, 'json') else response

            if response_data is None or 'CheckoutRequestID' not in response_data:
                logger.error("Invalid response from M-pesa API")
                return JsonResponse({'status': 'error', 'message': 'Invalid response from payment gateway'}),

            # Save payment information
            order = Order.objects.create(
                full_name=full_name,
                email=email,
                phone=phone_number,
                country=country,
                state=state,
                payment_method=payment_method,
                total_amount=amount
            )    
            payment= Payment(
                order=order,
                method='mpesa',
                amount=amount,
                transaction_id=response_data.get('CheckoutRequestID', 'N/A')
            )
            payment.save()

            return JsonResponse({'status': 'success', 'response': response_data, 'order_id': order_id})

        except Exception as e:
            logger.error(f"Error initiating payment: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        logger.warning('Invalid request method')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def mpesa_callback(request):
    logger.info('mpesa_callback')
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8') 
            response = json.loads(body)
            logger.debug(f"Callback response: {response}")

            if response['Body']['stkCallback']['ResultCode'] == 0:
                callback_metadata = response['Body']['stkCallback']['CallbackMetadata']
                merchant_request_id = response['Body']['stkCallback']['MerchantRequestID']
                checkout_request_id = response['Body']['stkCallback']['CheckoutRequestID']
                amount = next(item['Value'] for item in callback_metadata if item['Name'] == 'Amount')
                mpesa_receipt_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber')
                transaction_date = next(item['Value'] for item in callback_metadata if item['Name'] == 'TransactionDate')
                phone_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber')

                payment= Payment.objects.filter(transaction_id=checkout_request_id).first()
                if payment:
                    payment.status = 'completed'
                    payment.save()

                    order = payment.order
                    order.status = 'PAID'
                    order.save()
                    logger.info(f"Payment for order {order.id} completed successfully")
                    return JsonResponse({'status': 'success', 'message': 'Payment completed successfully'})
                else:
                    logger.warning(f"Payment not found")
                    return JsonResponse({'succcess': False, 'message': 'Payment not found'})
            else:
                logger.warning('Transaction failed')
                return JsonResponse({'success': False, 'message': 'Transaction failed'})

        except Exception as e:
           logger.error(f"Error processing callback: {e}")
           return JsonResponse({'success': False, 'message': str(e)}, status=500)

    logger.warning('Invalid request method')
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def create_order(request):
    logger.info('create_order called')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone')
            country = data.get('country')
            state = data.get('state')
            payment_method = data.get('payment_method')
            total_amount = data.get('total_amount')
            shipping_address = data.get('shipping_address')
            order_id = data.get('order_id')

            if not all([full_name, email, phone, country, state, payment_method, total_amount, shipping_address]):
                logger.warning('Missing required fields')
                return JsonResponse({'error': 'Missing required fields'}, status=400) 
            # Generate unique order_id if not provided
            if order_id is None:
                order_id = str(uuid.uuid4())
                logger.info(f"Generate unique order_id: {order_id}")

            if payment_method == 'mpesa':
                payment_data = {
                    'phone_number': phone,
                    'amount': total_amount,
                    'full_name': full_name,
                    'email': email,
                    'country': country,
                    'state': state,
                    'payment_method': payment_method,
                    'order_id': order_id
                }

                factory = RequestFactory()
                payment_request = factory.post('/dummy-url', data=json.dumps(payment_data), content_type='application/json')
                payment_request.META = request.META.copy()
                logger.info('Initiating Mpesa payment')
                return initiate_payment(payment_request)
            else:
                order = Order.objects.create(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    country=country,
                    state=state,
                    payment_method=payment_method,
                    total_amount=total_amount,
                    shipping_address=shipping_address,
                    order_id=order_id,
                    status='PENDING'
                )
                logger.info('Order created successfully')
                return JsonResponse({'status': 'success', 'order_id': order_id})

        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        logger.warning('Invalid request method')
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)            