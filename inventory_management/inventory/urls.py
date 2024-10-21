from django.urls import path
from .views import ItemView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('items/', ItemView.as_view(), name='items'),
    path('items/<int:item_id>/', ItemView.as_view(), name='item-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]