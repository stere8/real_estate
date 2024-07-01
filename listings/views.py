# views.py in listings app
import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from enums import ListingStatus, OrderStatus
from orders.models import Order
from .models import Listing, User
from .forms import ListingForm
from django.core.paginator import Paginator
from django.db.models import Q


def listing_list(request):
    listings_list = Listing.objects.all()  # Replace with your queryset
    p = Paginator(listings_list, 9)  # Set the number of listings per page

    page = request.GET.get('page')
    listings = p.get_page(page)
    first_group = listings[:3]  # First three listings
    second_group = listings[3:]  # Last three listings

    groups = [first_group, second_group]
    context = {'groups': groups}
    return render(request, 'listings/listing_list.html', context)


def listing_search(request):
    search_term = request.GET.get('q', '')
    filtered_listings = Listing.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term)
    )  # Search by title and description

    paginator = Paginator(filtered_listings, 6)  # Set the number of listings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    first_group = page_obj[:3]  # First three listings
    second_group = page_obj[3:]  # Last three listings

    context = {'first_group': first_group,
               'second_group': second_group, 'listings': page_obj, 'is_paginated': page_obj.has_other_pages(),
               'is_from_search': True,
               'search_term': search_term}
    return render(request, 'listings/listing_list.html', context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    users = User.objects.all() if request.user.is_superuser else None
    listing_reservations = Order.objects.filter(listing=pk).values_list('reservation_date', flat=True)
    reserved_dates = json.dumps(list(listing_reservations), cls=DjangoJSONEncoder)

    context = {
        'listing': listing,
        'users': users,
        'reserved_dates': reserved_dates,
    }

    return render(request, 'listings/listing_detail.html', context)


def listing_create(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success.html', {'action': 'Listing Created'})
    return render(request, 'listings/listing_create.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method == "POST":
        data = request.POST
        listing.title = data.get('title')
        listing.description = data.get('description')
        listing.price = data.get('price')
        listing.available = (data.get('available') == "on")
        print(data.get('main_img'))
        if request.FILES:
            new_main_img = request.FILES['main_img']

            # Delete the previous image (if it exists)
            if listing.main_img:
                listing.main_img.delete(save=False)  # Avoid saving the model again
            listing.main_img = new_main_img
        listing.save()
        return redirect('success')
    return render(request, 'listings/listing_edit.html', {'listing': listing, 'pk': pk})


def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        if listing.main_img:
            print(listing.main_img.name)
            if listing.main_img.name != 'images/no_image.jpeg':
                listing.main_img.delete()
        listing.delete()
        return HttpResponse("Listing successfully deleted")
    return render(request, 'listings/listing_confirm_delete.html', {'listing': listing})


@login_required
def reserve_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser:
            user_id = request.POST.get('reserve_user')
            user = get_object_or_404(User, pk=user_id)
        else:
            user = request.user
        listing.reserved_by_id = user.id
        listing.available = False
        listing.status = ListingStatus.PENDING
        listing.save()

        order = Order(user_id=user.id, listing_id=listing.id, date_ordered=datetime.datetime.now(),
                      status=OrderStatus.PENDING)
        order.save()
        return redirect('listing_detail', pk=listing.pk)
    return redirect('listing_detail', pk=listing.pk)
