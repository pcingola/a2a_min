import httpx
from httpx_sse import connect_sse
from typing import Any, AsyncIterable
from a2a_min.types import (
    AgentCard,
    GetTaskRequest,
    SendTaskRequest,
    SendTaskResponse,
    JSONRPCRequest,
    GetTaskResponse,
    CancelTaskResponse,
    CancelTaskRequest,
    SetTaskPushNotificationRequest,
    SetTaskPushNotificationResponse,
    GetTaskPushNotificationRequest,
    GetTaskPushNotificationResponse,
    A2AClientHTTPError,
    A2AClientJSONError,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    TaskIdParams,
    TaskPushNotificationConfig,
    TaskQueryParams,
    TaskSendParams,
)
import json


class A2AClient:
    def __init__(self, agent_card: AgentCard = None, url: str = None):
        if agent_card:
            self.url = agent_card.url
        elif url:
            self.url = url
        else:
            raise ValueError("Must provide either agent_card or url")

    async def send_task(self, task_send_params: TaskSendParams) -> SendTaskResponse:
        request = SendTaskRequest(params=task_send_params)
        return SendTaskResponse(**await self._send_request(request))

    async def send_task_streaming(
        self, payload: dict[str, Any]
    ) -> AsyncIterable[SendTaskStreamingResponse]:
        request = SendTaskStreamingRequest(params=payload)
        with httpx.Client(timeout=None) as client:
            with connect_sse(
                client, "POST", self.url, json=request.model_dump()
            ) as event_source:
                try:
                    for sse in event_source.iter_sse():
                        yield SendTaskStreamingResponse(**json.loads(sse.data))
                except json.JSONDecodeError as e:
                    raise A2AClientJSONError(str(e)) from e
                except httpx.RequestError as e:
                    raise A2AClientHTTPError(400, str(e)) from e

    async def _send_request(self, request: JSONRPCRequest) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                # Image generation could take time, adding timeout
                response = await client.post(
                    self.url, json=request.model_dump(), timeout=30
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise A2AClientHTTPError(e.response.status_code, str(e)) from e
            except json.JSONDecodeError as e:
                raise A2AClientJSONError(str(e)) from e

    async def get_task(self, task_query_params: TaskQueryParams) -> GetTaskResponse:
        request = GetTaskRequest(params=task_query_params)
        return GetTaskResponse(**await self._send_request(request))

    async def cancel_task(self, task_id_params: TaskIdParams) -> CancelTaskResponse:
        request = CancelTaskRequest(params=task_id_params)
        return CancelTaskResponse(**await self._send_request(request))

    async def set_task_callback(
        self, task_push_notification_config: TaskPushNotificationConfig
    ) -> SetTaskPushNotificationResponse:
        request = SetTaskPushNotificationRequest(params=task_push_notification_config)
        return SetTaskPushNotificationResponse(**await self._send_request(request))

    async def get_task_callback(
        self, task_id_params: TaskIdParams
    ) -> GetTaskPushNotificationResponse:
        request = GetTaskPushNotificationRequest(params=task_id_params)
        return GetTaskPushNotificationResponse(**await self._send_request(request))
