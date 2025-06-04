from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
import stripe

stripe.api_key = 'your_stripe_secret_key_here'  # Replace with your Stripe secret key

def home(request):
    return render(request, 'store/home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart_detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('store:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('store:cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        try:
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(cart.total_price() * 100),  # amount in cents
                currency='usd',
                metadata={'user_id': request.user.id}
            )
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                total_amount=cart.total_price(),
                payment_intent_id=intent['id'],
                status='pending'
            )
            return JsonResponse({'clientSecret': intent['client_secret']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return render(request, 'store/checkout.html', {'cart': cart, 'stripe_public_key': 'your_stripe_public_key_here'})

@login_required
def payment_success(request):
    return render(request, 'store/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')
