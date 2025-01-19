from django.shortcuts import render
from .models import Room,Message
from django.http import JsonResponse
from .sentiment import analyze_sentiment
import json

def rooms(request):
    rooms=Room.objects.all()
    return render(request, "rooms.html",{"rooms":rooms})

def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request, "room.html",{"room_name":room_name,"slug":slug,'messages':messages})

def get_sentiment_score(request):
    """
    Handle AJAX request for sentiment analysis.
    """
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            score = analyze_sentiment(text)
            return JsonResponse({'score': score})
        return JsonResponse({'error': 'No text provided'}, status=400)