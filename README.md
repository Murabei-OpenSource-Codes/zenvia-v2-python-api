# zenvia-v2-python-api
Python API to interact with Zenvia API

## Example
```
import os
from zenvia_v2_api.zenvia import ZenviaAPI


ZENVIA_API_TOKEN = os.getenv("ZENVIA_API_TOKEN")
zenvia_api = ZenviaAPI(token=ZENVIA_API_TOKEN)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


zenvia_api.webhook_create(
    event_type="MESSAGE",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp",
    criteria_direction="IN")

zenvia_api.webhook_create(
    event_type="MESSAGE",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp",
    criteria_direction="OUT")

zenvia_api.webhook_create(
    event_type="MESSAGE_STATUS",
    webhook_url=WEBHOOK_URL,
    webhook_headers={},
    criteria_channel="WhatsApp")

zenvia_api.whatsapp_send_text(
    msg_from='soft-harbor',
    msg_to='0000000000000',
    text='testando 1234')

zenvia_api.whatsapp_send_templated(
    msg_from='soft-harbor',
    msg_to='0000000000000',
    template_id="c5f3228e-3dd9-49be-9922-9f362ca5e089",
    fields={
        "name": "André",
        "productName": "Chuchu bem gostoso",
        "deliveryDate": "11/01/2023",
    })
```
