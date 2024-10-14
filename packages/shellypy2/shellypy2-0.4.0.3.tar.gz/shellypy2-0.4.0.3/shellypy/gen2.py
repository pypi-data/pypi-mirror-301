from typing import Any, Optional
from json.decoder import JSONDecodeError

from numpy import nan
from requests import post
from requests import Response
from requests.auth import HTTPDigestAuth

from .error import BadLogin, NotFound, BadResponse
from .base import _ShellyBase


class ShellyGen2(_ShellyBase):
    """
    Implements a general Class for interaction with Shelly devices of generation 2
    """

    def __init__(self, ip: str, port: int = 80, timeout: int = 5,
                 login: Optional[dict[str, str]] = None, debug: bool = False, init: bool = False) -> None:

        super().__init__(ip=ip, port=port, timeout=timeout, login=login, debug=debug, init=init)
        self.payload_id: int = 1
        self._generation: int = 2

    def update(self) -> None:

        status = self.settings()

        name: Optional[str] = status["device"].get("name", self._name)
        self._name: str = name if name is not None else "Device name not yet set!"
        self._type: str = status["device"].get("mac", self._type)

    def post(self, page: str, values: Optional[dict[str, Any]] = None) -> dict[str, Any]:

        url: str = f"{self._proto}://{self._hostname}:{self._port}/rpc"

        # increment payload id globally
        self.payload_id += 1
        # but keep a local copy around so we face no race conditions
        payload_id: int = self.payload_id

        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": payload_id, "method": page}

        if values:
            payload["params"] = values

        credentials: Optional[HTTPDigestAuth] = None
        try:
            credentials = HTTPDigestAuth('admin', self._credentials[1])
        except IndexError:
            pass

        response: Response = post(url, auth=credentials, json=payload, timeout=self._timeout)

        if response.status_code == 401:
            raise BadLogin()
        elif response.status_code == 404:
            raise NotFound("Not Found")

        try:
            response_data: dict[str, Any] = response.json()
        except JSONDecodeError:
            raise BadResponse("Bad JSON")

        if "error" in response_data:
            error_code: Optional[int] = response_data["error"].get("code", None)
            error_message: str = response_data["error"].get("message", "")

            if error_code == 401:
                raise BadLogin(error_message)
            elif error_code == 404:
                raise NotFound(error_message)
            else:
                raise BadResponse(f"{error_code}: {error_message}")

        if response_data["id"] != payload_id:
            raise BadResponse("invalid payload id was returned")

        return response_data.get("result", {})

    def status(self) -> dict[str, Any]:
        return self.post("Sys.GetStatus")

    def settings(self, subpage: Optional[str] = None) -> dict[str, Any]:
        return self.post("Sys.GetConfig")

    def meter(self, index: int) -> dict[str, Any]:
        raise NotImplementedError("Unavailable")

    def relay(self, index: int, timer: float = 0.0, turn: Optional[bool] = None) -> dict[str, Any]:

        values: dict[str, Any] = {"id": index}
        method: str = "Switch.GetStatus"
        if timer > 0.0:
            values["toggle_after"] = timer

        if turn is not None:
            method = "Switch.Set"

            if turn:
                values["on"] = True
            else:
                values["on"] = False

        return self.post(method, values)

    def roller(self, index: int, go: Optional[str] = None,
               roller_pos: Optional[int] = None, duration: Optional[int] = None) -> dict[str, Any]:

        method: str = ""
        values: dict[str, Any] = {
            "id": index
        }

        if go is not None:
            if go == "open":
                method = "Cover.Open"
            elif go == "close":
                method = "Cover.Close"
            elif go == "stop":
                method = "Cover.Stop"
            else:
                raise ValueError("Method is not open, close or stop")

        if roller_pos is not None:
            method = "Cover.GoToPosition"
            values["pos"] = self._clamp_percentage(roller_pos)

        if duration is not None:
            values["duration"] = duration

        return self.post(method, values)

    def light(self, index: int, mode: Optional[str] = None, timer: Optional[int] = None, turn: Optional[bool] = None,
              red: Optional[int] = None, green: Optional[int] = None, blue: Optional[int] = None,
              white: Optional[int] = None, gain: Optional[int] = None, temp: Optional[int] = None,
              brightness: Optional[int] = None) -> dict[str, Any]:
        raise NotImplementedError("Unavailable")

    def emeter(self, index: int) -> dict[str, Any]:
        raise NotImplementedError("Unavailable")

    def temperature(self, index: int, fahrenheit: bool = False) -> float:
        scale = "tF" if fahrenheit else "tC"
        temperature = self.post("Temperature.GetStatus", {"id": index}).get(scale, nan)
        return temperature

    def humidity(self, index: int) -> float:
        humidity = self.post("Humidity.GetStatus", {"id": index}).get("rh", nan)
        return humidity
