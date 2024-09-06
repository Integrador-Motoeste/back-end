import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideQueueConsumer(AsyncWebsocketConsumer):
    pilots = []  

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'request_ride':
            await self.request_ride(data)
        if message_type == 'ride_request':
            await self.ride_request(data)
        if message_type == 'respond_ride':
            await self.respond_ride(data)
        if message_type == 'ride_response':
            await self.ride_response(data)

    async def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        user_type = self.scope['url_route']['kwargs']['user_type']

        self.scope['session']['user_id'] = user_id
        self.scope['session']['user_type'] = user_type


        if user_type == 'pilot':
            self.pilots.append(user_id)
            await self.channel_layer.group_add('pilots', self.channel_name)
        else:
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
        print("ride_request")
        await self.send(text_data=json.dumps({
            'type': 'ride_request',
            'passenger_id': event['passenger_id']
        }))

    async def respond_ride(self, event):
        pilot_id = event['pilot_id']
        passenger_id = event['passenger_id']
        response = event['response']

        if response:
            await self.channel_layer.group_send(
                str(passenger_id),
                {
                    'type': 'ride_response',
                    'pilot_id': pilot_id,
                    'response': response
                }
            )

    async def ride_response(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ride_response',
            'pilot_id': event['pilot_id'],
            'response': event['response']
        }))
