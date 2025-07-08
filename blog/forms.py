from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'  # 꼭 설정
        self.helper.add_input(Submit('submit', '저장'))
