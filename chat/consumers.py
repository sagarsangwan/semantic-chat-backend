# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
#         self.room_group_name = f"chat_{self.room_id}"

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         sender = data["sender"]
#         timestamp = data["timestamp"]
#         sentiment = data.get("sentiment")
#         # Broadcast to group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat_message",
#                 "message": message,
#                 "sender": sender,
#                 "timestamp": timestamp,
#                 "sentiment": sentiment,
#             },
#         )

#     async def chat_message(self, event):
#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "message": event["message"],
#                     "sender": event["sender"],
#                     "timestamp": event["timestamp"],
#                     "sentiment": event["sentiment"],
#                 }
#             )
#         )

#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
