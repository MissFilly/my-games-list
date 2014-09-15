from django.contrib import admin
from .models import Company, Game, ListEntry, GameReview, GameRecommendation, Genre, Platform

admin.site.register(Company)
admin.site.register(Game)
admin.site.register(ListEntry)
admin.site.register(GameReview)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(GameRecommendation)
