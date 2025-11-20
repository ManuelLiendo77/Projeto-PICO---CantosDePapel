from django import forms
from .models import Review
from django.utils.translation import gettext_lazy as _


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'titulo', 'comentario']
        labels = {
            'rating': _('Avaliação'),
            'titulo': _('Título da avaliação'),
            'comentario': _('Comentário'),
        }
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'rating-input'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resuma a sua opinião...',
                'maxlength': '200'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva a sua avaliação detalhada...',
                'rows': '5'
            }),
        }
        
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError(_('A avaliação deve estar entre 1 e 5 estrelas.'))
        return rating
