
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from post.views import (

    index, 
    blog, 
    post, 
    search,
    contact,
    post_update, 
    post_delete, 
    post_create
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('create/', post_create, name='post-create'),
    path('post/<id>/', post, name='post'),
    path('post/<id>/update/', post_update, name='post-update'),
    path('post/<id>/delete/', post_delete, name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('contact/', contact, name='contact'),
    path('accounts/', include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('members/', include('django.contrib.auth.urls')),
    # path('members/', include('members.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)