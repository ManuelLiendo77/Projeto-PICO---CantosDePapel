from django import forms
from .models import Livro, Filme
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Utilizador
from django.utils.translation import gettext_lazy as _

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'isbn', 'descricao', 'imagem_capa', 'categoria', 'novidade', 'tem_filme']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class FilmeForm(forms.ModelForm):
    class Meta:
        model = Filme
        fields = ['titulo', 'trailer_url']


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    primeiro_nome = forms.CharField(required=True)
    ultimo_nome = forms.CharField(required=True)
    telefone = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    pais = forms.CharField(required=False)
    morada = forms.CharField(required=False)
    porta = forms.CharField(required=False)
    andar = forms.CharField(required=False)
    codigo_postal = forms.CharField(required=False)
    localidade = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = Utilizador.objects.create(
                primeiro_nome=self.cleaned_data.get('primeiro_nome',''),
                ultimo_nome=self.cleaned_data.get('ultimo_nome',''),
                telefone=self.cleaned_data.get('telefone',''),
                nif=self.cleaned_data.get('nif',''),
                pais=self.cleaned_data.get('pais',''),
                morada=self.cleaned_data.get('morada',''),
                porta=self.cleaned_data.get('porta',''),
                andar=self.cleaned_data.get('andar',''),
                codigo_postal=self.cleaned_data.get('codigo_postal',''),
                localidade=self.cleaned_data.get('localidade','')
            )
            # opcional: vincular perfil a usuario si usas OneToOne (no definido ahora)
        return user

    def clean_nif(self):
        nif = (self.cleaned_data.get('nif') or '').strip()
        if nif == '':
            return nif
        if not nif.isdigit() or len(nif) != 9:
            raise forms.ValidationError(_('NIF deve ter 9 dígitos numéricos.'))
        # checksum
        total = sum(int(nif[i]) * (9 - i) for i in range(8))
        check = 11 - (total % 11)
        if check >= 10:
            check = 0
        if check != int(nif[8]):
            raise forms.ValidationError(_('NIF inválido.'))
        return nif

    def clean_telefone(self):
        tel = (self.cleaned_data.get('telefone') or '').strip()
        if tel == '':
            return tel
        s = tel.replace(' ', '').replace('-', '')
        if s.startswith('+351'):
            s = s[4:]
        if not s.isdigit() or len(s) != 9:
            raise forms.ValidationError(_('Telefone inválido. Deve ter 9 dígitos (ou +351 seguido).'))
        return tel

    def clean_codigo_postal(self):
        cp = (self.cleaned_data.get('codigo_postal') or '').strip()
        if cp == '':
            return cp
        import re
        if not re.match(r'^\d{4}-\d{3}$', cp):
            raise forms.ValidationError(_('Formato de código postal inválido. Ex: 1234-567'))
        return cp
