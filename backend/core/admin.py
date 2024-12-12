from django.contrib import admin
from .models import (User, Vendor, Category, Product, Order, OrderItem, Cart,
    CartItem, Shipping, Payment, Coupon, Review, Wishlist, Notification, Blog,
    Contact, FAQ, Analytics, Configurations, Tax, Subscription, Refund)


admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Shipping)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Notification)
admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(FAQ)
admin.site.register(Analytics)
admin.site.register(Configurations)
admin.site.register(Tax)
admin.site.register(Subscription)
admin.site.register(Refund)