from channels.generic.websocket import AsyncWebsocketConsumer


class SecurityConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        session_key = self.scope["session"].session_key
        if not session_key:
            await self.close()
            return

        self.group_name = f"session_{session_key}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

    async def force_logout(self, event):
        await self.send_json({
            "type": "force_logout"
        })