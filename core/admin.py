from django.contrib import admin
from core.models import UserProfile, Company, Product, Listing, Review

admin.site.register(UserProfile)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Listing)
admin.site.register(Review)

