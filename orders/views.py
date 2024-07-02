# orders/views.py
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from enums import OrderStatus
from .models import Order

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    if request.user.is_superuser:
        orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def accept_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.is_superuser or order.user == request.user:
        order.status = OrderStatus.APPROVED.name
        order.save()
        return redirect('account_detail', pk=order.user.pk)
    else:
        return HttpResponseForbidden()

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.is_superuser or order.user == request.user:
        order.status = OrderStatus.CANCELED.name
        order.save()
        return redirect('account_detail', pk=order.user.pk)
    else:
        return HttpResponseForbidden()