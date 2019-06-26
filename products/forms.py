from django import forms
from .models import Product
from django.utils.text import slugify



PUBLISH_CHOICES = {
    ('publish', "Publish"),
    ('draft', "Draft"),
}





class ProductAddForm(forms.Form):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "media",
        ]



    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "custom-class",
            "placeholder": "Title",
            }
        ))
    description = forms.CharField(widget=forms.Textarea(
        attrs = {
            "class": "my-custom-class",
            "placeholder": "Description",
            "some-attr": "this",
        }
        ))
    price = forms.DecimalField()
    publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES,
        required=False)


    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            raise forms.ValidationError("Price must be greater than $1.00")
        elif price >= 99.99:
            raise forms.ValidationError("Price must be less than $100.00")
        else:
            return price


    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title is too short (required at least 3 characters)")


    def clean_media(self):
        media = self.cleaned_data.get("media")
        ## jesli to nie jest zdjecie, to odmowic przyjecia pliku

        return media






class ProductModelForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    tags = forms.CharField(label='Related Tags', required=False)
    publish = forms.ChoiceField(widget=forms.RadioSelect, choices=PUBLISH_CHOICES, required=False)

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "media",
        ]
        widgets = {
        "description": forms.Textarea(
            attrs={"placeholder":"New Description",
            }),
        "title": forms.TextInput(
            attrs={
            "placeholder":"Title"
            }
            )
        }




    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            raise forms.ValidationError("Price must be greater than $1.00")
        elif price >= 100.00:
            raise forms.ValidationError("Price must be less than $100.00")
        else:
            return price


    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title is too short (required at least 3 characters)")


    def clean_media(self):
        media = self.cleaned_data.get("media")
        return media
