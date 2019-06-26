from django import forms
#from verified_email_field.forms import VerifiedEmailField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




# our new form
class ContactForm(forms.Form):
    subject= forms.CharField(required=True)
    from_email = forms.EmailField(required=True)
    form_content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Subject:"
        self.fields['from_email'].label = "Your email:"
        self.fields['form_content'].label = "What do you want to say?"



class UserDetailChangeForm(forms.ModelForm):
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username']
