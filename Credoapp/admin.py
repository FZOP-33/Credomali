from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cible, Contact, Formation, Evenement, Article, Galerie, InscriptionWebinaire, Temoin, Utilisateur, Webinaire, Intervenant, AxeIntervention, TypeFormation


@admin.register(Cible)
class CibleAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)

# Formation
# Formation (Mise à jour Vision Credo)
@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("titre", "axe", "type_formation", "prix", "date_creation", "image_tag")
    search_fields = ("titre", "description_courte", "objectifs_cles")
    list_filter = ("axe", "type_formation", "date_creation", "cibles") # keep cibles for legacy compatibility if needed
    filter_horizontal = ("cibles",)
    prepopulated_fields = {"slug": ("titre",)}

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image"

@admin.register(AxeIntervention)
class AxeInterventionAdmin(admin.ModelAdmin):
    list_display = ("nom", "slug", "icone")
    prepopulated_fields = {"slug": ("nom",)}

@admin.register(TypeFormation)
class TypeFormationAdmin(admin.ModelAdmin):
    list_display = ("nom",)

# Evenement
@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ("titre", "date_debut", "date_fin", "lieu", "image_tag")
    search_fields = ("titre", "description", "lieu")
    list_filter = ("date_debut", "date_fin")

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "date_publication", "image_tag", "pdf_link")
    search_fields = ("titre", "contenu", "auteur__username")
    list_filter = ("date_publication",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image"

    def pdf_link(self, obj):
        if obj.fichier_pdf:
            return format_html('<a href="{}" target="_blank">📄 Voir PDF</a>', obj.fichier_pdf.url)
        return "-"
    pdf_link.short_description = "PDF"

# Temoin
@admin.register(Temoin)
class TemoinAdmin(admin.ModelAdmin):
    list_display = ("nom", "fonction", "date_creation", "photo_tag")
    search_fields = ("nom", "fonction", "message")
    list_filter = ("date_creation",)

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px;" />', obj.photo.url)
        return "-"
    photo_tag.short_description = "Photo"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", 'message',"date_envoi")
    search_fields = ("nom", "email", "message")
    list_filter = ("date_envoi",)




# --- Personnalisation de l'admin Utilisateur ---
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "cible", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "cible")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


# --- Admin pour la Galerie ---
@admin.register(Galerie)
class GalerieAdmin(admin.ModelAdmin):
    list_display = ("titre", "image_preview", "date_ajout")
    search_fields = ("titre", "description")
    list_filter = ("date_ajout",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px; border-radius:5px;" />', obj.image.url)
        return "Pas d'image"

    image_preview.short_description = "Aperçu"

@admin.register(Intervenant)
class IntervenantAdmin(admin.ModelAdmin):
    list_display = ("nom", "titre", "photo_preview")
    search_fields = ("nom", "titre")

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:50px; height:50px; border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return "—"
    photo_preview.short_description = "Photo"

@admin.register(Webinaire)
class WebinaireAdmin(admin.ModelAdmin):
    list_display = ("titre", "date", "etat", "duree", "image_preview", "nb_inscrits")
    list_filter = ("etat", "date")
    search_fields = ("titre", "description")
    prepopulated_fields = {"slug": ("titre",)}
    filter_horizontal = ("intervenants",)
    
    def nb_inscrits(self, obj):
        return obj.inscriptionwebinaire_set.count()
    nb_inscrits.short_description = "Inscrits"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover;border-radius:4px"/>', obj.image.url)
        return "—"
    image_preview.short_description = "Image"

    def video_preview(self, obj):
        if obj.video_file:
            return format_html(
                '<video width="120" height="80" controls>'
                '<source src="{}" type="video/mp4">Votre navigateur ne supporte pas la vidéo.</video>',
                obj.video_file.url
            )
        return "—"
    video_preview.short_description = "Vidéo"


@admin.register(InscriptionWebinaire)
class InscriptionWebinaireAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "webinaire", "date_inscription")
    list_filter = ("webinaire", "date_inscription")
    search_fields = ("utilisateur__username", "utilisateur__email", "webinaire__titre")
    ordering = ("-date_inscription",)
    readonly_fields = ("date_inscription",)

