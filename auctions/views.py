from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max

from .models import User, Listing, Bid, Comment, Category, Watchlist
from .forms import ListingForm, BidForm, CommentForm

from .utils import get_watchlist_count


def index(request):
    listings = Listing.objects.all()
    watchlist_count = get_watchlist_count(request.user)

    context = {'listings': listings,
               "watchlist_count": watchlist_count,}
    return render(request, 'auctions/index.html', context=context)


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


@login_required
def create_listing_view(request):

    watchlist_count = get_watchlist_count(request.user)
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            print(form)
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('index')

    context = {
        "form": form,
        "watchlist_count": watchlist_count,
    }
    return render(request, 'auctions/create_listing.html', context=context)


def show_listing_view(request, listing_id):

    watchlist_count = get_watchlist_count(request.user)
    bid_form = BidForm()
    comment_form = CommentForm()
    listing = get_object_or_404(Listing, pk=listing_id)

    is_creator_of_listing = False
    is_auction_winner = False
    if listing.user.id == request.user.id:
        is_creator_of_listing = True

    if not listing.is_active and request.user.is_authenticated:
        bids_on_this_listing = Bid.objects.filter(
            user=request.user, listing=listing)
        max_bid_obj = bids_on_this_listing.order_by('-value').first()
        if max_bid_obj:
            if listing.start_bid == max_bid_obj.value:
                is_auction_winner = True

    comments = Comment.objects.filter(listing=listing).order_by('created')

    context = {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "is_creator_of_listing": is_creator_of_listing,
        "is_auction_winner": is_auction_winner,
        "comments": comments,
        "watchlist_count": watchlist_count,
    }

    return render(request, 'auctions/show_listing.html', context=context)


@login_required
def show_watchlist_view(request):
    watchlist = None
    watchlist_count = get_watchlist_count(request.user)

    if not request.user.is_anonymous:
        try:
            watchlist = Watchlist.objects.filter(
                user=request.user
            )
        except:
            print("Invalid user to get watchlist")

    context = {
        "watchlist": watchlist,
        "watchlist_count": watchlist_count,
    }
    return render(request, "auctions/show_watchlist.html", context=context)


@login_required
def remove_from_watchlist_view(request, watchlist_item_id):

    if not request.user.is_anonymous:
        item = get_object_or_404(Watchlist, pk=watchlist_item_id)
        item.delete()
        messages.success(request, "Item removed from watchlist...")

    context = {}
    return redirect('show_watchlist')


@login_required
def add_to_watchlist_view(request, listing_item_id):

    if not request.user.is_anonymous:
        listing = get_object_or_404(Listing, pk=listing_item_id)

        if not Watchlist.objects.filter(listing=listing, user=request.user):
            watchlist_item = Watchlist(user=request.user, listing=listing)
            watchlist_item.save()
            msg = 'Item added successfully to watchlist...'
        else:
            msg = "Item already present in watchlist..."

        messages.success(request, msg)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_bid_to_listing_view(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)
    current_bid = listing.start_bid

    form = BidForm(request.POST)
    if form.is_valid():
        new_bid = form.cleaned_data['current_bid']
        user = request.user

        if new_bid > current_bid:
            bid_obj = Bid(value=new_bid, user=user, listing=listing)
            bid_obj.save()
            listing.start_bid = new_bid
            listing.save()
        else:
            messages.error(
                request, "Bid should be larger than recent price: {}".format(current_bid))

    context = {}
    return redirect("show_listing", listing_id=listing_id)


@login_required
def add_comment_to_listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.cleaned_data['comment']
        user = request.user

        cmt_obj = Comment(content=new_comment, user=user, listing=listing)
        cmt_obj.save()

    context = {}
    return redirect("show_listing", listing_id=listing_id)


@login_required
def close_auction_view(request, listing_id):
    if request.user.is_authenticated:
        listing_obj = get_object_or_404(Listing, pk=listing_id)
        if listing_obj.user.id == request.user.id:
            listing_obj.is_active = False
            listing_obj.save()

    context = {}
    return redirect("show_listing", listing_id=listing_id)


def show_categories_view(request):
    watchlist_count = get_watchlist_count(request.user)

    categories = Category.objects.all()

    context = {
        "categories": categories,
        "watchlist_count": watchlist_count,
    }
    return render(request, "auctions/show_categories.html", context=context)


def show_category_items_view(request, category_id):
    watchlist_count = get_watchlist_count(request.user)

    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category)

    context = {
        "listings": listings,
        "category": category.content,
        "watchlist_count": watchlist_count,
    }
    return render(request, "auctions/show_category_items.html", context=context)
