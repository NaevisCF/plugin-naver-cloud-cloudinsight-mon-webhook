import logging
import json
from plugin.manager.event_manager.base import ParseManager

_LOGGER = logging.getLogger("spaceone")


class IntegrationManager(ParseManager):
    webhook_type = "Integration"

    def parse(self, raw_data: dict) -> dict:
        """

        :param raw_data:
        :return EventResponse:
            "results": EventResponse
        """
        results = []

        _LOGGER.debug(f"[AWSPersonalHealthDashboard] parse => {json.dumps(raw_data, indent=2)}")

        #event_type_category = raw_data.get("detail", {}).get("eventTypeCategory", "")

        event: dict = {
            'event_key': self.generate_event_key(raw_data),
            'event_type': self.get_event_type(raw_data),
            'severity': self.get_severity(raw_data),
            #'resource': self._get_resource(raw_data),#not required
            'title': self._change_string_format(raw_data),
            #'rule': raw_data.get("ruleName"),#not required
            'description': raw_data.get("text"),
            'occurred_at': self.convert_to_iso8601(raw_data.get("startTime")),
            'additional_info': self.get_additional_info(raw_data)
        }

        results.append(event)
        _LOGGER.debug(f"[Ncloud_Webhook] parse => {event}")

        return {
            "results": results
        }

    def generate_event_key(self, raw_data: dict) -> str:
        return raw_data.get("id")

    def get_event_type(self, raw_data: dict) -> str:
        return raw_data.get("type")

    def get_severity(self, raw_data: dict) -> str:
        if raw_data.get("eventLevel") is not None:
            return raw_data.get("eventLevel")
        else:
            return "INFO"

    @staticmethod
    def _change_string_format(raw_data):
        return raw_data.get("name")

    @staticmethod
    def get_additional_info(raw_data: dict) -> dict:
        additional_info = {
            "url": raw_data.get("url")
        }

        return additional_info


    @staticmethod
    def _get_resource(raw_data: dict) -> dict:
        key = ["RESOURCE_NAME"]
        if key in raw_data:
            return {
                    "name" : raw_data[key]
            }
        else:
            return {"name": "Undefined"}
