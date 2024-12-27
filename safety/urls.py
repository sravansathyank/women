from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('quote_page/', views.quote_page, name='quote_page'),
    path('file_complaint/', views.file_complaint, name='file_complaint'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('resources/', views.empowerment_resources, name='empowerment_resources'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('resolve_complaint/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('councelling/', views.councelling, name='councelling'),
    path('job_oppurtunity/', views.job_oppurtunity, name='job_oppurtunity'),
    path('sell_product/', views.sell_product, name='sell_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
