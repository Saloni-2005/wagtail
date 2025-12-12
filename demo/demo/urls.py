from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls

from search import views as search_views
from . import views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("images/", include(wagtailimages_urls)),
    path("search/", search_views.search, name="search"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("<slug:context_menu_slug>/header/login/", views.login_view_context, name="login_context"),
    path("<slug:context_menu_slug>/header/profile/", views.profile_view_context, name="profile_context"),
    path("<slug:context_menu_slug>/<slug:item_menu_slug>/<slug:item_slug>/", views.menu_item_detail_context, name="menu_item_detail_context"),
    path("<slug:menu_slug>/<slug:item_slug>/", views.menu_item_detail, name="menu_item_detail"),
    path("<slug:slug>/", views.menu_preview, name="menu_preview"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
]
