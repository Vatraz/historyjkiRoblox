import base64
import os
import json
from typing import NamedTuple, Optional

import requests

from historyjki_roblox.resource_manager import ResourceManager


class VoiceGeneratorException(Exception):
    pass


class Voice(NamedTuple):
    name: str
    pitch: float
    speaking_rate: int

    @classmethod
    def from_json(cls, data) -> "Voice":
        return Voice(
            name=data["name"],
            pitch=data["speaking_rate"],
            speaking_rate=data["speaking_rate"],
        )


class VoiceGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.resource_manager = ResourceManager()
        self.api_key = api_key or self.resource_manager.get_gtts_api_key()
        self.base_url = "https://texttospeech.googleapis.com/v1"

    def synthesize(self, text: str, voice: Voice) -> str:
        # valid speaking_rate is between 0.25 and 4.0.
        # Out of range: valid pitch is between -20.0 and 20.0.
        filepath = self.resource_manager.get_dialogue_path(
            f"{voice.name}-{voice.pitch}-{voice.speaking_rate}",
            "".join(filter(str.isalpha, text)),
        )
        if os.path.exists(filepath):
            return filepath

        body = {
            "audioConfig": {
                "audioEncoding": "MP3",
                "pitch": voice.pitch,
                "speakingRate": voice.speaking_rate,
            },
            "input": {"text": text},
            "voice": {"languageCode": "pl-PL", "name": voice.name},
        }
        params = {"key": self.api_key}
        response = requests.post(
            f"{self.base_url}/text:synthesize", params=params, json=body
        )
        if response.status_code != 200:
            raise VoiceGeneratorException(
                f"response status code: {response.status_code}\n{response.text}"
            )

        with open("ggts.json", "w") as f:
            json.dump(response.json(), f)

        binary_data = base64.b64decode(response.json()["audioContent"].encode())
        with open(filepath, "wb") as f:
            f.write(binary_data)

        return filepath
