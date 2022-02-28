from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class lageBruker(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2']
        
    def clean_brukernavn(self):
        brukernavn = self.cleaned_data.get('username')

        bruker_qs = User.objects.filter(username = brukernavn)
        if bruker_qs.exists():
            raise forms.ValidationError('Brukernavn allerede i bruk')
        return brukernavn
    
    def clean(self, *args, **kwargs):
        passord1 = self.cleaned_data.get('password1')
        passord2 = self.cleaned_data.get('password2')

        if passord1 != passord2:
            raise forms.ValidationError('Passordene må være like')
        return super(lageBruker, self).clean(*args, **kwargs)