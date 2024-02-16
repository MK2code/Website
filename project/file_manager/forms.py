from django import forms
from .models import Folder


# class MultipleFileInput(forms.FileField):
#     # widget = forms.FileField(label='Select files')
#     allow_multiple_selected = True
#     is_hidden = False
#     def __init__(self, attrs=None):
#         super().__init__(attrs)
#         self.widget = forms.ClearableFileInput(attrs={'multiple': True})
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
           
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileUploadForm(forms.Form):
    file = MultipleFileField(label='Select files')
    folder = forms.ModelChoiceField(queryset=None, required=False, label="Select an existing folder")
    new_folder_name = forms.CharField(max_length=255, required=False, label='Or create a new folder')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user)
        self.fields['folder'].choices = [(folder.id, folder.name) for folder in self.fields['folder'].queryset]
        
        
