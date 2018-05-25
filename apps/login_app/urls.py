from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log_reg', views.log_reg, name='log_reg'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_post', views.add_post, name='add_post'),
    path('show/<post_id>', views.show, name='show'),
    path('logout', views.logout, name='logout'),
    path('reply/<post_id>', views.reply, name='reply'),
    path('profile/<id>', views.profile, name='profile'),
    #path('fb_login', views.fb_login, name='fb_login')
]
