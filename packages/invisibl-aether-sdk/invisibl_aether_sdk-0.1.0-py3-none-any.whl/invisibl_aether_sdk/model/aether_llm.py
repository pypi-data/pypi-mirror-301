"""Chat LLMs with Aether's Guardrails and Hallucinations, along with governance."""

from typing import Literal, Union, Optional
import os

from ..auth import Auth
from ..utils import Utils


class AetherLlm:
    def __init__(
        self,
        guardrails: bool = False,
        default_llm_provider: Literal["azure", "google", "openai", "aws"] = "azure",
        profile="default",
    ) -> None:
        self.ids = Auth.get_authenticated_ids(profile)
        self.default_llm_provider = default_llm_provider
        self.guardrails = guardrails
        self.url: str = os.getenv("AETHER_BASE_URL") + "/model"

    def invoke(
        self,
        prompt: str,
        llm_provider: Union[Literal["azure", "google", "openai", "aws"], None] = None,
        model_name: Optional[str] = None,
        hallucination_type: Union[str, None] = None,
        hallucination_params: dict = {},
        llm_param_overrides: dict = {},
    ):
        payload = {
            "user_id": self.ids.get("user_id"),
            "prompt": prompt,
            "guardrails": self.guardrails,
            "hallucination_type": hallucination_type,
            "hallucination_params": hallucination_params,
            "llm_param_overrides": llm_param_overrides,
            "llm_provider": llm_provider or self.default_llm_provider,
            "model_name": model_name,
        }

        route = "/invoke"
        self.headers = {"api-key": self.ids.get("api_key")}

        try:
            response = Utils.send_api_request(
                method="POST",
                url=self.url + route,
                request_payload=payload,
                auth=True,
                headers=self.headers,
            )
            if response.status_code == 200:
                response = response.json()
            else:
                response = {"status": response.status_code, "detail": response.text}
            return response

        except Exception as e:
            raise Exception(
                "Sorry! Something went wrong. Please check your inputs. "
            ) from e
