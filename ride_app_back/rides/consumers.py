import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RideConsumer(AsyncWebsocketConsumer):
    pilots = []  

    async def connect(self):
        user_type = self.scope['headers'][b'user-type'].decode('utf-8')
        user_id = self.scope['headers'][b'user-id'].decode('utf-8')

        self.scope['session']['user_type'] = user_type
        self.scope['session']['user_id'] = user_id

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
            await self.channel_layer.group_discard(user_id, self.channel_name)

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
            'passenger_id': event['passenger_id']
        }))

    async def respond_ride(self, event):
        pilot_id = event['pilot_id']
        passenger_id = event['passenger_id']
        response = event['response']

        await self.channel_layer.group_send(
            passenger_id,
            {
                'type': 'ride_response',
                'pilot_id': pilot_id,
                'response': response
            }
        )

    async def ride_response(self, event):
        await self.send(text_data=json.dumps({
            'pilot_id': event['pilot_id'],
            'response': event['response']
        }))
