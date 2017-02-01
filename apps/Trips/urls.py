from django.conf.urls import url
from views import dashboard, addTrip, destination, join, logout
app_name= "trips"
urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
    url(r'^addTrip$', addTrip, name='addTrip'),
    url(r'^destination/(?P<id>\d+)/(?P<owner_id>\d+)$', destination, name='destination'),
    url(r'^join/(?P<id>\d+)$', join, name='join'),
    url(r'^logout$', logout, name='logout')
]
