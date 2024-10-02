from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListing, Bids, Comments, WatchList
from .forms import CreateListing



def index(request):
    print(request.user.is_authenticated) # return true if user is logged in

    auction_listings = AuctionListing.objects.all()[::-1]
    return render(request, "auctions/index.html", {
        "listings": auction_listings
    })



@login_required
def new_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            new_list = AuctionListing(
                item_name = form.cleaned_data['item_name'],
                image_url = form.cleaned_data['image_url'],
                category = form.cleaned_data['category'],
                description = form.cleaned_data['description'],
                starting_price = form.cleaned_data['starting_bid'],
                created_by = request.user
                )
            new_list.save()
            return HttpResponseRedirect(reverse("new_listing"))
    
    form = CreateListing
    return render(request, "auctions/new_listing.html", {
        "form": form,
    })



@login_required
def listed_item(request, id):
    item = get_object_or_404(AuctionListing, id=id)
    return render(request, 'auctions/listed_item.html', {
        "item": item
    })



@login_required
def watchlists(request):
    if request.method == "POST":
        auction_item = get_object_or_404(AuctionListing, id=request.POST.get('item_id'))
        add_to = WatchList(user=request.user, auction_item=auction_item)
        add_to.save()
        messages.success(request, "Item added to your watchlist.")

    watchlists = WatchList.objects.filter(user=request.user)
    return render(request, 'auctions/watchlists.html', {
        'watchlists': watchlists
    })


@login_required
def remove_item(request):
    if request.method == "POST":
        auction_item = get_object_or_404(AuctionListing, id=request.POST.get('item_id'))
        watchlist_item = WatchList.objects.filter(user=request.user, auction_item=auction_item).first()
        if watchlist_item:
            watchlist_item.delete()
            messages.success(request, "Item removed from your watchlist.")
        else:
            messages.error(request, "Item not found in your watchlist.")
        return HttpResponseRedirect(reverse("watchlists"))
    


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


