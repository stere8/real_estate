# accounts/views.py
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from listings.models import Listing
from orders.models import Order
from django.contrib.auth import views as auth_views, logout as auth_logout
from django.db.models import Q
from .models import User
from django.contrib.auth import login



def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser, login_url='listing_list')(view_func)
    return decorated_view_func


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        # Basic validation (you can add more as needed)
        if not username or not first_name or not last_name or not email or not password or not password_repeat:
            # Handle missing fields
            return render(request, 'accounts/signup.html', {'error': 'All fields are required'})
        if password != password_repeat:
            # Handle password mismatch
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})

        # Create a new user object
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Log in the newly created user (optional)
        login(request, user)  # Comment out if not immediately logging in

        return redirect('login')  # Redirect to the login page (or another page)
    else:
        # Empty form for GET requests
        return render(request, 'accounts/signup.html')


class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/signin.html'
    next_page = 'listing_list'  # Redirect to 'listing_list' after login

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('listing_list')  # Replace with your desired redirect URL
        return super().dispatch(request, *args, **kwargs)


def custom_logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to the login page after logout


@superuser_required
def account_search(request):
    search_term = request.GET.get('q', '')
    filtered_listings = User.objects.filter(
        Q(username__icontains=search_term) | Q(email__icontains=search_term) | Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)
    )  # Search by title and description

    paginator = Paginator(filtered_listings, 5)  # Set the number of listings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'accounts': page_obj, 'is_paginated': page_obj.has_other_pages(), 'is_from_search': True,
               'search_term': search_term}
    return render(request, 'accounts/accounts_list.html', context)


@superuser_required
def accounts_list(request):
    users_list = User.objects.all()
    p = Paginator(users_list, 5)  # Set the number of listings per page

    page = request.GET.get('page')
    accounts = p.get_page(page)

    context = {'accounts': accounts}
    return render(request, 'accounts/accounts_list.html', context)


@superuser_required
def account_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    orders = Order.objects.filter(user=user.id)
    print(orders, user.id)
    context = {
        'account': user,
        'orders': orders,
    }
    return render(request, 'accounts/accounts_detail.html', context)