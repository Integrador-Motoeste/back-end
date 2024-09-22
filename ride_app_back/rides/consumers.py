import json
from channels.generic.websocket import AsyncWebsocketConsumer
from geopy.distance import geodesic
from .models import Ride
from ride_app_back.users.models import User
from ride_app_back.transactions.models import Invoice
from channels.db import database_sync_to_async
from django.http import JsonResponse

class RideQueueConsumer(AsyncWebsocketConsumer):
    pilots = {} 
    passengers = {}

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'request_ride':
            await self.request_ride(data)
        elif message_type == 'ride_request':
            await self.ride_request(data)
        elif message_type == 'respond_ride':
            await self.respond_ride(data)
        elif message_type == 'ride_response':
            await self.ride_response(data)
        elif message_type == 'confirm_pilot':
            await self.confirm_pilot(data)
        elif message_type == 'pilot_confirmed':
            await self.pilot_confirmed(data)
        elif message_type == "user_not_found":
            await self.user_not_found(data)
        elif message_type == "update_coords":
            await self.update_coords(data)
        elif message_type == "remove_coords":
            await self.remove_coords(data)

    async def update_coords(self, event):
        user_id = event['user_id']
        coords = event['coords']
        user_type = event['user_type']

        if user_type == 'pilot':
            self.pilots[user_id] = coords
        else:
            self.passengers[user_id] = coords

    async def remove_coords(self, event):
        user_id = event['user_id']
        user_type = event['user_type']

        if user_type == 'pilot':
            self.pilots.pop(user_id)
        else:
            self.passengers.pop(user_id)


    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        user_type = self.scope['url_route']['kwargs']['user_type']

        self.scope['session']['user_id'] = user_id
        self.scope['session']['user_type'] = user_type

        await self.channel_layer.group_add(user_id, self.channel_name)

        await self.accept()

        print(f"{user_type} {user_id} conectado com SID: {self.channel_name}")

    async def disconnect(self, close_code):
        user_type = self.scope['session']['user_type']
        user_id = self.scope['session']['user_id']

        await self.channel_layer.group_discard(str(user_id), self.channel_name)

        print(f"{user_type} {user_id} desconectado")

    async def request_ride(self, event):
        passenger_id = event['passenger_id']
        origin = event['origin']
        destination = event['destination']
        info = event['info']

        passenger_point = (origin['latitude'], origin['longitude'])
        nearby_pilots = []

        for pilot_id, pilot_coords in self.pilots.items():
            if pilot_coords:
                pilot_point = (pilot_coords['latitude'], pilot_coords['longitude'])
                distance = geodesic(passenger_point, pilot_point).km
                if distance <= 5:
                    nearby_pilots.append(pilot_id)

        for pilot_id in nearby_pilots:
            await self.channel_layer.group_send(
                str(pilot_id),
                {
                    'type': 'ride_request',
                    'passenger_id': passenger_id,
                    'origin': origin,
                    'destination': destination,
                    'info': info
                }
            )

    async def ride_request(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ride_request',
            'passenger_id': event['passenger_id'],
            'origin': event['origin'],
            'destination': event['destination'],
            'info': event['info']
        }))

    async def respond_ride(self, event):
        pilot_id = event['pilot_id']
        passenger_id = event['passenger_id']
        response = event['response']

        if response and str(passenger_id) in self.channel_layer.groups:
            await self.channel_layer.group_send(
                str(passenger_id),
                {
                    'type': 'ride_response',
                    'pilot_id': pilot_id,
                    'response': response
                }
            )
        else:
            await self.channel_layer.group_send(
                str(pilot_id),
                {
                    'type': 'user_not_found',
                    'response': False
                }
            )

    async def user_not_found(self, event):
        await self.send(text_data=json.dumps({
            'type': 'passenger_not_found',
            'response': event['response']
        }))

    async def ride_response(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ride_response',
            'pilot_id': event['pilot_id'],
            'response': event['response']
        }))

    async def confirm_pilot(self, event):
        pilot_id = event['pilot_id']
        response = event['response']
        ride_id = event['ride_id']

        if not response and 'cancel_type' in event:
            ride = await database_sync_to_async(Ride.objects.get)(id=ride_id)
            ride.status = "canceled"
            await database_sync_to_async(ride.save)()


        await self.channel_layer.group_send(
            str(pilot_id),
            {
                'type': 'pilot_confirmed',
                'pilot_id': pilot_id,
                'ride_id': ride_id,
                'response': response
            }
        )

    async def pilot_confirmed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'pilot_confirmed',
            'pilot_id': event['pilot_id'],
            'ride_id': event['ride_id'],
            'response': event['response']
        }))


class RideExecutionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        ride_id = self.scope['url_route']['kwargs']['ride_id']

        await self.channel_layer.group_add(ride_id, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        ride_id = self.scope['url_route']['kwargs']['ride_id']

        await self.channel_layer.group_discard(ride_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'change_pilot_position':
            await self.change_pilot_position(data)
        elif message_type == 'send_change_pilot_position':
            await self.send_change_pilot_position(data)
        elif message_type == 'confirm_boarding':
            await self.confirm_boarding(data)
        elif message_type == 'finish_ride':
            await self.finish_ride(data)
        elif message_type == 'send_finish_ride':
            await self.send_finish_ride(data)

    async def change_pilot_position(self, event):
        ride_id = event['ride_id']
        latitude = event['latitude']
        longitude = event['longitude']
        destination = event['destination']

        pilot_point = (latitude, longitude)
        destination_point = (destination.get('lat'), destination.get('lng'))
        distance = geodesic(destination_point, pilot_point).km
        if distance <= 0.020:
            ride = await database_sync_to_async(Ride.objects.get)(id=ride_id)
            ride.status = 'payment'
            await database_sync_to_async(ride.save)()
            await self.channel_layer.group_send(
                str(ride_id),
                {
                    'type': 'send_finish_ride',
                }
            )
        else:
            await self.channel_layer.group_send(
                str(ride_id),
                {
                    'type': 'send_change_pilot_position',
                    'latitude': latitude,
                    'longitude': longitude
                }
            )

    async def send_change_pilot_position(self, event):
        await self.send(text_data=json.dumps({
            'type': 'pilot_position',
            'latitude': event['latitude'],
            'longitude': event['longitude']
        }))

    async def confirm_boarding(self, event):
        ride_id = event['ride_id']
        ride = await database_sync_to_async(Ride.objects.get)(id=ride_id)
        ride.is_boarded = True
        await database_sync_to_async(ride.save)()

        await self.channel_layer.group_send(
            str(ride_id),
            {
                'type': 'send_confirm_boarding',
            }
        )

    async def send_confirm_boarding(self, event):
        await self.send(text_data=json.dumps({
            'type': 'confirm_boarding',
        }))

    async def send_finish_ride(self, event):
        await self.send(text_data=json.dumps({
            'type': 'finish_ride',
        }))


class PaymentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        ride_id = self.scope['url_route']['kwargs']['ride_id']

        await self.channel_layer.group_add(ride_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        ride_id = self.scope['url_route']['kwargs']['ride_id']

        await self.channel_layer.group_discard(ride_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        print(message_type, data)

        if message_type == 'confirmation':
            await self.confirmation(data)
        elif message_type == 'send_confirmation':
            await self.send_confirmation(data)


    async def confirmation(self, event):
        ride_id = event['ride_id']

        ride = await database_sync_to_async(Ride.objects.get)(id=ride_id)
        pilot_id = await database_sync_to_async(lambda: ride.pilot.id)()
        pilot = await database_sync_to_async(User.objects.get)(id=pilot_id)
        invoice = await database_sync_to_async(Invoice.objects.get)(ride=ride)

        await database_sync_to_async(lambda: setattr(ride, 'status', 'finished'))()
        await database_sync_to_async(lambda: setattr(invoice, 'status', 'completed'))()

        tax_value = (float(invoice.value) - 1.99) * 0.1
        await database_sync_to_async(lambda: setattr(pilot, 'balance', float(pilot.balance) + float(invoice.value) - tax_value))()

        await database_sync_to_async(ride.save)()
        await database_sync_to_async(invoice.save)()
        await database_sync_to_async(pilot.save)()


        await self.channel_layer.group_send(
            str(ride_id),
            {
                'type': 'send_confirmation',
            }
        )

    async def send_confirmation(self, event):
        await self.send(text_data=json.dumps({
            'type': 'confirmation',
        }))