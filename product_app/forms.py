from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CreateUser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','password2']