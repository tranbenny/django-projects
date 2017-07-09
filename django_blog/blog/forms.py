from django import forms

from blog.models import Comment

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


'''
By default django builds a form from the fields
'''
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')