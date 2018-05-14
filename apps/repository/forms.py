from django import forms

class FormOrganization(forms.Form):
    organization = forms.CharField()
