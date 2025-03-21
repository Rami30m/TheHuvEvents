import json
import qrcode
from django.shortcuts import render
from panel.models import Event, Customers
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
# Create your views here.

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

        msg2 = {'qrcode': qr_path}
        html_content = render_to_string("ticket_template/ticket.html", msg2)
        # html_content = "<h1>Ваш билет на The HUB</h1><p>Вот ваш QR-код:</p>"
        # print("Содержимое HTML-письма:\n", html_content)

        print('/n Отправленное письмо')
        msg = EmailMultiAlternatives(
            subject="Билет The HUB",
            body="Ваш билет на мероприятие",
            from_email="bighub.info@gmail.com",
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        # Customers.save()

        return JsonResponse({"success": True, "qr_code_url": f"/qrcodes/{customer.id}.png"})