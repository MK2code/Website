from django import forms
from .models import Folder


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select files to upload', widget=forms.ClearableFileInput())
    folder = forms.ModelChoiceField(queryset=None, required=False, label="Select an existing folder")
    new_folder_name = forms.CharField(max_length=255, required=False, label='Or create a new folder')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user)
        self.fields['folder'].choices = [(folder.id, folder.name) for folder in self.fields['folder'].queryset]
        
        
