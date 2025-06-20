from django.shortcuts import render, redirect
from .models import User
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

        
        User.objects.create(    
            first_name=first,
            last_name=last,
            email=email,
            password=password,
            phone=phone,
            vehicle_number=vehicle
        )

        return redirect('home')  

    return render(request, 'signup.html')



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Fixed here
            if user.password == passw:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Incorrect password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'No user found'})   

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')