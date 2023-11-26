"""
Serializers for the recipe APIs
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag,
    Ingredient,
)

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients',
        ]
        read_only_fields = ['id']

    def _get_or_create_ingredients(self, ingredients, recipe):
        """Handle getting or creating ingredients as needed"""
        # the context is passed by the view when you're using the serializer
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,)
            recipe.ingredients.add(ingredient_obj)

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed"""
        # the context is passed by the view when you're using the serializer
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,)
            recipe.tags.add(tag_obj)

    # Tag are read only by default, so we need to handle the tag
    def create(self, validated_data):
        """Create ad recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        # Recipe model only expects only the values of recipe, tag is the related field
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        # empty list will call the _get_or_create_tags, but loop will not implement(it helps us with handling clear ingredients)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



# we use RecipeSerializer because RecipeDetailSerializer it's the extension of RecipeSerializer, so we dont need write repeat things.
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']

class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    # separate api for just handing image
    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs ={'image': {'required': True}}


