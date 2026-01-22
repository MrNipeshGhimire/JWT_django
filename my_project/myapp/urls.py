from django.urls import path
from .views import register_view,login_view, blog_view,blog_view_detail

urlpatterns = [
    path('register/',register_view),
    path('login/',login_view),
    path('blog/',blog_view),
    path('blog/<int:id>/',blog_view_detail)

]
