from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import stripe
from django.conf import settings
from orders.models import Order
from .models import Payment


class CreateCheckoutSession(APIView):
    def post(self, request):
        dataDict = dict(request.data)

        order_id = dataDict['order_id']
        try:
            order_obj = Order.objects.get(id=order_id)
        except Order.DoesNotExist as e:
            print(e)
            return Response('Order ID not found', status=404)

        # TODO: check if the payment processing is done by the same user
        if order_obj.order_placed_by != request.user:
            return Response('Unauthorized access', status=400)

        # check if the order is already paid
        # if paid, then just return the
        if order_obj.payment_status == 'paid':
            data = {
                'order_id': order_id,
                'payment_status': order_obj.payment_status,
                'payment_intent_id': order_obj.payments.last().stripe_payment_intent_id
            }
            return Response(data=data, status=200)
        
        # print(order_obj.ordereditems.all())

        total = sum([float(ordered_item.item.price) * int(ordered_item.quantity) for ordered_item in order_obj.ordereditems.all()])

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order ID: {order_id}'
                        },
                        'unit_amount': int(total*100)
                    },

                    'quantity': 1
                }],

                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,
                # cancel_url=
            )
            # checkout_session.status in ('open', 'completed', 'expired')
            checkout_session_id = checkout_session.id
            print(checkout_session_id)

            try:
                p = Payment.objects.get(order=order_obj)
                p.checkout_session_id = checkout_session_id
                p.save()
            except Payment.DoesNotExist:
                p = Payment.objects.create(
                    order=order_obj,
                    checkout_session_id=checkout_session_id,
                )
                p.save()
            except Payment.MultipleObjectsReturned:
                print("Multiple Payment object returned")

            data = {
                'order_id': order_obj.id,
                'checkout_url': checkout_session.url,
            }
            return Response(data=data, status=201)
        except Exception as e:
            print(e)
            return Response(status=403)


class StripePaymentWebhook(APIView):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        webhook_secret = settings.WEBHOOK_ENDPOINT_SECRET_KEY

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        # Handle the event
        if event.type == 'charge.succeeded':
            # payment_intent = dict(event.data.object)
            pass

        if event.type == 'payment_intent.succeeded':
            pass
        elif event.type == 'payment_method.attached':
            pass
        elif event.type == 'payment_method.completed':
            pass
        elif event.type == 'payment_method.succeeded':
            pass

        elif event.type == 'checkout.session.completed':
            checkout_session_obj = dict(event.data.object)
            checkout_id = checkout_session_obj['id']
            amount = checkout_session_obj['amount_total']
            payer_email = checkout_session_obj['customer_details']['email']
            payer_name = checkout_session_obj['customer_details']['name']
            payer_phone = checkout_session_obj['customer_details']['phone']
            stripe_payment_intent_id = checkout_session_obj['payment_intent']
            payment_status = checkout_session_obj['payment_status']

            try:
                payment_obj = Payment.objects.get(
                    checkout_session_id=checkout_id)
                payment_obj.stripe_payment_intent_id = stripe_payment_intent_id
                payment_obj.payer_email = payer_email
                payment_obj.payer_name = payer_name
                payment_obj.payer_phone = payer_phone
                payment_obj.amount = float(amount)

                payment_obj.payment_status = payment_status
                payment_obj.save()

                # now update the order paid status
                order = payment_obj.order
                order.payment_status = payment_status
                order.payment_id = payment_obj.id
                order.save()

            except Exception as e:
                print(e)
        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse(data={'SUCEEDED': True})
    



from django.http import HttpResponse
def success_view(request):
    return HttpResponse('Payment is successfully processed.')