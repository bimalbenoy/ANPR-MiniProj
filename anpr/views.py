from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Residents, Logbook
from .forms import UserRegistrationForm
from .running import process_video_file
from .databasecomp import compare_license_plates
from datetime import date, datetime
import os

# Static pages
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def animatedregister(request):
    return render(request, 'animatedregister.html')

def home1(request):
    return render(request, 'home1.html')


# Vehicle registration (Residents)
@login_required
def registerveh(request):
    if request.method == "POST":
        owner_name = request.POST.get("ownerName")
        vehicle_number = request.POST.get("vehicleNumber")
        resident_address = request.POST.get("residentAddress")
        category = request.POST.get("category")

        if Residents.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Vehicle Number already registered!")
            return redirect("registerveh")

        Residents.objects.create(
            owner_name=owner_name,
            vehicle_number=vehicle_number,
            resident_address=resident_address,
            category=category,
            registered_at=now(),
        )

        messages.success(request, "Vehicle registered successfully!")
        return redirect("registerveh")

    return render(request, "registervehicle.html")


# Vehicle registration (Logbook)
def registerlogbook(request):
    if request.method == "POST":
        owner_name = request.POST.get("ownerName2")
        vehicle_number = request.POST.get("vehicleNumber2")
        resident_address = request.POST.get("residentAddress2")
        category = request.POST.get("category2")

        if Logbook.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Vehicle Number already registered!")
            return redirect("registerlogbook")

        Logbook.objects.create(
            owner_name=owner_name,
            vehicle_number=vehicle_number,
            resident_address=resident_address,
            category=category,
            registered_date=date.today(),
            registered_time=datetime.now().time()
        )

        messages.success(request, "Vehicle registered successfully!")
        return redirect("registerlogbook")

    return render(request, "registerlogbook.html")


# Upload image/video and detect plate
@login_required
def upload(request):
    if request.method == "POST":
        # Create data directory under media/anpr/
        data_dir = os.path.join(settings.MEDIA_ROOT, 'anpr')
        os.makedirs(data_dir, exist_ok=True)

        plate_file_path = os.path.join(data_dir, 'car_plate_data.txt')
        with open(plate_file_path, "w") as file:
            file.write("")

        uploaded_file = request.FILES.get('photo')
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension in ['.mp4', '.avi', '.mov']:
            upload_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            upload_path = os.path.join(settings.MEDIA_ROOT, 'images')
        else:
            messages.error(request, "Unsupported file type.")
            return redirect("upload")

        os.makedirs(upload_path, exist_ok=True)
        fs = FileSystemStorage(location=upload_path)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Process video/image and match license plates
        process_video_file(file_path)
        plates = compare_license_plates(plate_file_path)

        for plate in plates:
            resident = Residents.objects.filter(vehicle_number=plate).first()
            if resident:
                Logbook.objects.create(
                    owner_name=resident.owner_name,
                    vehicle_number=resident.vehicle_number,
                    resident_address=resident.resident_address,
                    category=resident.category,
                    registered_date=date.today(),
                    registered_time=datetime.now().time()
                )
                if resident.category in ['Resident', 'Visitor']:
                    return render(request, 'approvegate.html', {
                        'No': resident.vehicle_number,
                        'name': resident.owner_name
                    })
                elif resident.category == 'Criminal':
                    return render(request, 'declinegate.html', {'No': plate})

        messages.warning(request, "No matching registered vehicles found.")
        return render(request, 'declinegate1.html')

    return render(request, 'upload.html')


# Gate Control Views
def gateopen(request):
    return render(request, 'approvegate.html')

def gateclose(request):
    return render(request, 'declinegate1.html')

def criminalgateclose(request):
    return render(request, 'declinegate.html')


# View logbook
@login_required
def logbook(request):
    vehicles = Logbook.objects.all()
    return render(request, 'logbook.html', {'vehicles': vehicles})


# User registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home1')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
