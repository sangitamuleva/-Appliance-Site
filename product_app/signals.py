from .models import Customer
from django.db.models.signals import post_save
from django.contrib.auth.models import User ,Group

# on the registration of user we need to create group and customer object
def create_cutomer_profile(sender,instance,created,**kwargs):
    if created:
     group = Group.objects.get(name='customer')
     # user.groups.add(group)
     instance.groups.add(group)

     Customer.objects.create(user=instance,name=instance.username)

post_save.connect(create_cutomer_profile,sender=User)