import os
from zenvia_v2_api.zenvia import ZenviaAPI


ZENVIA_API_TOKEN = os.getenv("ZENVIA_API_TOKEN")
self = ZenviaAPI(token=ZENVIA_API_TOKEN)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


self.webhook_create(
    event_type="MESSAGE",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp",
    criteria_direction="IN")

self.webhook_create(
    event_type="MESSAGE",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp",
    criteria_direction="OUT")

self.webhook_create(
    event_type="MESSAGE_STATUS",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp")

self.whatsapp_send_text(
    msg_from='soft-harbor',
    msg_to='5511974510831',
    text='testando 1234')

self.whatsapp_send_templated(
    msg_from='soft-harbor',
    msg_to='5511974510831',
    template_id="c5f3228e-3dd9-49be-9922-9f362ca5e089",
    fields={
        "name": "André",
        "productName": "Chuchu bem gostoso",
        "deliveryDate": "11/01/2023",
    })
