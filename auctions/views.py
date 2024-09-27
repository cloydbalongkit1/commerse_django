from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bids, Comments
from .forms import CreateListing



def index(request):
    auction_listing = AuctionListing.objects.all()
    print(auction_listing)
    return render(request, "auctions/index.html", {
        "items": auction_listing
    })



def new_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            print(form.cleaned_data["title"])
            print(form.cleaned_data["image_url"])
            print(form.cleaned_data["starting_bid"])
            print(form.cleaned_data["category"])
            print(form.cleaned_data["description"])
            print(form.cleaned_data["image_url"])
            
            return HttpResponseRedirect(reverse("new_listing"))

    form = CreateListing
    return render(request, "auctions/new_listing.html", {
        "form": form,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


