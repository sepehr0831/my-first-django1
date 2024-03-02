from dataclasses import fields
from socket import fromshare
from tkinter import Widget
from django import forms
from django.forms import ModelForm
from .models import Venue , Event

#create a venue form

class Venueform(ModelForm):
    class Meta:
        model = Venue
        fields= ("name","address","zip_code", "phone", "web", "email_a","venue_image",)
        labels={
            "name":'',
            "address":'',
            "zip_code":'',
            "phone":'',
            "web":'',
            "email_a":'',
            "venue_image":'',}

        widgets = {
            "name":forms.TextInput(attrs={"class": "form-control", "placeholder":"name"}),
            "address":forms.TextInput(attrs={"class":"form-control", "placeholder":"Address"}),
            "zip_code":forms.TextInput(attrs={"class":"form-control", "placeholder":"Zip Code"}),
            "phone":forms.TextInput(attrs={"class":"form-control", "placeholder":"Phone"}),
            "web":forms.TextInput(attrs={"class":"form-control", "placeholder":"Web Address"}),
            "email_a":forms.EmailInput(attrs={"class":"form-control", "placeholder":"Email"}),
                       }

#User Event Form
class Eventform(ModelForm):
    class Meta:
        model = Event
        fields= ("name","event_date","venue", "attendees", "decription")
        labels={
            "name":'',
            "event_date":'YYYY-MM-DD HH:MM:SS',
            "venue":'Venue',
            "attendees":'Attendees',
            "decription":'',}
        widgets = {
            "name":forms.TextInput(attrs={"class": "form-control", "placeholder":" Event name"}),
            "event_date":forms.TextInput(attrs={"class":"form-control", "placeholder":"Event Date"}),
            "venue":forms.Select(attrs={"class":"form-select", "placeholder":"Venue"}),
            "attendees":forms.SelectMultiple(attrs={"class":"form-control", "placeholder":"attendees"}),
            "decription":forms.Textarea(attrs={"class":"form-control", "placeholder":"decription"}),
                       }




# Admin SUPERUSER Event Form
class EventformAdmin(ModelForm):
    class Meta:
        model = Event
        fields= ("name","event_date","venue", "manager", "attendees", "decription")
        labels={
            "name":'',
            "event_date":'YYYY-MM-DD HH:MM:SS',
            "venue":'Venue',
            "manager":'Manager',
            "attendees":'Attendees',
            "decription":'',}
        widgets = {
            "name":forms.TextInput(attrs={"class": "form-control", "placeholder":" Event name"}),
            "event_date":forms.TextInput(attrs={"class":"form-control", "placeholder":"Event Date"}),
            "venue":forms.Select(attrs={"class":"form-select", "placeholder":"Venue"}),
            "manager":forms.Select(attrs={"class":"form-select", "placeholder":"Manager"}),
            "attendees":forms.SelectMultiple(attrs={"class":"form-control", "placeholder":"attendees"}),
            "decription":forms.Textarea(attrs={"class":"form-control", "placeholder":"decription"}),
                       }                       