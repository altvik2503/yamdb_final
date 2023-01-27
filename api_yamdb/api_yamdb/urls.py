from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from reviews.views import default_redirect

urlpatterns = [
    path('admin/', admin.site.urls, name='login'),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', default_redirect)
]
