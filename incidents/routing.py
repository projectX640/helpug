from django.urls import path

from .consumers import CaseChatConsumer, EmergencyChatConsumer, InHouseChatConsumer


websocket_urlpatterns = [
    path("ws/chat/incidents/<int:incident_id>/", EmergencyChatConsumer.as_asgi(), name="emergency_chat_socket"),
    path("ws/institution/chat/<int:referral_id>/", CaseChatConsumer.as_asgi(), name="case_chat_socket"),
    path("ws/inhouse/chat/<int:conversation_id>/", InHouseChatConsumer.as_asgi(), name="inhouse_chat_socket"),
]
