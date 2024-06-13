from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page

from products.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cache_page(60 * 2)(IndexView.as_view()), name='index'),
    path('products/', cache_page(60 * 2)(include('products.urls', namespace='products'))),
    path('users/', cache_page(60)(include('users.urls', namespace='users'))),
    path('api/', cache_page(60 * 10)(include('api.urls', namespace='api'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
