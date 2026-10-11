from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LiveRefreshConsumer(AsyncJsonWebsocketConsumer):
    group_prefix = ""
    token_kind = ""
    id_key = ""

    async def connect(self):
        identity = self.scope.get("websocket_identity") or {}
        object_id = int(self.scope["url_route"]["kwargs"][self.id_key])
        allowed_ids = {int(value) for value in identity.get("allowed_ids", [])}
        if identity.get("kind") != self.token_kind or object_id not in allowed_ids:
            await self.close(code=4403)
            return
        token_user_id = identity.get("user_id")
        connected_user = self.scope.get("user")
        if token_user_id is not None and (
            connected_user is None
            or not connected_user.is_authenticated
            or connected_user.pk != token_user_id
        ):
            await self.close(code=4403)
            return
        if token_user_id is None and identity.get("sender_type") not in {None, "public"}:
            await self.close(code=4403)
            return
        self.group_name = f"{self.group_prefix}-{object_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({"type": "chat.ready"})

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def chat_refresh(self, event):
        await self.send_json({"type": "chat.refresh"})

    async def receive_json(self, content, **kwargs):
        if content.get("action") in {"sync", "presence"}:
            await self.send_json({"type": "chat.ready"})
            return
        await self.send_json({"type": "chat.error", "error": "Use the protected HTTP action endpoint for chat actions."})


class EmergencyChatConsumer(LiveRefreshConsumer):
    group_prefix = "emergency-chat"
    token_kind = "emergency"
    id_key = "incident_id"


class CaseChatConsumer(LiveRefreshConsumer):
    group_prefix = "referral-chat"
    token_kind = "case"
    id_key = "referral_id"


class InHouseChatConsumer(LiveRefreshConsumer):
    group_prefix = "inhouse-chat"
    token_kind = "inhouse"
    id_key = "conversation_id"
