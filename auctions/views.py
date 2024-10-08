from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, AuctionListing, WatchList, Bids, Comments
from .forms import CreateListing


def index(request):
    auction_listings = AuctionListing.objects.all()[::-1]

    if request.user.is_authenticated:
        if not request.session.get("message_shown", False):
            try:
                item_won = AuctionListing.objects.get(
                    winner=request.user, winner_notified=False
                )
                item_won.winner_notified = True
                item_won.save()
                request.session["message_shown"] = True
                messages.success(
                    request,
                    f"The auction has been closed. You won - {item_won.item_name.upper()} - at the price of ${item_won.current_price}.",
                    extra_tags="success",
                )
            except AuctionListing.DoesNotExist:
                pass

    return render(request, "auctions/index.html", {"listings": auction_listings})


def listed_item(request, id):
    item = get_object_or_404(AuctionListing, id=id)
    item_comments = Comments.objects.filter(commented_item=item)
    return render(
        request,
        "auctions/listed_item.html",
        {
            "item": item,
            "comments": item_comments,
        },
    )


@login_required
def comments(request):
    if request.method == "POST":
        item_commented = get_object_or_404(
            AuctionListing, id=request.POST.get("item_id")
        )
        current_user_comment = request.POST.get("user-comment")
        current_user = get_object_or_404(User, username=request.user)
        db_comments = Comments(
            commented_item=item_commented,
            comment_by=current_user,
            comments=current_user_comment,
        )
        db_comments.save()
        messages.success(request, "Comment posted!", extra_tags="success")
        return redirect("listed_item", id=item_commented.id)


@login_required
def close_bid(request, id):
    closed_item = get_object_or_404(AuctionListing, id=id)
    highest_bid = (
        Bids.objects.filter(auction_item=closed_item).order_by("-bid_amount").first()
    )

    if highest_bid:
        winner = highest_bid.bid_by
        closed_item.winner = winner
        closed_item.active = False
        closed_item.save()
        messages.success(
            request,
            f"The auction has been closed. The winner is {winner.username}.",
            extra_tags="success",
        )
    else:
        messages.error(
            request, "No bids were placed on this item.", extra_tags="danger"
        )

    return redirect("index")


@login_required
def item_deleted(request, id):
    auction_item = AuctionListing.objects.filter(id=id).first()
    auction_item.delete()
    messages.success(request, "Item removed from your watchlist.", extra_tags="success")
    return redirect("index")


@login_required
def my_bid(request):
    if request.method == "POST":
        my_bid = float(request.POST.get("bid-amount"))
        item = get_object_or_404(AuctionListing, id=request.POST.get("item_id"))
        user = get_object_or_404(User, id=request.user.id)
        highest_bid = (
            Bids.objects.filter(auction_item=item).order_by("-bid_amount").first()
        )

        if highest_bid is None:
            highest_bid_amount = 0
        else:
            highest_bid_amount = highest_bid.bid_amount

        if my_bid > item.current_price and my_bid > highest_bid_amount:
            bidding = Bids(auction_item=item, bid_by=user, bid_amount=my_bid)
            bidding.save()
            AuctionListing.objects.filter(id=item.id).update(current_price=my_bid)
            messages.success(request, "Bid request successful!", extra_tags="success")
            return redirect("index")
        else:
            messages.error(
                request,
                "Request Fail! Your bid is equal or less than the current price.",
                extra_tags="danger",
            )
            return redirect("index")


@login_required
def new_listing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)

        if form.is_valid():
            new_list = AuctionListing(
                item_name=form.cleaned_data["item_name"],
                image_url=form.cleaned_data["image_url"],
                category=form.cleaned_data["category"],
                description=form.cleaned_data["description"],
                starting_price=form.cleaned_data["starting_price"],
                created_by=request.user,
            )
            new_list.save()
            return HttpResponseRedirect(reverse("new_listing"))

    form = CreateListing()
    return render(
        request,
        "auctions/new_listing.html",
        {
            "form": form,
        },
    )


@login_required
def watchlists(request):

    if request.method == "POST":
        auction_item = get_object_or_404(AuctionListing, id=request.POST.get("item_id"))
        add_to = WatchList(user=request.user, auction_item=auction_item)
        add_to.save()
        messages.success(request, "Add to watchlists successful!", extra_tags="success")

    watchlists = WatchList.objects.filter(user=request.user)[::-1]
    return render(request, "auctions/watchlists.html", {"watchlists": watchlists})


@login_required
def remove_item(request):
    if request.method == "POST":
        auction_item = get_object_or_404(AuctionListing, id=request.POST.get("item_id"))
        watchlist_item = WatchList.objects.filter(
            user=request.user, auction_item=auction_item
        ).first()

        if watchlist_item:
            watchlist_item.delete()
            messages.success(request, "Item removed from your watchlist.")
        else:
            messages.error(request, "Item not found in your watchlist.")

        return HttpResponseRedirect(reverse("watchlists"))


@login_required
def categories(request):
    category = request.GET.get("category")
    categories = AuctionListing.objects.filter(category=category)

    return render(
        request,
        "auctions/categories.html",
        {
            "categories": categories,
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
