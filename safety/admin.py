from django.contrib import admin
from .models import Complaint, EmpowermentResource
from django.contrib import admin
from .models import Product

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description', 'status')
    list_filter = ('status',)
    search_fields = ('description', 'user__username')

@admin.register(EmpowermentResource)
class EmpowermentResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'link')
    search_fields = ('title', 'description')




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'contact')
    search_fields = ('name', 'description', 'contact')



