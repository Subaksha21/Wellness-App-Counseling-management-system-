import os
from django.conf import settings
from django.contrib.auth import get_backends
from counseling.models import CounselingMaterial
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm  # Custom form for profile update
from .models import CounselingMaterial,Appointment, Counselor
from django.http import HttpResponse,  Http404
from .forms import ContactForm, AppointmentForm
from .utils import generate_pdf_thumbnail
from .models import Appointment



# Home page view
def home(request):
    materials = None
    missing_files = []

    if request.user.is_authenticated:
        materials = CounselingMaterial.objects.all()

        # Check if the material file exists
        for material in materials:
            if material.file:  # Check if the file field has a file
                file_path = os.path.join(settings.MEDIA_ROOT, str(material.file))  # Use the correct field 'file'
                if not os.path.exists(file_path):
                    missing_files.append(material.id)  # Track material by id

    return render(request, 'home.html', {'materials': materials, 'missing_files': missing_files})

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

# Counseling materials download page (requires login)
@login_required
def materials(request):
    materials = CounselingMaterial.objects.all()  # Fetch all counseling materials
    return render(request, 'materials.html', {'materials': materials})

# File download view (requires login)
@login_required
def download_material(request, material_id):
    try:
        material = CounselingMaterial.objects.get(id=material_id)

        # Ensure the material has a file associated with it
        if not material.file:
            messages.error(request, 'The requested material does not have a file associated with it.')
            return redirect('materials')  # Redirect to materials page if no file

        # Check for 'action' parameter in the request to determine whether to download or display
        action = request.GET.get('action', 'download')

        # Read the file content
        file_content = material.file.open('rb')

        # Set the appropriate response based on the 'action' parameter
        if action == 'view':
            # Display PDF in the browser
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{material.title}.pdf"'
        else:
            # Download the PDF
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{material.title}.pdf"'
        
        return response

    except CounselingMaterial.DoesNotExist:
        raise Http404("Material not found")
    except FileNotFoundError:
        messages.error(request, 'The requested file is missing.')
        return redirect('materials')  # Redirect to the materials page if the file is missing
# Profile view (requires login)
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# Edit profile view (requires login)
@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def dashboard(request):
    # Fetch all counseling materials from the database
    materials = CounselingMaterial.objects.all()
    
    # Fetch user-specific appointments
    appointments = Appointment.objects.filter(user=request.user)  # Filter appointments by logged-in user

    return render(request, 'dashboard.html', {'materials': materials, 'appointments': appointments})


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        appointment.status = request.POST.get('status', appointment.status)
        appointment.save()
        return redirect('dashboard')
    
    return render(request, 'edit_appointment.html', {'appointment': appointment})



@login_required
def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.user = request.user
            contact_message.save()
            messages.success(request, 'Your message has been sent to support.')
            return redirect('home')  # Redirect back to the dashboard after successful submission
    else:
        form = ContactForm()

    return render(request, 'contact_support.html', {'form': form})




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Retrieve the authentication backend and set it
            backend = get_backends()[0]  # Pick the first available backend (assuming it's the correct one)
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'

            login(request, user)  # Pass the backend explicitly
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})




def material_detail(request, material_id):
    try:
        material = CounselingMaterial.objects.get(id=material_id)
        
        # Path to store the thumbnail image
        thumbnail_path = f"media/thumbnails/{material.id}.jpg"
        
        # Generate thumbnail if it doesn't exist
        if not os.path.exists(thumbnail_path):
            generate_pdf_thumbnail(material.file.path, thumbnail_path)
        
        context = {
            'material': material,
            'thumbnail_url': thumbnail_path
        }
        return render(request, 'material_detail.html', context)
    except CounselingMaterial.DoesNotExist:
        raise Http404("Material not found")




# viewsfor councellor appointment

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'Your appointment has been scheduled!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'schedule_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})
