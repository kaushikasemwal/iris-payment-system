import stripe

stripe.api_key = "your_secret_key"

def process_payment(customer_id, amount):
    """Charges a Stripe customer."""
    charge = stripe.PaymentIntent.create(
        customer=customer_id,
        amount=amount * 100,  # Convert to cents
        currency="usd",
        payment_method_types=["card"]
    )
    return charge
