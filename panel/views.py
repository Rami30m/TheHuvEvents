from django.shortcuts import render
import json
from .models import Event, Customers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
# Create your views here.

@login_required
def index(request):
    if request.method == 'GET':
        events = Event.objects.all()
        print("сайт открыт")
        return render(request, 'panel/index.html', {"events": events})
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get("description")
        date = request.POST.get("date")
        location = request.POST.get("location")
        image = request.FILES.get("image")
        event = Event(title=title, description=description, date=date, location=location, image=image)
        event.save()

        if not title or not description:
            return JsonResponse({"success": False, "error": "Заполните все обязательные поля!"})

        return JsonResponse({"success": True})
    # else:
    #     return JsonResponse({"success": False, "error": "Только POST-запросы разрешены!"})

def DeleteEvent(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        event_id = data.get('event_id')
        # event = get_object_or_404(Event, id=event_id)
        event = Event.objects.get(id=event_id)
        print(event)
        event.delete()
        return JsonResponse({"success": True, "message": "Ивент удалён"})
    return JsonResponse({"success": False, "error": "Только DELETE-запрос разрешён"}, status=400)


@login_required
def lists(request):
    if request.method == 'GET':
        # events = Event.objects.all()
        # customers = Customers.objects.all()
        # customers_count = {event.id: event.Customers.count() for event in events}
        events = Event.objects.annotate(customers_count=Count("Customers"))
        return render(request, 'panel/lists.html', {"events": events})

@login_required
def ShowCustomers(request, event_id):
    if request.method == 'GET':
        # events = Event.objects.all()
        # customers = Customers.objects.all()
        event = Event.objects.get(id=event_id)
        customers = Customers.objects.filter(event=event)
        count = Customers.objects.filter(event=event, status="attended").count()
        return render(request, 'panel/customers.html', {'customers': customers, 'event': event, 'count': count})


@login_required
def change_status(request, event_id, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customers, id=customer_id, event_id=event_id)

        # Переключаем статус
        customer.status = 'attended' if customer.status == 'pending' else 'pending'
        customer.save()

    return redirect('ShowCustomers', event_id=event_id)



