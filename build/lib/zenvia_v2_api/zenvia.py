"""Class for comunication with Zenvia V2 API."""
import requests
import validators
import simplejson as json
from urllib.parse import urljoin
from zenvia_v2_api.exceptions import (
    ZenviaAPIException, ZenviaAPIRequestException,
    ZenviaAPIFunctionValidation)
from typing import Any


class ZenviaAPI:
    """Class for comunication with Zenvia v2 API."""

    API_HOST = "https://api.zenvia.com/v2/"

    def __init__(self, token: str):
        """
        __init__.

        Args:
            token [str]: Token for Zenvia API authentication calls.
        Return:
            ZenviaAPI object.
        """
        self._token = token

    def get_auth_header(self) -> dict:
        """
        Return header dictionary with authentication.

        Args:
            No Args.
        Kwargs:
            No Kwargs.
        Return [dict]:
            Return a dictionary with "X-API-Token" key.
        """
        return {
            "X-API-Token": self._token
        }

    def request_get(self, endpoint: str, params: dict = {}, **kwargs) -> Any:
        """
        Make get request at Zenvia v2 API.

        Args:
            endpoint [str]: End-point for Zenvia API.
            params [dict]: Get parameters passed to request.get function.
        Kwargs:
            params [dict]: Parameters passed to request.get function.
            **kwargs: Extra arguments passed to request.get function.
        Return [Any]:
            Request return on python native variables.
        """
        url = urljoin(self.API_HOST, endpoint)
        auth_header = self.get_auth_header()
        try:
            response = requests.get(
                url, headers=auth_header, params=params,
                **kwargs)
            response.raise_for_status()
        except Exception as e:
            raise ZenviaAPIRequestException(str(e))

        return response.json()

    def request_post(self, endpoint: str, params: dict = {}, data: dict = {},
                     **kwargs) -> Any:
        """
        Make post request at Zenvia v2 API.

        Args:
            endpoint [str]: End-point for Zenvia API.
            params [dict]: Get parameters passed to request.get function.
        Kwargs:
            params [dict]: Parameters passed to request.get function.
            **kwargs: Extra arguments passed to request.get function.
        Return [Any]:
            Request return on python native variables.
        """
        url = urljoin(self.API_HOST, endpoint)
        auth_header = self.get_auth_header()
        try:
            response = requests.post(
                url, headers=auth_header, params=params, json=data,
                **kwargs)
        except Exception as e:
            raise ZenviaAPIRequestException(str(e))

        if not response.ok:
            msg = (
                "Request reponse with error status[{status}]:\n{text}"
            ).format(
                status=response.status_code,
                text=json.dumps(response.json(), indent=2))
            raise ZenviaAPIRequestException(msg)

        return response.json()

    def request_delete(self, endpoint: str, params: dict = {},
                       **kwargs) -> Any:
        """
        Make delete request at Zenvia v2 API.

        Args:
            endpoint [str]: End-point for Zenvia API.
            params [dict]: Get parameters passed to request.get function.
        Kwargs:
            params [dict]: Parameters passed to request.get function.
            **kwargs: Extra arguments passed to request.get function.
        Return [Any]:
            Request return on python native variables.
        """
        url = urljoin(self.API_HOST, endpoint)
        auth_header = self.get_auth_header()
        try:
            response = requests.delete(
                url, headers=auth_header, params=params,
                **kwargs)
            response.raise_for_status()
        except Exception as e:
            raise ZenviaAPIRequestException(str(e))

        return response.json()

    def webhook_list(self, **kwargs) -> list:
        """
        List all avaiable webhooks.

        Args:
            No Args.
        Kwargs:
            **kwargs: Extra arguments passed to request.get function.
        Return [list]:
            List of dictionary with registred webhooks.

            Zenvia API Doc:
            https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Webhooks/paths/~1subscriptions/get

            Example:
            {
                "id": "string",
                "eventType": "MESSAGE",
                "webhook": {
                    "url": "string",
                    "headers": { }
                },
                "status": "ACTIVE",
                "version": "v1",
                "createdAt": "string",
                "updatedAt": "string",
                "criteria": {
                    "channel": "string",
                    "direction": "IN"
                }
            }
        """
        return self.request_get(endpoint="subscriptions", **kwargs)

    def webhook_retrieve(self, id: int, **kwargs) -> dict:
        """
        Retrieve one webhook using its id.

        Args:
            id [int]: Id of the webhook to retrieved.
        Kwargs:
            **kwargs: Extra arguments passed to request.get function.
        Return [dict]:
            A dictionary with registred webhook with id passed as argument.

            Zenvia API Doc:
            https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Webhooks/paths/~1subscriptions~1%7BsubscriptionId%7D/get

            Example:
            {
                "id": "string",
                "eventType": "MESSAGE",
                "webhook": {
                    "url": "string",
                    "headers": { }
                },
                "status": "ACTIVE",
                "version": "v1",
                "createdAt": "string",
                "updatedAt": "string",
                "criteria": {
                    "channel": "string",
                    "direction": "IN"
                }
            }
        """
        endpoint = "subscriptions/{}".format(int(id))
        return self.request_get(endpoint=endpoint, **kwargs)

    def webhook_delete(self, id: int, **kwargs) -> list:
        """
        Delete one webhook using its id.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Webhooks/paths/~1subscriptions~1%7BsubscriptionId%7D/delete

        Args:
            id [int]: Id of the webhook to retrieved.
        Kwargs:
            **kwargs: Extra arguments passed to request.get function.
        Return [list]:
            List of dictionary with registred webhooks.

            Example:
            {
                "id": "string",
                "eventType": "MESSAGE",
                "webhook": {
                    "url": "string",
                    "headers": { }
                },
                "status": "ACTIVE",
                "version": "v1",
                "createdAt": "string",
                "updatedAt": "string",
                "criteria": {
                    "channel": "string",
                    "direction": "IN"
                }
            }
        """
        endpoint = "subscriptions/{}".format(int(id))
        return self.request_delete(endpoint=endpoint, **kwargs)

    def webhook_create(self, event_type: str, webhook_url: str,
                       webhook_headers: dict, criteria_channel: str,
                       criteria_direction: str = None,
                       status: str = 'ACTIVE'):
        """
        Create a webhook.

        Webhooks will make calls to {webhook_url} using {webhook_headers} as
        headers that may have authentication.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Webhooks/paths/~1subscriptions/post

        Args:
            event_type [str]: Type of event that will be listened, it may
                have values in: MESSAGE, will call if new messages are received
                on especified channel; MESSAGE_STATUS, will make a call if
                sent messages changes their status (delivered, read, etc, ...).
            webhook_url [str]: Url to be called when webhook criteria is met.
            webhook_headers [str]: Headers used to call {webhook_url}.
            criteria_channel [str]: Channel to listen to.

        Kwargs:
            status [str]: Status of the webhook when create, must be in
                ["ACTIVE", "DEGRADED", "INACTIVE"]
            criteria_direction [str]: Used when event_type='MESSAGE', it can
                be set as "IN" or "OUT", Indicates whether is received from a
                channel (IN) or sent to a channel (OUT).
        """
        # Validation of function parameters
        if event_type not in ["MESSAGE", "MESSAGE_STATUS"]:
            raise ZenviaAPIFunctionValidation(
                "event_type not in [MESSAGE, MESSAGE_STATUS]")

        if status is not None:
            if status not in ["ACTIVE", "DEGRADED", "INACTIVE"]:
                raise ZenviaAPIFunctionValidation(
                    "status not in [ACTIVE, DEGRADED, INACTIVE]")

        if event_type == "MESSAGE":
            if criteria_direction is None:
                raise ZenviaAPIFunctionValidation(
                    "event_type == MESSAGE and criteria_direction is None")
            if criteria_direction not in ["IN", "OUT"]:
                raise ZenviaAPIFunctionValidation(
                    "criteria_direction not in [IN, OUT]")

        val_webhook_url = validators.url(webhook_url)
        if not val_webhook_url:
            raise ZenviaAPIFunctionValidation(
                "webhook_url is not a well formated url")

        data = {}
        if event_type == "MESSAGE":
            data = {
                "eventType": "MESSAGE",
                "webhook": {
                    "url": webhook_url,
                    "headers": webhook_headers,
                },
                "status": status,
                "version": "v2",
                "criteria": {
                    "channel": criteria_channel,
                    "direction": criteria_direction
                }
            }
        elif event_type == "MESSAGE_STATUS":
            data = {
                "eventType": "MESSAGE_STATUS",
                "webhook": {
                    "url": webhook_url,
                    "headers": webhook_headers,
                },
                "status": status,
                "version": "v2",
                "criteria": {
                    "channel": criteria_channel,
                }
            }
        else:
            raise ZenviaAPIFunctionValidation(
                "event_type not avaiable: {}".format(event_type))
        return self.request_post(endpoint="subscriptions", data=data)

    def whatsapp_send_text(self, msg_from: str, msg_to: str, text: str):
        """
        Send a WhatsApp message with free text.

        It is only possible to send a free text after the recipient respond
        a template formated message.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/WhatsApp/paths/~1channels~1whatsapp~1messages/post

        Args:
            msg_from [str]: The identifier of the sender of the message. The
                sender is created when an integration for the channel is
                connected on the integrations console.
            msg_to [str]: The identifier of the recipient (varies according to
                the channel) of the message. More details on the channel's
                sender and recipient section.
            text [str]: Text to be sent. When a URL is sent in the text,
                a URL preview will be added to the message, if the channel
                supports it.
        """
        data = {
            "from": msg_from,
            "to": msg_to,
            "contents": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
        return self.request_post(
            endpoint="channels/whatsapp/messages",
            data=data)

    def whatsapp_send_templated(self, msg_from: str, msg_to: str,
                                template_id: str, fields: dict):
        """
        Send a templated message to recipient.

        Templated message must be used to start a conversation. Free text
        message may only be sent if recipient respond a template one, and
        only for 24 hours after that.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/WhatsApp/paths/~1channels~1whatsapp~1messages/post

        Args:
            msg_from [str]: The identifier of the sender of the message. The
                sender is created when an integration for the channel is
                connected on the integrations console.
            msg_to [str]: The identifier of the recipient (varies according to
                the channel) of the message. More details on the channel's
                sender and recipient section.
            template_id [str]: The template identifier. Click here to go to
                the template page.
            fields [dict]: The available fields to be used in this template.
        """
        data = {
            "from": msg_from,
            "to": msg_to,
            "contents": [
                {
                    "type": "template",
                    "templateId": template_id,
                    "fields": fields
                }
            ]
        }
        return self.request_post(
            endpoint="channels/whatsapp/messages",
            data=data)

    def template_list(self, channel: str = None, sender_id: str = None,
                      status: str = None, **kwargs) -> list:
        """
        List all templates.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Templates/paths/~1templates/post

        Args:
            No Args.
        Kwargs:
            channel [str]: Query templates in channel. Must be in ["WHATSAPP",
                "SMS", "RCS", "EMAIL"].
            sender_id [str]: Sender's templates.
            status [str]: Query templates with status. Must be in [
                "WAITING_REVIEW" "REJECTED" "WAITING_APPROVAL" "APPROVED"
                "PAUSED" "DISABLED"]
        Return:
            List all template on Zenvia.
        """
        query_params = {}
        if channel is not None:
            if channel not in ["WHATSAPP", "SMS", "RCS", "EMAIL"]:
                pass
            else:
                query_params["channel"] = channel

        if status is not None:
            if status not in ["WAITING_REVIEW", "REJECTED", "WAITING_APPROVAL",
                              "APPROVED", "PAUSED", "DISABLED"]:
                pass
            else:
                query_params["status"] = status

        if sender_id is not None:
            query_params["senderId"] = sender_id

        return self.request_get(
            endpoint="templates", params=query_params,
            **kwargs)

    def template_retrieve(self, id: str, **kwargs) -> dict:
        """
        Retrieve a template using its it.

        Zenvia API Doc:
        https://zenvia.github.io/zenvia-openapi-spec/v2/#tag/Templates/paths/~1templates/post

        Args:
            id [str]: ID associated with the template.
        Kwargs:
            No Kwargs.
        Return:
            Return a template from Zenvia.
        """
        endpoint = "templates/{}".format(id)
        return self.request_get(endpoint=endpoint, **kwargs)
