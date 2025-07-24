from django.shortcuts import render, redirect, get_object_or_404
from .models import User, ChargingStation, Booking
from django.http import HttpResponseForbidden
from functools import wraps

# -------------------- Utility Decorators --------------------

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        if not admin_id or not User.objects.filter(id=admin_id, role='admin').exists():
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

# -------------------- Auth Views --------------------

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

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        User.objects.create(
            first_name=first,
            last_name=last,
            email=email,
            password=password,  # For demo only: store securely in real apps
            phone=phone,
            vehicle_number=vehicle,
            role='user'  # ✅ Set role explicitly
        )

        return redirect('home')

    return render(request, 'signup.html')
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['user_role'] = user.role  # 👈 Store role in session

            # ✅ Redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('home')

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# -------------------- User Views --------------------
def home(request):
    user = request.user

    # Get all stations or filter if query param exists
    stations = ChargingStation.objects.all()
    if request.GET.get('available_only'):
        stations = stations.filter(available_slots__gt=0)

    # Get user bookings
    bookings = Booking.objects.filter(user=user)

    context = {
        'name': user.first_name,
        'vehicle': user.vehicle_number,
        'stations': stations,
        'bookings': bookings,
        'user': user,
    }

    return render(request, 'home.html', context)
    

def station_list(request):
    stations = ChargingStation.objects.all()
    filter_slots = request.GET.get('available_only', None)
    if filter_slots:
        stations = stations.filter(available_slots__gt=0)
    return render(request, 'station_list.html', {'stations': stations})

def station_detail(request, station_id):
    station = get_object_or_404(ChargingStation, id=station_id)
    return render(request, 'station_detail.html', {'station': station})

# -------------------- Admin Views --------------------

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, password=password, role='admin')
            request.session['admin_id'] = user.id
            return redirect('admin_dashboard')
        except User.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')


@admin_required
def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    station_count = ChargingStation.objects.count()
    user_count = User.objects.filter(role='user').count()
    booking_count = 0  # Update this once reservation model is ready

    return render(request, 'admin_dashboard.html', {
        'station_count': station_count,
        'user_count': user_count,
        'booking_count': booking_count
    })

@admin_required
def manage_stations(request):
    stations = ChargingStation.objects.all()
    return render(request, 'admin/manage_stations.html', {'stations': stations})

@admin_required
def add_station(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        is_available = 'is_available' in request.POST
        image = request.FILES.get('image')
        ChargingStation.objects.create(name=name, location=location, is_available=is_available, image=image)
        return redirect('manage_stations')
    return render(request, 'admin/add_station.html')

@admin_required
def edit_station(request, station_id):
    station = get_object_or_404(ChargingStation, id=station_id)
    if request.method == 'POST':
        station.name = request.POST['name']
        station.location = request.POST['location']
        station.is_available = 'is_available' in request.POST
        if 'image' in request.FILES:
            station.image = request.FILES['image']
        station.save()
        return redirect('manage_stations')
    return render(request, 'admin/edit_station.html', {'station': station})

@admin_required
def delete_station(request, station_id):
    station = get_object_or_404(ChargingStation, id=station_id)
    station.delete()
    return redirect('manage_stations')

@admin_required
def manage_users(request):
    users = User.objects.filter(role='user')
    return render(request, 'admin/manage_users.html', {'users': users})


