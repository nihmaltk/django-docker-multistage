from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'cooking_time', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'ingredients')
