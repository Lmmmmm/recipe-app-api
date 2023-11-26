"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from recipe import views

# If your view is based on a ViewSet,
# you can use DefaultRouter or another router to automatically generate a URL pattern for your view set
router = DefaultRouter()
router.register('recipe', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

# These auto-generated URL patterns are then added to urlpatterns via include(router.urls).
urlpatterns = [
    path('', include(router.urls)),
]