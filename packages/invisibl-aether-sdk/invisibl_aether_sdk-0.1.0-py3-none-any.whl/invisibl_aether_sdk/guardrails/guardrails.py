import os
import uuid
from typing import Union

from ..auth import Auth
from ..utils import Utils

logger = Utils.setup_logger(__name__)


class Guardrails:
    def __init__(self) -> None:
        self.url: str = os.getenv("AETHER_BASE_URL") + "/guardrails"
        auth_response = Auth.get_authenticated_ids()
        self.user_id = auth_response.get("user_id")
        self.request_payload: dict = {
            "user_id": self.user_id,
        }
        route = "/check-policy"
        self.headers = {"api-key": auth_response.get("api_key")}
        response = Utils.send_api_request(
            method="POST",
            url=self.url + route,
            request_payload=self.request_payload,
            auth=True,
            headers=self.headers,
        )
        if not response.content:
            raise Exception(
                "There is no policy configured for "
                f"{self.project_id}/{self.team_id}/{self.user_id}."
            )

    def validate(
        self,
        user_prompt: str,
        validation_type: str,
        llm_response: str = "",
        check_all: bool = True,
        trace_id: Union[str, None] = None,
    ) -> dict:
        trace_id = trace_id or str(uuid.uuid4())

        route: str = "/validate-policy"
        self.user_prompt = user_prompt
        if not isinstance(self.user_prompt, str):
            self.user_prompt = str(self.user_prompt)

        payload: dict = {
            "user_prompt": self.user_prompt,
            "llm_response": llm_response,
            "validation_type": validation_type,
            "check_all": check_all,
            "trace_id": trace_id,
        }
        payload.update(self.request_payload)

        try:
            response = Utils.send_api_request(
                method="POST",
                url=self.url + route,
                request_payload=payload,
                auth=True,
                timeout=302,
                headers=self.headers,
            )
            if response.status_code == 200:
                response = response.json()
                response.update({"trace_id": trace_id})
            else:
                response = {"status": response.status_code, "detail": response.text}
            return response

        except Exception as e:
            logger.info(e)
            raise Exception(
                "Sorry! Something went wrong. Please check your inputs."
            ) from e
