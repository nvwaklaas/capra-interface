from django import forms


class UploadFileForm(forms.Form):
    """Form to upload a file"""
    route_file = forms.FileField()
