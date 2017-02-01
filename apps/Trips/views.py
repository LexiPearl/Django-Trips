from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.core.urlresolvers import reverse
from ..loginAndRegistration.models import User
from .models import Destination, Join

def dashboard(request):
    variable=Join.objects.filter(trip_user_id=request.session['user_id'])
    second= Destination.objects.exclude(owner_id=request.session['user_id'])
    for x in variable:
        second=second.exclude(id=x.trip_destination.id)
    third=Destination.objects.filter(owner_id=request.session['user_id'])
    context={
        "destinations": variable,
        "trip_users": second,
        "owner_id": third
    }
    print third
    return render(request, "Trips/dashboard.html",context)

def addTrip(request):
    if request.method=="GET":
        return render(request, 'Trips/addTrip.html')
    if request.method=="POST":
        today=datetime.now()
        datefrom=datetime.strptime(request.POST['datefrom'], '%Y-%m-%d')
        dateto= datetime.strptime(request.POST['dateto'], '%Y-%m-%d')
        postData={
            "user":request.session['user_id'],
            "destination": request.POST['destination'],
            "description": request.POST['description'],
            "datefrom": datefrom,
            "dateto": dateto,
            "today": today,
        }
        results=Destination.objects.add_user_to_trip(postData)
        if results[0]:
            for err in results[1]:
                messages.error(request,err)
            return render(request, 'Trips/addTrip.html')
        return redirect(reverse('Trips:dashboard'))

def destination(request, id, owner_id):
    variable=Join.objects.exclude(trip_user_id=owner_id)
    second=Join.objects.filter(trip_destination_id=id)
    print variable
    print second
    # for x in variable:
        # second=second.exclude()
    context={
        "destinations": Destination.objects.get(id=id),
        "trip_users": second
    }
    return render(request, "Trips/destination.html", context)

def join(request, id):
    user= User.objects.get(id=request.session['user_id'])
    destination=Destination.objects.get(id=id)
    Join.objects.create (trip_user=user, trip_destination=destination)
    print
    return redirect(reverse('Trips:dashboard'))

def logout(request):
    request.session.pop('user_id')
    request.session.pop('name')
    return redirect(reverse("loginAndRegistration:index"))
