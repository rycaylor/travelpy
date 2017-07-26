# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User
from dateutil.parser import parse
from datetime import datetime
# Create your models here.

class TripManager(models.Manager):
    def plan_make(self, postData, user):
        logged = User.objects.get(id=user)
        results = {'create':True, 'error': [], 'plan':None}
        if postData['destination'] == '':
            results['create'] = False
            results['error'].append('Please enter a destination for your trip')
            #checking to make sure that the destination is not blank returns an error telling the user to satisfiy this field
        else:
            destination = postData['destination']

        if postData['description'] == '':
            results['create'] = False
            results['error'].append('Please enter a description so we know whats going to take place')
            #checking to make sure that the description is not blank returns an error telling the user to satisfiy this field
        else:
            description = postData['description']

        if postData['date_start'] == '':
            results['create'] = False
            results['error'].append('Please enter a starting date')
            #checks to make sure that the starting date is not blanks and returns an error telling the user to satisfiy this field
        else:
            date_start = datetime.strptime(postData['date_start'], '%Y-%m-%d').date()
            #formatting my datetime field to only show the year months and date
        if postData['date_end'] == '':
            results['create'] = False
            results['error'].append('Please enter an ending date')
            #checks to make sure that my ending date is not blank and returns an erorr telling the user to satisfiy this field
        else:
            date_end = datetime.strptime(postData['date_end'], '%Y-%m-%d').date()
            #formatting my datetime again to show year months and day
        try:
            if date_start < datetime.now().date():
                results['create'] = False
                results['error'].append('Start date cannot occur before todays date')
                #checks to see if the entered date is before the current date returning an error to the user telling them to fix this error
            if date_end < date_start:
                results['create'] = False
                results['error'].append('End date cannot not occur before start date')
                #checks to see if the ending date is before the starting date returning an error to the user telling them to fix this eror
        except:
            pass

        if results['create']:
            #if my trip passes the above validations the create value should be true passing it to my create function
            planned_trip = Trip.objects.create(destination=destination, description=description, date_start=date_start, date_end=date_end, maker=logged)

            planned_trip.save()
            results['plan'] = planned_trip
        return results


    def join_trip(self, user, trip):
        plan = Trip.objects.get(id=trip)
        joiner = User.objects.get(id=user)
        #this function grabs the current selected trip and whoever is logged in and adds them to the ManyToManyField of trips

        plan.joining.add(joiner)

        plan.save()

        return plan





class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    date_start = models.DateField()
    date_end = models.DateField()
    maker = models.ForeignKey(User, related_name='maker')
    joining = models.ManyToManyField(User, related_name='joning')
    objects = TripManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
