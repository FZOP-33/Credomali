from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db import models


# --- Cibles (public visé) ---
class Cible(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Cible"
        verbose_name_plural = "Cibles"

    def __str__(self):
        return self.nom


class Utilisateur(AbstractUser):
    cible = models.ForeignKey(
        'Cible',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="utilisateurs"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
# --- AXES & TYPES (NOUVEAU) ---

class AxeIntervention(models.Model):
    nom = models.CharField(max_length=100, help_text="Ex: Marketing, Communication, Orientation")
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    message_cle = models.CharField(max_length=255, blank=True, help_text="Ex: 'Ne choisis pas ta carrière au hasard'")
    icone = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône FontAwesome ou emoji")
    
    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class TypeFormation(models.Model):
    nom = models.CharField(max_length=100, help_text="Ex: Formation Continue, Alternance, Hybride")
    
    def __str__(self):
        return self.nom


# --- Formations ou Services ---
class Formation(models.Model):
    # Relation clés
    axe = models.ForeignKey(AxeIntervention, on_delete=models.SET_NULL, null=True, related_name="formations")
    type_formation = models.ForeignKey(TypeFormation, on_delete=models.SET_NULL, null=True, blank=True)

    # Infos de base
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description_courte = models.TextField(help_text="Accroche pour la liste")
    
    # Contenu Riche (Vision Credo)
    pour_qui = models.TextField(blank=True, help_text="Cibles : Bacheliers, Commerçants...")
    objectifs_cles = models.TextField(blank=True, help_text="Ce que vous allez gagner")
    programme_detaille = models.TextField(blank=True, help_text="Liste des modules")
    avantages = models.TextField(blank=True, help_text="Pourquoi nous ? (Avant/Après)")
    
    # Logistique
    prix = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    duree = models.CharField(max_length=100, blank=True, help_text="Ex: 3 jours / 20 heures")
    lieu = models.CharField(max_length=255, blank=True, help_text="Présentiel / En ligne")
    
    # Médias
    image = models.ImageField(upload_to="formations/", null=True, blank=True)
    brochure_pdf = models.FileField(upload_to="formations/brochures/", null=True, blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # Ancienne relation (à garder pour compatibilité ou à migrer)
    cibles = models.ManyToManyField(Cible, blank=True, related_name="formations")

    class Meta:
        verbose_name = "Formation / Service"
        verbose_name_plural = "Formations / Services"

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)


# --- Événements ---
class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    lieu = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="evenements/", null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"

    def __str__(self):
        return f"{self.titre} ({self.date_debut.date()})"



class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField(blank=True)  # devient optionnel si PDF
    image = models.ImageField(upload_to="articles/", null=True, blank=True)
    fichier_pdf = models.FileField(upload_to="articles/pdfs/", null=True, blank=True)
    auteur = models.ForeignKey(
        "Utilisateur",
        on_delete=models.CASCADE,
        related_name="articles"
    )
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article éducatif"
        verbose_name_plural = "Articles éducatifs"

    def __str__(self):
        return self.titre

    def is_pdf(self):
        return bool(self.fichier_pdf)


# --- Témoignages ---
class Temoin(models.Model):
    nom = models.CharField(max_length=100)
    fonction = models.CharField(
        max_length=150,
        blank=True,
        help_text="Ex: Étudiant, Client, Partenaire..."
    )
    message = models.TextField()
    photo = models.ImageField(upload_to="temoins/", null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.nom} - {self.fonction}"

    def save(self, *args, **kwargs):
        # Nettoyage automatique des espaces pour éviter les bugs d'affichage
        if self.nom:
            self.nom = self.nom.strip()
        if self.fonction:
            self.fonction = self.fonction.strip()
        super().save(*args, **kwargs)



class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.email}) - {self.date_envoi.strftime('%d/%m/%Y %H:%M')}"

class Galerie(models.Model):
    TYPE_CHOIX = [
        ("conférence", "Conférence"),
        ("atelier", "Atelier"),
        ("autre", "Autre"),
    ]

    titre = models.CharField(max_length=200, blank=True, choices=TYPE_CHOIX)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="galerie/")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image de la galerie"
        verbose_name_plural = "Galerie"

    def __str__(self):
        return self.titre if self.titre else f"Image {self.id}"

class Intervenant(models.Model):
    nom = models.CharField(max_length=150)
    titre = models.CharField(max_length=200, help_text="Ex: Expert Marketing, CEO de ...")
    photo = models.ImageField(upload_to="intervenants/", null=True, blank=True)
    bio = models.TextField(blank=True, help_text="Courte biographie")
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Webinaire(models.Model):
    STATUT_CHOIX = [
        ("a_venir", "À venir"),
        ("en_direct", "En direct"),
        ("replay", "Replay disponible"),
        ("termine", "Terminé"),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, help_text="Généré automatiquement si vide")
    description = models.TextField()
    date = models.DateTimeField()
    duree = models.CharField(max_length=50, help_text="Ex: 1h 30m", default="1h")
    etat = models.CharField(max_length=20, choices=STATUT_CHOIX, default="a_venir")
    
    lieu = models.CharField(max_length=255, blank=True)  # utile si hybride
    lien = models.URLField(blank=True, null=True, help_text="Lien YouTube/Zoom (ou page d'accès).")
    video_file = models.FileField(upload_to="webinaires/videos/", blank=True, null=True)
    
    image = models.ImageField(upload_to="webinaires/", blank=True, null=True, help_text="Affiche")
    background_image = models.ImageField(upload_to="webinaires/backgrounds/", blank=True, null=True, help_text="Image de fond pour le header")
    ressource_pdf = models.FileField(upload_to="webinaires/ressources/", blank=True, null=True, help_text="Document (PDF) à partager avec les participants")
    
    intervenants = models.ManyToManyField(Intervenant, blank=True, related_name="webinaires")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        verbose_name = "Webinaire"
        verbose_name_plural = "Webinaires"

    def __str__(self):
        return f"{self.titre} ({self.date.date()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def has_video(self):
        return bool(self.lien or self.video_file)
    
class InscriptionWebinaire(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    webinaire = models.ForeignKey(Webinaire, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'webinaire')  # Un utilisateur ne peut s'inscrire qu'une seule fois

    def __str__(self):
        return f"{self.utilisateur.username} - {self.webinaire.titre}"

class InscriptionFormation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="inscriptions")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscription Formation"
        verbose_name_plural = "Inscriptions Formations"

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.formation.titre}"
