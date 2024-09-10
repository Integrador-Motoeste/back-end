import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideQueueConsumer(AsyncWebsocketConsumer):
    pilots = []  

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

    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        user_type = self.scope['url_route']['kwargs']['user_type']

        self.scope['session']['user_id'] = user_id
        self.scope['session']['user_type'] = user_type

        if user_type == 'pilot':
            self.pilots.append(user_id)
            await self.channel_layer.group_add('pilots', self.channel_name)

        await self.channel_layer.group_add(user_id, self.channel_name)

        await self.accept()

        print(f"{user_type} {user_id} conectado com SID: {self.channel_name}")

    async def disconnect(self, close_code):
        user_type = self.scope['session']['user_type']
        user_id = self.scope['session']['user_id']

        if user_type == 'pilot':
            self.pilots.remove(user_id)
            await self.channel_layer.group_discard('pilots', self.channel_name)
        else:
            await self.channel_layer.group_discard(str(user_id), self.channel_name)

        print(f"{user_type} {user_id} desconectado")

    async def request_ride(self, event):
        passenger_id = event['passenger_id']
        await self.channel_layer.group_send(
            'pilots',
            {
                'type': 'ride_request',
                'passenger_id': passenger_id
            }
        )

    async def ride_request(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ride_request',
            'passenger_id': event['passenger_id']
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
    users = []

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

    async def change_pilot_position(self, event):
        ride_id = event['ride_id']
        latitude = event['latitude']
        longitude = event['longitude']

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