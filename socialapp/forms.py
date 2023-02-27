from django import forms
from socialapp.models import Myuser,Posts,Comment,Profile
from django.contrib.auth.forms import UserCreationForm

#form for registration
class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    class Meta:
        model=Myuser
        fields=["first_name", "last_name", "username",
                 "password1","password2", "bio", "email","profile_pic"]
        
    
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control border border-info", "placeholder": "enter firstname"}),
            "last_name": forms.TextInput(attrs={"class": "form-control border border-info", "placeholder": "enter lastname"}),
            "username": forms.TextInput(attrs={"class": "form-control border border-info", "placeholder": "enter username"}),
            "email": forms.EmailInput(attrs={"class": " form-control border border-info", "placeholder": "enter email"}),
            "bio": forms.TextInput(attrs={"class": " form-control border border-info", "placeholder": " your Bio .."}),
            "location": forms.TextInput(attrs={"class": "form-control border border-info", "placeholder": "enter your location "}),
        }
      
# form for login purpose
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

#form for creating a post
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","images","description"]

        widgets={
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "images": forms.FileInput(attrs={"class":"form-select"}),
            "description": forms.Textarea(attrs={"class":"form-control",'rows':'3'}),
        }


#form for commenting
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["comment"]

        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control",'rows':'3'}),
        }


#form for editing Profile

# class UpdateprofileForm(forms.ModelForm):
#     class Meta:
#         model=Profile
#         fields=["bio","email"]

#         widgets = {
#             "bio": forms.TextInput(attrs={"class": "form-control"}),
#             # "profile_pic": forms.FileInput(attrs={"class": "form-select"}),
#             "email": forms.EmailInput(attrs={"class": "form-control"}),
#         #     "username": forms.TextInput(attrs={"class": "form-control"})
#         }
