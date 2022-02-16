
from django.contrib import admin
from django.urls import include, path

# from .settings import DEBUG

urlpatterns = [
    path('api/', include('recipes.urls')),
    path('api/', include('users.urls')),
    # path('api/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
]

# if DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls))
#     ]

# if DEBUG:
#     urlpatterns += [
#         path('silk/', include('silk.urls', namespace='silk'))
#     ]
