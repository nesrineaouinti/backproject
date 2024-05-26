from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.conf import settings
# from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", RegisterUserView.as_view(), name="register"),  #we add as_view() when its class based view
    path("api/user/get/", GetUserView.as_view(), name="get_user"),
    path("api/user/update/", UpdateUserView.as_view(), name="update-user"),
    path("api/user/view/", RegisterUserView.as_view(), name="get_user"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/",include("api.urls")),
    path("api/checkifadmin/",CheckIfAdminWithRecievedAccessTokenView.as_view(), name="checkifAdmin"),

#addedotp' 
    path('api/user/confirm/<str:email>/', ConfirmUserView.as_view(), name='confirm'),
    path('api/user/sendcode/<str:email>/', SendConfirmationCodeView.as_view(), name='send-resend-code'),
    path('api/user/verifycode/', VerifyCodeView.as_view(), name='verify-code'),
    path('api/user/changepassword/', ResetPasswordView.as_view(), name='change-reset-password'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   