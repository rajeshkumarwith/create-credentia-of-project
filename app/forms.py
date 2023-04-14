from django import forms

# creating a form
class UserCreationForm(forms.Form):
    email=forms.EmailField()



    
