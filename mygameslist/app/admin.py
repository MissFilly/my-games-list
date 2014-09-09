from django.contrib import admin
from .models import Company, Game, ListEntry, GameReview, GameRecommendation

admin.site.register(Company)
admin.site.register(Game)
admin.site.register(ListEntry)
admin.site.register(GameReview)
admin.site.register(GameRecommendation)
