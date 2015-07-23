from django.conf.urls import include, url
from TP4375Serveur import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', 'TP4375Serveur.views.index'),
    url(r'^RechercheAjax/(?P<critere>[\w\ ]{0,50})/$', 'TP4375Serveur.views.AjaxSearch',),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
