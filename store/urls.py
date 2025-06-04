from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('logout/', auth_views.LogoutView.as_view(next_page='store:home'), name='logout'),
]

# Add this to allow logout via GET request
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LogoutView

urlpatterns += [
    path('logout/', csrf_exempt(LogoutView.as_view(next_page='store:home')), name='logout'),
]
