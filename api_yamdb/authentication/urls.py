from django.urls import path, include

from authentication.views import get_or_create_user, get_token

app_name = 'authentication'

urlpatterns = [
    path('v1/auth/', include(
        [
            path('signup/', get_or_create_user, name='get_or_create_user'),
            path('token/', get_token, name='get_token'),
        ]
    )),
]
