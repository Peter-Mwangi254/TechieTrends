from django.urls import path, include
from .mpesa import mpesa_callback, create_order
from rest_framework import routers
from .views import (UserDetailsViewSet, VendorViewSet, CategoryViewSet, ProductViewSet,
    OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet, ShippingViewSet,
    PaymentViewSet, CouponViewSet, ReviewViewSet, WishlistViewSet, NotificationViewSet,
    BlogViewSet, ContactViewSet, FAQViewSet, AnalyticsViewSet, ConfigurationsViewSet,
    TaxViewSet, SubscriptionViewSet, RefundViewSet,
    LoginView, LogoutView, SignupView, ActivateAccountView)


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
# router.register(r'payment-gateway-credentials', PaymentGatewayCredentialsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('create-order/', create_order, name='create_order'),
    path('mpesa-callback', mpesa_callback, name='mpesa-calback'),
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('api/auth/user', UserDetailsViewSet.as_view(), name='user-details'),
]