from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def contact(request):
    return render(request,'contact_us.html')