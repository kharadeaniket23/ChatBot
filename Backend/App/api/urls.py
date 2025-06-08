from django.urls import path
from . import views
from .views import product_list
from django.urls import path, include
from .views import chatbot_response , get_conversation_history, register, user_list
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('search/', views.search_products),
    path('chat/', views.save_chat_message),
    path('history/', views.get_chat_history),
    path('products/', product_list),
    path("chat/", chatbot_response),
    path("chat/history/", get_conversation_history),
    path('register/', register),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/users/', user_list),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', views.register),
    path('api/token/', views.AutoCreateTokenView.as_view()),  # token auto-create login
    path('api/chat/', views.chatbot_response),
    path('api/conversation/', views.get_conversation_history),
    path('api/products/', views.product_list),
    path('api/products/search/', views.search_products),


    
]
