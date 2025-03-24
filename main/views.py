import json
import qrcode
from django.shortcuts import render
from panel.models import Event, Customers
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
import threading
from django.contrib.auth.models import Group

def create_groups():
    Group.objects.get_or_create(name='Администраторы')
    Group.objects.get_or_create(name='Операторы QR')
# Create your views here.

def send_email(email, qr_path):
    msg2 = {'qrcode': qr_path}
    html_content = render_to_string("ticket_template/ticket.html", msg2)

    print('/n Отправленное письмо')
    msg = EmailMultiAlternatives(
        subject="Билет The HUB",
        body="Ваш билет на мероприятие",
        from_email="bighub.info@gmail.com",
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def index(request):
    if request.method == 'GET':
        events = Event.objects.all()
        print("сайт открыт")
        return render(request, 'main/index.html', {"events": events})
    if request.method == 'POST':
        data = json.loads(request.body)

        name = data.get('name')
        email = data.get('email')
        event = data.get('event_id')

        exists = Customers.objects.filter(name=name, email=email).exists()
        if exists:
            return JsonResponse({'exists': True})

        event_id = Event.objects.get(id=event)
        customer = Customers.objects.create(event=event_id, name=name, email=email)

        # event_id = Event.objects.get(id=event)
        # Customers.objects.create(event=event_id, name=name, email=email)
        print(f"{customer.uid}")
        print(f"Полученные данные: name={name}, email={email}, event_id={event}")

        qr = qrcode.make(f"{customer.uid}")
        qr_path = f"media/qrcodes/{customer.id}.png"
        qr.save(qr_path)
        # customers = Customers(event=event, name=name, email=Email)
        email_send = threading.Thread(target=send_email, args=(email, qr_path))
        email_send.start()

        # Customers.save()

        return JsonResponse({"success": True, "qr_code_url": f"/qrcodes/{customer.id}.png"})