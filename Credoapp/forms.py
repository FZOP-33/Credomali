from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Contact, Temoin, Utilisateur, Cible, Webinaire, InscriptionFormation
class InscriptionForm(UserCreationForm):
    cible = forms.ModelChoiceField(queryset=Cible.objects.all(), required=True)

    class Meta:
        model = Utilisateur
        fields = ["username", "email", "password1", "password2", "cible"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "email": forms.EmailInput(attrs={"class": "border p-2 rounded w-full"}),
            "password1": forms.PasswordInput(attrs={"class": "border p-2 rounded w-full"}),
            "password2": forms.PasswordInput(attrs={"class": "border p-2 rounded w-full"}),
            "cible": forms.Select(attrs={"class": "border p-2 rounded w-full"}),
        }


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "border p-2 rounded w-full"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "border p-2 rounded w-full"}))

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["titre", "contenu", "image", "fichier_pdf"]  # ajout du PDF
        widgets = {
            "titre": forms.TextInput(attrs={"class": "w-full rounded px-3 py-2 border"}),
            "contenu": forms.Textarea(attrs={"class": "w-full rounded px-3 py-2 border"}),
        }


class TemoinForm(forms.ModelForm):
    class Meta:
        model = Temoin
        fields = ["nom", "fonction", "message", "photo"]

        widgets = {
            "nom": forms.TextInput(attrs={"class": "input-style", "placeholder": "Votre nom"}),
            "fonction": forms.TextInput(attrs={"class": "input-style", "placeholder": "Ex: Étudiant, Client..."}),
            "message": forms.Textarea(attrs={"class": "input-style", "rows": 5, "placeholder": "Votre témoignage"}),
        }
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["nom", "email", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "email": forms.EmailInput(attrs={"class": "border p-2 rounded w-full"}),
            "message": forms.Textarea(attrs={"class": "border p-2 rounded w-full h-32"}),
        }


class InscriptionEvenementForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["nom", "email", "message"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors", "placeholder": "Votre nom complet"}),
            "email": forms.EmailInput(attrs={"class": "w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors", "placeholder": "votre@email.com"}),
            "message": forms.Textarea(attrs={"class": "w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors h-32", "placeholder": "Message ou question facultative"}),
        }


class WebinaireForm(forms.ModelForm):
    class Meta:
        model = Webinaire
        fields = ["titre", "description", "date", "lieu", "lien", "video_file", "image"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "description": forms.Textarea(attrs={"class": "border p-2 rounded w-full h-40"}),
            "date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "border p-2 rounded w-full"}),
            "lieu": forms.TextInput(attrs={"class": "border p-2 rounded w-full"}),
            "lien": forms.URLInput(attrs={"class": "border p-2 rounded w-full"}),
        }
class InscriptionWebinaireForm(forms.Form):
    nom = forms.CharField(max_length=150)
    email = forms.EmailField()

class InscriptionFormationForm(forms.ModelForm):
    class Meta:
        model = InscriptionFormation
        fields = ['nom', 'prenom', 'email', 'telephone', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors', 'placeholder': 'Votre nom'}),
            'prenom': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors', 'placeholder': 'Votre prénom'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors', 'placeholder': 'votre@email.com'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors', 'placeholder': '+223 ...'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-[#0A3D62] transition-colors h-32', 'placeholder': 'Un message ou une question ? (Optionnel)'}),
        }