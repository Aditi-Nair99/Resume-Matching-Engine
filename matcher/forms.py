from django import forms


class ResumeUploadForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=50, required=False)
    resume = forms.FileField()
