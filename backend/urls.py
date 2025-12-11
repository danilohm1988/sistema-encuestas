from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
]

# En desarrollo, desactivamos CSRF para GraphQL
if settings.DEBUG:
    urlpatterns.append(
        path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
    )
else:
    urlpatterns.append(
        path('graphql/', GraphQLView.as_view(graphiql=False))
    )
