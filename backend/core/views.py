from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .serializers import UserSerializer
from .tokens import account_activation_token
from .models import User

from .models import (User, Vendor, Category, Product, Order, OrderItem, Cart,
    CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog,
    Contact, FAQ, Analytics, Configurations, Tax, Subscription, Refund)

from .serializers import (UserSerializer, VendorSerializer, CategorySerializer,
    ProductSerializer, OrderSerializer, OrderItemSerializer, CartSerializer,
    CartItemSerializer, ShippingSerializer, PaymentSerializer, CouponSerializer,
    ReviewSerializer, WishlistSerializer, NotificationSerializer, BlogSerializer,
    ContactSerializer, FAQSerializer, AnalyticsSerializer, ConfigurationsSerializer,
    TaxSerializer, SubscriptionSerializer, RefundSerializer)


# Authentication views

class SignupView(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')
        is_vendor = request.data.get('is_vendor', False)

        if not email or not name or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email=email, name=name, password=password, is_vendor=is_vendor)
            user.is_vendor = is_vendor
            user.save()
            user.send_activation_email(request)
            return Response({'message': 'User created successfully. Please confirm your email address to complete the registration'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is not activated. Please check your email'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Thank you for your email confirmation. Now you can login to your account.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)



class UserDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # queryset = User.objects.all()
    # serializer_class = UserSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'  

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer

class ConfigurationsViewSet(viewsets.ModelViewSet):
    queryset = Configurations.objects.all()
    serializer_class = ConfigurationsSerializer

class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
                                                                                        