from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from books.views import BookListAsIndex

urlpatterns = [
                  path('', BookListAsIndex, name='book_list'),
                  path('admin/', admin.site.urls),
                  path('books/', include('books.urls')),
                  path('accounts/', include('accounts.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
