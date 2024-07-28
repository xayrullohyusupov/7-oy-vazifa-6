from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.myCart, name='my_cart'),
    path('add/', views.addProductToCart, name='add_product_to_cart'),
    path('substract/', views.substractProductFromCart, name='substract_product_from_cart'),
    path('delete/', views.deleteProductCart, name='delete_product_cart'),
    path('create_order/', views.CreateOrder, name='create_order'),
]
