from django.shortcuts import render
from .models import GameReview, GameRecommendation


def home(request):
    reviews = GameReview.objects.order_by('-date_created')[:6]
    recommendations = GameRecommendation.objects.order_by('-date_created')[:6]
    context = dict(reviws=reviews, recommendations=recommendations)
    return render(request, 'index.html')
