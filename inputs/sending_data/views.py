from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
import sqlite3

from .models import Client
from .services import bot, list_of_tuples_to_list_of_items


class ContactWithUs(APIView):
    def post(self, request: Request) -> Response:
        data = request.data
        client_name = data["client_name"]
        client_phone = data["client_phone"]

        client = Client.objects.create(name=client_name, phone_number=client_phone)
        client.save()

        # Отправка сообщения в тг бот
        message = f"Новый клиент!\nИмя: {client_name}\nНомер телефона: {client_phone}"
        conn = sqlite3.connect('admins.sqlite3')
        cur = conn.cursor()
        admins_ids = list_of_tuples_to_list_of_items(list(cur.execute("SELECT chat_id FROM admins")))
        for admin_id in admins_ids:
            bot.send_message(admin_id, message)
        cur.close()
        conn.close()

        return Response(status.HTTP_201_CREATED)
