from django import forms


class UploadFileForm(forms.Form):
    docfile = forms.FileField()


class GenerateForceAccountForm(forms.Form):
    docfile = forms.FileField(required=True)
    daily_sheets = forms.BooleanField(initial=False, required=False)
    save_json = forms.BooleanField(initial=False, required=False)
