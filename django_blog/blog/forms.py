from django import forms


'''
Django Form Classes
- Forms: build standard forms
- ModelForm: build forms to create or update model instances
'''
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)