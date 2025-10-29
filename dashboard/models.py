from django.db import models
from django.core.validators import  RegexValidator , FileExtensionValidator
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name
    
class State(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="states")
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'name')
         
    def __str__(self):
        return f"{self.country.name} - {self.name}"
    
class City(models.Model):
    state = models.ForeignKey(State,on_delete=models.CASCADE,related_name="cities")
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('state','name')

    def __str__(self):
        return f"{self.state.name} - {self.name}"
    
    
class UserManage(models.Model):
    GENDER_CHOICE = [
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    ]    
    ROLE_CHOCIE = [
        ('HR','HR'),
        ('Manager','Manager'),
        ('Team Leader','Team Leader')
    ]

    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(r'^\d{10}$', 'Phone number must be exactly 10 digits')
        ]
    )
    gender = models.CharField(max_length=100,choices=GENDER_CHOICE)
    dob = models.DateField()
    profile_photo = models.ImageField(upload_to='user_photo/',blank=True,null=True)
    profile_video = models.FileField(upload_to='user_video/',blank=True,null=True,validators=[FileExtensionValidator(["mp4","avi","mov"])])
    bio = models.TextField(blank=False)
    country = models.ForeignKey(Country,related_name="users",on_delete=models.SET_NULL,null=True)
    state = models.ForeignKey(State,related_name="users",on_delete=models.SET_NULL,null=True)
    city = models.ForeignKey(City,related_name="users",on_delete=models.SET_NULL,null=True)
    role = models.CharField(max_length=100,choices=ROLE_CHOCIE)
    
    def __str__(self):
        return self.username
    