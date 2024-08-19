from .models import Comment
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # Layout to customize the form appearance and include labels
        self.helper.layout = Layout(
            Field('recipient', css_class='form-control'),
            Field('subject', css_class='form-control'),
            Field('message', css_class='form-control'),
            Submit('submit', 'Send Email', css_class='btn btn-primary')
        )
