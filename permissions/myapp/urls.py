from django.urls import path
from .views import ItemList, ItemDetail,StaffDetail, MyProtectedView,AllowanyView,IsAdminView,CreateUserView
#PostDetailView,PostCreate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
    path('staff-details/', StaffDetail.as_view(), name='staff-detail'),
    path('protected/', MyProtectedView.as_view(), name='protected-view'),
    path('allowany/', AllowanyView.as_view(), name='allowany-view'),
    path('adminview/', IsAdminView.as_view(), name='adminview-view'),

    
]

#path('posts/', PostCreate.as_view(), name='post-create'),
#path('post/<int:pk>/', PostDetailView.as_view(), name='blogpost_detail'),