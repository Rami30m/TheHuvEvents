from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='admin-panel'),
    path('delete/', views.DeleteEvent, name='DeleteEvent'),
    path('login/', auth_views.LoginView.as_view(template_name="panel/login.html"), name='login'),
    path('lists', views.lists, name='lists'),
    path('customers/<int:event_id>/', views.ShowCustomers, name='ShowCustomers'),
    path('logout', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    path('customers/<int:event_id>/<int:customer_id>/', views.change_status, name='change_status'),
]