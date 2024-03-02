from fileinput import filename
import http
from pickle import NONE
from pickletools import read_uint1
from urllib.request import Request
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import date, datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import Venueform , Eventform , EventformAdmin
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.http import HttpResponse
import csv
#for pdf
from django.http import FileResponse
import io
#import pagination stuff
from django.core.paginator import Paginator
from django.contrib import messages


#show Event
def show_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    return render(request,"pages/show_event.html",{"event":event})



def venue_events(requeset,venue_id):

    #Grab the venue
    venue = Venue.objects.get(id=venue_id)
    #Grab the events from that venue
    events = venue.event_set.all()
    if events:
        return render (requeset,"pages/venue_events.html",{"events":events})
    else:
         messages.success(requeset,("That Venue Has No Events At This Time"))
         return redirect("admin_approval")





#create Admin Event Approval Page

def admin_approval(request):
    venue_list = Venue.objects.all()


    #get count 
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count  = User.objects.all().count()

    event_list = Event.objects.all().order_by("-event_date")
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist("boxes")

            #unchek all events
            event_list.update(approved=False)
            #update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request,("Event List Approval Has Been Updated."))
            return redirect("events")


        else:

            return render(request,"pages/admin_approval.html", {
            "event_list":event_list,
            "event_count":event_count,
            "venue_count":venue_count,
            "user_count":user_count,
            "venue_list":venue_list})

    else:
        messages.success(request,("You arent authorized to view this page !"))
        return redirect("home")










#create my events page


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request,"pages/my_events.html",{"events":events})
    else:
        messages.success(request,("You Arent Authorized To View This Page"))
        return redirect("home")



#generate a PDF file venue list



def venue_pdf(request):
    buf = io.BytesIO()
    # create a canves
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    #Add some lines
    #lines = [
        #"THis is line 1"
       #"THis is line 2"
    #]

    #Designate The Model 
    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_a)
        lines.append("====================")


    
    for line in lines:
        textob.textLine(line)


    #finish up
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #return 

    return FileResponse(buf , as_attachment=True, filename="venue.pdf")






def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename= venues.csv"
    #creat a csv writer
    writer = csv.writer(response)


    #Designate The Model 
    venues = Venue.objects.all()

    #add column headings to the ccsv file
    writer.writerow(["Venue Name","Address", "zip code ", "Phone", "Web Address ", "Email"])

    #loop
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_a])
         
    return response




def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename= venues.txt"
    #Designate The Model 
    venues = Venue.objects.all()

    lines = []
    for venue in venues:
        lines.append(f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_a}\n\n\n")
         

    #lines = ["This is line 1 \n",
    #"This is line 2 \n",
    #"This is line 3 \n"]

    #Write to the text box
    response.writelines(lines)
    return response

# Create your views here.

def delete_venue(request,venue_id):
    venue= Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list_venues")






def delete_event(request,event_id):
    event= Event.objects.get(pk=event_id)
    if request.user ==event.manager:
        event.delete()
        messages.success(request,("Event Deleted!!!"))
        return redirect("events")

    else:
        messages.success(request,("You arent't Authorized To Delete This Event.."))
        return redirect("events")



def update_event(request, event_id):
    event= Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventformAdmin(request.POST or None, instance=event)
    else:
        form = Eventform(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect("events")

    return render(request,"pages/update_event.html",
        {"event": event ,
         "form":form,})







def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:

            form = EventformAdmin(request.POST)
            if form.is_valid():
                form.save()
                return  HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = Eventform(request.POST)
            if form.is_valid():

                event = form.save(commit=False)
                event.manager = request.user # logged in user
                event.save()
                return  HttpResponseRedirect("/add_event?submitted=True")

      
    else:
        if request.user.is_superuser:
            form = EventformAdmin

        else:
            form = Eventform

        if "submitted" in request.GET:
            submitted = True


    return render(request,"pages/add_event.html",{"form":form,"submitted":submitted})







def update_venue(request, venue_id):
    venue= Venue.objects.get(pk=venue_id)
    form = Venueform(request.POST or None,request.FILES or None , instance=venue)
    if form.is_valid():
        form.save()
        return redirect("list_venues")

    return render(request,"pages/update_venue.html",
        {"venue": venue ,
         "form":form,})






def search_venues(request):
    
    if request.method == "GET":
        searched = request.GET.get("searched")
        venues  = Venue.objects.filter(name__contains = searched )

        return render(request,"pages/search_venues.html",
        {"searched":searched,
         "venues":venues,})


    else:
         return render(request,"pages/search_venues.html",
            {})







def show_venue(request,venue_id):
    venue= Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    #Grab the events from that venue
    events = venue.event_set.all()

    return render(request,"pages/show_venue.html",
        {"venue": venue,
         "venue_owner":venue_owner,
         "events":events })


 

def list_venues(request):
     venue_list = Venue.objects.all()

     #set pagination
     p = Paginator(Venue.objects.all(),3)
     page = request.GET.get("page")
     venues = p.get_page(page)
     nums = "a" *venues.paginator.num_pages


     return render(request,"pages/venue.html",
        {"venue_list": venue_list,
        "venues":venues ,
        "nums":nums})





def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = Venueform(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # logged in user
            venue.save()
            return  HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = Venueform
        if "submitted" in request.GET:
            submitted = True


    form = Venueform
    return render(request,"pages/add_venue.html",{"form":form,"submitted":submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request,"pages\event_list.html",
        {"event_list": event_list, })
    




def home(request,year= datetime.now().year,month=datetime.now().strftime("%B")):
    name = "sepehr"
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year,month_number)
    now = datetime.now()
    current_year = now.year
    time = now.strftime("%H:%M:%S:%p")
    event_list = Event.objects.filter(
    event_date__year = year,
    event_date__month = month_number)


    return render (request,
    "pages\home.html",{
    "first_name":name,
    "year":year,
    "month":month,
    "month_number":month_number,
    "cal":cal,
    "current_year":current_year, 
    "time":time,
    "event_list":event_list})