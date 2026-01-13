from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test


from Credoapp.forms import ArticleForm, ConnexionForm, ContactForm, InscriptionEvenementForm, InscriptionWebinaireForm, InscriptionFormationForm, TemoinForm ,WebinaireForm
from django.urls import reverse_lazy

from .models import Cible, Contact, Formation, Evenement, Article, InscriptionWebinaire, InscriptionFormation, Temoin, Webinaire
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .models import Galerie, Cible, Utilisateur, Formation, AxeIntervention
from django.db import models
from django.db.models import Q
from django import forms
from django.utils import timezone



def home(request):
    formations = Formation.objects.all()[:3]
    evenements = Evenement.objects.order_by("date_debut")[:3]
    articles = Article.objects.order_by("-date_publication")[:3]
    temoins = Temoin.objects.order_by("-date_creation")[:3]

    context = {
        "formations": formations,
        "evenements": evenements,
        "articles": articles,
        "temoins": temoins,
    }
    return render(request, "home.html", context)


def formations_list(request):
    formations = Formation.objects.all().order_by("-date_creation")
    axes = AxeIntervention.objects.all()
    
    # 1. Filtre par Axe (via URL ou GET param)
    selected_axe_slug = request.GET.get('axe')
    if selected_axe_slug:
        formations = formations.filter(axe__slug=selected_axe_slug)

    # 2. Recherche
    search_query = request.GET.get("search", "")
    if search_query:
        formations = formations.filter(
            Q(titre__icontains=search_query) | 
            Q(description_courte__icontains=search_query)
        )

    # 3. Rétrocompatibilité Cible (si besoin)
    cible_id = request.GET.get("cible")
    if cible_id:
        formations = formations.filter(cibles__id=cible_id)

    context = {
        "formations": formations,
        "axes": axes,
        "selected_axe": selected_axe_slug,
        "search_query": search_query,
        # Pour les templates existants si besoin
        "cibles": Cible.objects.all(),
        "selected_cible": int(cible_id) if cible_id else None,
    }
    return render(request, "formations.html", context)


