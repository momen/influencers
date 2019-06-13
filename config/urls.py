import os
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.documentation import include_docs_urls
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("influencers.users.urls", namespace="users")),
    path("core/", include("influencers.core.urls", namespace="core")),
    path("clients/", include("influencers.clients.urls", namespace="clients")),
    path(
        "influencers/", include("influencers.influencers.urls", namespace="influencers")
    ),
    path("robots.txt", include("robots.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG or os.getenv("DJANGO_SETTINGS_MODULE") == "config.settings.staging":
    # Show documentation
    urlpatterns += [
        path(
            "",
            include_docs_urls(
                title="Influencers",
                permission_classes=[permissions.IsAdminUser],
                authentication_classes=[SessionAuthentication],
            ),
            name="home",
        )
    ]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
