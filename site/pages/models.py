import email
from email.policy import default
from hashlib import blake2b
import imp
from operator import mod
from pyexpat import model
from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField("venue name" ,max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField(max_length=19,blank=True)
    phone =models.CharField("Contact Phone", max_length=28,blank=True)
    web = models.URLField("Website Address",blank=True)
    email_a = models.EmailField("Email address",blank=True)
    owner = models.IntegerField("vneue Owner",blank=False , default=1)
    venue_image = models.ImageField(null= True , blank=True, upload_to = "images")
    
    def __str__(self) :
        return self.name




class MyClubUser(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=120)
    email = models.EmailField("User email")

    def __str__(self) -> str:
        return self.first_name+ "  " + self.last_name




# Create your models here.
class Event(models.Model):
     name = models.CharField("Event name", max_length=120)
     event_date=models.DateTimeField("Event date")
     venue = models.ForeignKey(Venue, blank=True , null=True, on_delete=models.CASCADE)
     #venue = models.CharField(max_length=120)
     manager = models.ForeignKey(User,blank=True,null=True, on_delete=models.SET_NULL)
     decription =models.TextField(blank=True)
     attendees = models.ManyToManyField(MyClubUser, blank=True,)
     approved = models.BooleanField("Approved", default= False)




     def __str__(self):
        return self.name

     @property
     def Days_till(self):
         today = date.today()
         days_till = self.event_date.date() - today
         days_till_stripped = str(days_till).split(",",1)[0]
         return days_till_stripped

     @property
     def Is_Past(self):
        today = date.today()
        if self.event_date.date() < today :
            thing = "Past"
        else:
            thing = "Future"
        return thing


    