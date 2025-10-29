from .models import UserManage
from django import forms


class UserManageForm(forms.ModelForm):
    class Meta:
        model = UserManage
        fields = '__all__'
        exclude = ["country","state","city"]
        widgets = {
            'dob' : forms.DateInput(attrs={'type':'date'}),
            'gender' : forms.RadioSelect(choices=UserManage.GENDER_CHOICE),
            'role': forms.Select(choices=UserManage.ROLE_CHOCIE)
        }

