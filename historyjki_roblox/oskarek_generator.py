import json
import os
import random
import uuid
from io import BytesIO
from typing import Optional

import requests
from lxml.html import fromstring
from PIL import Image

from historyjki_roblox.gpt_relayer import GtpRelayer
from historyjki_roblox.resource_manager import ResourceManager


class OskarekGenerator:
    def __init__(self, gpt_relayer: Optional[GtpRelayer] = None):
        self.gpt_relayer = gpt_relayer or GtpRelayer()
        self.resource_manager = ResourceManager()
        self.face_descriptions_data = self._load_face_descriptions_data()

    def _load_face_descriptions_data(self) -> dict:
        with open("data/oskareks/descriptions.json", "r") as f:
            descriptions = json.load(f)
        return descriptions

    def get_oskarek_from_openai(self, gender):
        description = random.choice(self.face_descriptions_data[gender])
        image_url = self.gpt_relayer.generate_image(description)
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image_name = f"{str(uuid.uuid4())}.{image.format}"
        self.resource_manager.save_oskarek_image(image, image_name)
        return image_name

    def get_oskarek_from_bing(self, gender: str) -> str:
        search = "instaboy" if gender == "MALE" else "instagirl"
        response = requests.get(
            "https://www.bing.com/images/search", params={"q": search}
        )
        html = fromstring(response.text)

        tmp = "m" if gender == "MALE" else "f"
        images = html.xpath(
            f"//*[contains(concat(' ', normalize-space(@class), ' '), ' mimg ')]"
        )
        for c, i in enumerate(images):
            src = i.get("src")
            if src is None:
                src = i.get("data-src")
            if src is None:
                continue
            image_response = requests.get(src)
            image_data = BytesIO(image_response.content)
            image = Image.open(image_data)
            image_format = image.format
            image_name = f"{tmp}{c}_bing.{image_format}"
            self.resource_manager.save_oskarek_image(image, image_name)
