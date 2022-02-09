"""Shopify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Shop.views import *
from . import views


urlpatterns = [
    path('',views.Home),
    path('login',views.Login.as_view(),name='login'),
    path('register',views.Register.as_view(),name='register'),
    # path('product',views.Product.as_view(),name='product'),
    path('add',views.Addproduct.as_view(),name='add'),
    path('show',views.Show,name='show'),
    path('remove_from_cart',views.Remove_from_cart.as_view(),name='remove_from_cart'),
    path('update/<int:id>',views.upd,name='update'),
    path('logout',views.LogoutView.as_view(),name="logout"),
    # path('add-to-cart',views.AddToCart.as_view(),name="add_to_cart"),
    path('addtocart',views.AddToCart.as_view(),name='addtocart'),
    path('payment',views.Payment.as_view(),name="payment"),
    path('showproduct',views.Showproduct.as_view(),name="showproduct"),
    # path('charge',views.Charge,name='charge'),
    # path('create-checkout-session', views.create_checkout_session),
    # path('success/', views.SuccessView.as_view()), 
    # path('cancelled/', views.CancelledView.as_view()),
    # path('stripetest',views.stripetest,name='stripetest')


   
]
