from __future__ import unicode_literals
from django.db import models
from ..loginAndRegistration.models import User

class DestinationManager(models.Manager):
    def add_user_to_trip(self,postData):
        flag=False
        errors=[]
        if len(postData['destination'])<1:
            flag=True
            errors.append("Destination cannot be empty!")
        if len(postData['description'])<1:
            flag=True
            errors.append("Description cannot be empty!")
        if postData['datefrom'] < postData['today']:
            flag=True
            errors.append("Travel Date cannot be before today!")
        if postData['dateto']< postData['datefrom']:
            flag=True
            errors.append("End of travel cannot be before the start!")
        # if postData['dateto'].isoformat()>postdata['datefrom'].isoformat():
            # flag=True
            # errors.append("Travel to Date cannot be before Travel From")
        if not flag:
            trip= Destination.objects.create(owner=User.objects.get(id=postData['user']),destination=postData['destination'], description=postData['description'], datefrom=postData['datefrom'], dateto= postData['dateto'])
            Join.objects.create(trip_user=User.objects.get(id=postData['user']), trip_destination=trip)
            return (flag, trip)
        return (flag, errors)

class Destination(models.Model):
    owner= models.ForeignKey(User, related_name="owner")
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    datefrom= models.DateTimeField(max_length=20)
    dateto= models.DateTimeField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= DestinationManager()

class Join(models.Model):
	trip_user= models.ForeignKey(User, related_name="tripuser")
	trip_destination = models.ForeignKey(Destination, related_name="tripdestination")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
