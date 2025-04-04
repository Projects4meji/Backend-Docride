import stripe
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY

# Stripe PRICE IDs (use actual IDs from your dashboard)
PRICE_IDS = {
    'test_drive': 'price_1R3xUXEYQxHtXYU4vBEZYXLM',  # FREE trial for 1 month
    'budget': 'price_1R3xVZEYQxHtXYU4HBFgPNYY',
    'standard': 'price_1R3xdeEYQxHtXYU4f3AjqYoe',
    'economy': 'price_1R3xe2EYQxHtXYU4re4DW9FC',
}

@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutView(APIView):
    def post(self, request):
        print("Received POST data:", request.data)
        plan_type = request.data.get('plan')
        price_id = PRICE_IDS.get(plan_type)

        if not price_id:
            return Response({'error': 'Invalid plan type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Set mode to 'subscription' for all plans
            session_data = {
                'ui_mode': 'embedded',
                'line_items': [{'price': price_id, 'quantity': 1}],
                'mode': 'subscription',
                'return_url': f"{settings.SITE_URL}/?session_id={{CHECKOUT_SESSION_ID}}",
            }

            # ✅ For Test Drive, optionally apply trial (if not already configured in Stripe)
            if plan_type == 'test_drive':
                session_data['subscription_data'] = {
                    'trial_period_days': 30  # 1 month free
                }

            session = stripe.checkout.Session.create(**session_data)

            return Response({'clientSecret': session.client_secret}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Stripe Error:", e)  # Add this line
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home(request):
    return HttpResponse("Welcome to the homepage!")