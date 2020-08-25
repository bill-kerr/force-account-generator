from django import forms


class UploadFileForm(forms.Form):
    docfile = forms.FileField()
    daily_sheets = forms.BooleanField(initial=False, required=False)
    save_json = forms.BooleanField(initial=False, required=False)
