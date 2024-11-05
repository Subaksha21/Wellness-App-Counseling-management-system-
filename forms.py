from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage, Appointment,Counselor


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']



# forms.py

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']

    # Customize form field appearance
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Subject'})
        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Your message'})




class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counselor', 'date', 'reason']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }


