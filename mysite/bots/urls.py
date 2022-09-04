from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.bot_list, name='bot_list'),
    path('<str:name>', views.bot_detail, name='bot_detail'),
    path('listing/<str:bot>',views.listing, name='listing'),
    # path('pay/result/', views.pay_result), 
    # path('pay/update_order/', views.update_order),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)