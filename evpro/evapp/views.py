from django.shortcuts import render, redirect
from .models import user
import uuid 

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        
        first = request.POST.get('first_name')
        last = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        vehicle = request.POST.get('vehicle_number')
        password = request.POST.get('password')

        
        uid = "USR" + str(uuid.uuid4())[:6]

        
        user.objects.create(    
            first_name=first,
            last_name=last,
            email=email,
            password=password,
            phone=phone,
            vehicle_number=vehicle
        )

        return redirect('index')  

    return render(request, 'signup.html')
