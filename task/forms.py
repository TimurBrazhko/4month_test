from django import forms
from task.models import Category, Task


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        min_length=3,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search',
                'class': 'form-control',
                   }
        )
    )
    category = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )


class CreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category']

        def clean(self):
            cleaned_data = super().clean()
            title = cleaned_data.get('title')
            description = cleaned_data.get('description')
            if title.lower() == description.lower():
                raise forms.ValidationError('content and title cant be same')
            else:
                return cleaned_data
