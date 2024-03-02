from email.headerregistry import Group
from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event
from django.contrib.auth.models import Group
# Register your models here.

#admin.site.register(Venue)
admin.site.register(MyClubUser)

#Remove Grouos
admin.site.unregister(Group)


#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display=("name","address","phone")
    ordering = ("name",)
    search_fields = ("name","address")
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name","venue"), "event_date", "decription","manager", "approved")
    list_display = ("name" , "event_date",)
    list_filter = ("event_date","venue")
    ordering = ("event_date",)