from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="RESTful APIs for Blogging website",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    # path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
    #      name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger',
    #      cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
]


url_v1 = [
    path('api/v1/', include("accounts.urls")),
    path('api/v1/blogs/', include('blog.urls')),
]

urlpatterns += url_v1