def formation_detail(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    
    # Formations similaires (même axe ou même type)
    formations_similaires = Formation.objects.filter(
        models.Q(axe=formation.axe) | models.Q(type_formation=formation.type_formation)
    ).exclude(pk=pk)[:3]
    
    # Formulaire d'inscription
    inscription_form = InscriptionFormationForm(request.POST or None)
    success_message = None
    
    if request.method == "POST" and inscription_form.is_valid():
        inscription = inscription_form.save(commit=False)
        inscription.formation = formation
        inscription.save()
        
        # Envoi email de notification
        subject = f"Nouvelle inscription : {formation.titre}"
        message_text = f"Nouvelle inscription reçue pour : {formation.titre}\n\nClient : {inscription.nom} {inscription.prenom}\nEmail : {inscription.email}\nTéléphone : {inscription.telephone}\nMessage : {inscription.message}"
        
        try:
            send_mail(
                subject,
                message_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True
            )
        except:
            pass
            
        success_message = "Votre inscription a été envoyée avec succès ! Nous vous contacterons rapidement."
        inscription_form = InscriptionFormationForm() # Reset form

    context = {
        "formation": formation,
        "formations_similaires": formations_similaires,
        "inscription_form": inscription_form,
        "success_message": success_message,
    }
    return render(request, "formation_detail.html", context)


def evenements_list(request):
    evenements = Evenement.objects.all().order_by("date_debut")
    return render(request, "evenements.html", {"evenements": evenements})


def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    success_message = None

    if request.method == "POST":
        form = InscriptionEvenementForm(request.POST)
        if form.is_valid():
            inscription = form.save(commit=False)
            # Optionnel : ajouter un champ "evenement_id" si tu veux relier en DB
            # inscription.evenement_id = evenement.id
            inscription.save()
            success_message = "Votre inscription a été enregistrée !"
    else:
        form = InscriptionEvenementForm()

    autres_evenements = Evenement.objects.exclude(pk=pk).order_by("date_debut")[:3]

    context = {
        "evenement": evenement,
        "inscription_form": form,
        "success_message": success_message,
        "autres_evenements": autres_evenements,
    }
    return render(request, "evenement_detail.html", context)


def articles_list(request):
    articles = Article.objects.all().order_by("-date_publication")
    return render(request, "articles.html", {"articles": articles})

def article_detail(request, pk):
    """
    Affiche le détail d'un article, avec image et PDF téléchargeable.
    """
    article = get_object_or_404(Article, pk=pk)

    # URL absolue pour le PDF (utile si on veut un lien externe)
    pdf_url = None
    if article.fichier_pdf:
        pdf_url = request.build_absolute_uri(article.fichier_pdf.url)

    return render(request, "article_detail.html", {
        "article": article,
        "pdf_url": pdf_url,
    })
@login_required
def publier_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user  # L'utilisateur connecté est l'auteur
            article.save()
            return redirect("articles")  # Redirige vers la liste des articles
    else:
        form = ArticleForm()

    return render(request, "publier_article.html", {"form": form})



def temoignages(request):
    temoins = Temoin.objects.all().order_by("-date_creation")
    return render(request, "temoignages.html", {"temoins": temoins})


def temoignage_detail(request, pk):
    temoin = get_object_or_404(Temoin, pk=pk)
    return render(request, "temoignage_detail.html", {"temoin": temoin})

@login_required
def publier_temoignage(request):
    if request.method == "POST":
        form = TemoinForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("temoignages")
    else:
        form = TemoinForm()
    return render(request, "publier_temoignage.html", {"form": form})

def contact(request):
    context = {}
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if nom and email and message:
            try:
                # Sauvegarde en base
                Contact.objects.create(nom=nom, email=email, message=message)

                # Envoi email
                send_mail(
                    subject=f"Nouveau message de {nom}",
                    message=f"Expéditeur: {nom}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                context["success"] = True
            except BadHeaderError:
                context["error"] = "En-tête invalide détectée."
            except Exception as e:
                context["error"] = f"Erreur lors de l’envoi: {str(e)}"
        else:
            context["error"] = "Tous les champs sont obligatoires."

    return render(request, "contact.html", context)


def apropos(request):
    return render(request, "apropos.html")



# Formulaire d'inscription personnalisé
class InscriptionForm(UserCreationForm):
    cible = forms.ModelChoiceField(queryset=Cible.objects.all(), required=True)

    class Meta:
        model = Utilisateur
        fields = ["username", "email", "password1", "password2", "cible"]


def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = InscriptionForm()
    return render(request, "inscription.html", {"form": form})


def connexion(request):
    if request.method == "POST":
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "connexion.html", {"form": form})


def galerie(request):
    # param attendu en GET: ?categorie=conference  (on accepte aussi 'conférence')
    categorie_param = request.GET.get("categorie")  # ex: "conference" ou None

    images = Galerie.objects.all().order_by("-date_ajout")

    if categorie_param:
        # normalisation / mapping pour coller aux valeurs actuelles du modèle (avec accent)
        mapping = {
            "conference": "conférence",
            "conférence": "conférence",
            "atelier": "atelier",
            "autre": "autre",
        }
        valeur = mapping.get(categorie_param.lower(), categorie_param)
        images = images.filter(titre__iexact=valeur)

    return render(request, "galerie.html", {
        "images": images,
        "categorie": categorie_param,  # on renvoie le param brut pour les classes actives dans le template
    })




##>>>>>>>>>>webinaire les videos >>>>>>>>>>>>>>>>>>
def webinaires_list(request):
    now = timezone.now()
    
    # Le prochain webinaire à venir (pour le Hero header)
    next_webinaire = Webinaire.objects.filter(
        date__gte=now, 
        etat__in=["a_venir", "en_direct"]
    ).order_by("date").first()

    # Tous les webinaires à venir (excluant celui du hero si on veut, ou pas)
    # Ici on liste tout ce qui est futur
    upcoming = Webinaire.objects.filter(
        date__gte=now,
        etat__in=["a_venir", "en_direct"]
    ).order_by("date")
    
    if next_webinaire:
        upcoming = upcoming.exclude(id=next_webinaire.id)

    # Les replays et terminés
    past = Webinaire.objects.filter(
        models.Q(date__lt=now) | models.Q(etat__in=["replay", "termine"])
    ).order_by("-date")

    context = {
        "next_webinaire": next_webinaire,
        "upcoming": upcoming,
        "past": past,
    }
    return render(request, "webinaires_list.html", context)

# Helpers : vérifier si staff (pour accès création/édition)
def is_staff(user):
    return user.is_active and user.is_staff

@login_required
@user_passes_test(is_staff)
def webinaire_create(request):
    if request.method == "POST":
        form = WebinaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("webinaires_list")
    else:
        form = WebinaireForm()
    return render(request, "webinaire_form.html", {"form": form, "action": "Créer"})

@login_required
@user_passes_test(is_staff)
def webinaire_update(request, pk):
    webinaire = get_object_or_404(Webinaire, pk=pk)
    if request.method == "POST":
        form = WebinaireForm(request.POST, request.FILES, instance=webinaire)
        if form.is_valid():
            form.save()
            return redirect("webinaire_detail", pk=webinaire.pk)
    else:
        form = WebinaireForm(instance=webinaire)
    return render(request, "webinaire_form.html", {"form": form, "action": "Modifier"})

@login_required
@user_passes_test(is_staff)
def webinaire_delete(request, pk):
    webinaire = get_object_or_404(Webinaire, pk=pk)
    if request.method == "POST":
        webinaire.delete()
        return redirect("webinaires_list")
    return render(request, "webinaire_confirm_delete.html", {"webinaire": webinaire})


def inscription_webinaire(request, pk):
    webinaire = get_object_or_404(Webinaire, pk=pk)

    if request.method == "POST":
        form = InscriptionWebinaireForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            email = form.cleaned_data["email"]

            # Vérifie si l'utilisateur existe déjà
            utilisateur, created = Utilisateur.objects.get_or_create(
                email=email,
                defaults={"username": nom}
            )

            # Vérifie s'il est déjà inscrit à ce webinaire
            already = InscriptionWebinaire.objects.filter(
                webinaire=webinaire,
                utilisateur=utilisateur
            ).exists()

            if already:
                messages.warning(request, "Vous êtes déjà inscrit à ce webinaire.")
            else:
                InscriptionWebinaire.objects.create(
                    webinaire=webinaire,
                    utilisateur=utilisateur
                )
                
                # Envoi Email de confirmation
                subject = f"Confirmation inscription : {webinaire.titre}"
                message_text = f"""Bonjour {nom},

Votre inscription au webinaire "{webinaire.titre}" est confirmée !

Date : {webinaire.date.strftime('%d/%m/%Y à %H:%M')}
Lien d'accès : {webinaire.lien if webinaire.lien else 'Sera envoyé ultérieurement'}

À très vite,
L'équipe Credo Mali
"""
                try:
                    send_mail(
                        subject,
                        message_text,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"Erreur envoi email: {e}")

                messages.success(request, "Inscription réussie ! Un email de confirmation vous a été envoyé. 🎉")
                return redirect("webinaire_success", pk=webinaire.pk)

            return redirect("webinaires_list")
    else:
        form = InscriptionWebinaireForm()

    return render(request, "inscription_webinaire.html", {"form": form, "webinaire": webinaire})

def webinaire_success(request, pk):
    webinaire = get_object_or_404(Webinaire, pk=pk)
    return render(request, "webinaire_success.html", {"webinaire": webinaire})



def webinaire_detail(request, pk):
    webinaire = get_object_or_404(Webinaire, pk=pk)
    return render(request, "webinaire_detail.html", {"webinaire": webinaire})

def logout_view(request):
    if request.method == 'GET':   # accepter GET
        logout(request)
        return redirect('home')