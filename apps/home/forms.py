from django import forms

from apps.home.models import UploadData


class UploadsForm(forms.ModelForm):
    ##country_id = forms.CharField(widget=forms.Select(attrs={"class":"forms-control"}))
    class Meta:
        model = UploadData
        fields = ['profile_id','name','dob','remarks','created']