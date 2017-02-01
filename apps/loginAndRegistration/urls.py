from django.conf.urls import url
from views import index, register, login
app_name= "loginAndRegistration"
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^register$', register, name='register'),
    url(r'^login$', login, name='login'),
]
