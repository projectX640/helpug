from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_emergency_chat_update(incident_id):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f"emergency-chat-{incident_id}",
        {"type": "chat.refresh"},
    )


def broadcast_case_chat_update(referral_id):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f"referral-chat-{referral_id}",
        {"type": "chat.refresh"},
    )


def broadcast_inhouse_chat_update(conversation_id):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f"inhouse-chat-{conversation_id}",
        {"type": "chat.refresh"},
    )


async def async_broadcast_emergency_chat_update(incident_id):
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        await channel_layer.group_send(
            f"emergency-chat-{incident_id}",
            {"type": "chat.refresh"},
        )


async def async_broadcast_case_chat_update(referral_id):
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        await channel_layer.group_send(
            f"referral-chat-{referral_id}",
            {"type": "chat.refresh"},
        )
