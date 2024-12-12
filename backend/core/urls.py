from django.urls import path, include
from .mpesa import mpesa_callback, create_order
from rest_framework import routers
from .views import (UserViewSet, VendorViewSet, CategoryViewSet, ProductViewSet,
    OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet, ShippingViewSet,
    PaymentViewSet, CouponViewSet, ReviewViewSet, WishlistViewSet, NotificationViewSet,
    BlogViewSet, ContactViewSet, FAQViewSet, AnalyticsViewSet, ConfigurationsViewSet,
    TaxViewSet, SubscriptionViewSet, RefundViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cartitems', CartItemViewSet)
router.register(r'shippings', ShippingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'coupons', CouponViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'faqs', FAQViewSet)
router.register(r'analytics', AnalyticsViewSet)
router.register(r'configurations', ConfigurationsViewSet)
router.register(r'taxes', TaxViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'refunds', RefundViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('create-order/', create_order, name='create_order'),
    path('mpesa-callback', mpesa_callback, name='mpesa-calback'),
]