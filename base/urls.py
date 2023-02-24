from django.urls import path

from . import views 

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login_view,name="login"),
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logout_view,name="logout"),
    path('verification/',views.verification,name="verification"),
    path('physical-key-authentication/',views.physical_key_authentication),
    path('check-authentication/',views.check_authentication),
]
