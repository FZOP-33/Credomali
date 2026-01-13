from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("formations/", views.formations_list, name="formations"),
    path("formations/<int:pk>/", views.formation_detail, name="formation_detail"),

    path("evenements/", views.evenements_list, name="evenements_list"),
    path("evenements/<int:pk>/", views.evenement_detail, name="evenement_detail"),

    path("articles/", views.articles_list, name="articles"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("articles/publier/", views.publier_article, name="publier_article"),

    path("temoignages/", views.temoignages, name="temoignages"),
    path("temoignages/<int:pk>/", views.temoignage_detail, name="temoignage_detail"),
    path("temoignages/publier/", views.publier_temoignage, name="publier_temoignage"),


    path("contact/", views.contact, name="contact"),
    path("a-propos/", views.apropos, name="apropos"),

    path("inscription/", views.inscription, name="inscription"),
    path("connexion/", views.connexion, name="connexion"),
    path('logout/', views.logout_view, name='logout'),
    path("galerie/", views.galerie, name="galerie"),
    #path("galerie/conferences/", views.galerie_conference, name="galerie_conference"),



    path("webinaires/", views.webinaires_list, name="webinaires_list"),
    path("webinaire/inscription/<int:pk>/", views.inscription_webinaire, name="inscription_webinaire"),
    path("webinaire/succes/<int:pk>/", views.webinaire_success, name="webinaire_success"),
    path("webinaire/<int:pk>/", views.webinaire_detail, name="webinaire_detail"),

            # admin/staff
    path("webinaires/creer/", views.webinaire_create, name="webinaire_create"),
    path("webinaires/<int:pk>/modifier/", views.webinaire_update, name="webinaire_update"),
    path("webinaires/<int:pk>/supprimer/", views.webinaire_delete, name="webinaire_delete"),


]
