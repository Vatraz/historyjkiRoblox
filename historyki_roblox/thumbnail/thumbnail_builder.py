import json
import os
import random

import cv2
import numpy as np
from PIL import ImageFont, Image, ImageFilter, ImageDraw, ImageOps

from historyki_roblox.character_factory import Character
from historyki_roblox.image_utils import cv2_to_PIL, PIL_to_cv2

THUMBNAIL_DATA_DIR_PATH = "./data/thumbnail"
ROBLOX_IMG_DIR_PATH = "./data/characters"
THUMBNAIL_SHAPE = (720, 1280)
ROBLOX_SHAPE = (370, 370)
EMOJI_SHAPE = (300, 300)


class ThumbnailBuilder:
    def __init__(self):
        self._phrase_font = self._load_phrase_font()
        self._name_font = self._load_name_font()
        self._thumbnail_data = self._load_thumbnail_data()

        self._thumbnail_img = self._create_thumbnail_base()

    def _load_thumbnail_data(self):
        with open(f"{THUMBNAIL_DATA_DIR_PATH}/thumbnail_data.json") as fp:
            data = json.load(fp)
        return data

    def _load_phrase_font(self):
        return ImageFont.truetype(
            f"{THUMBNAIL_DATA_DIR_PATH}/fonts/phrase.otf", size=65
        )

    def _load_name_font(self):
        return ImageFont.truetype(
            f"{THUMBNAIL_DATA_DIR_PATH}/fonts/phrase.otf", size=50
        )

    def _create_thumbnail_base(self) -> np.ndarray:
        img = np.zeros((*THUMBNAIL_SHAPE, 3), dtype=np.uint8)
        return img

    def get_result(self) -> np.ndarray:
        return self._thumbnail_img

    def add_background(self):
        img_pil = cv2_to_PIL(self._thumbnail_img)
        background_img = Image.open(f"{THUMBNAIL_DATA_DIR_PATH}/background/1.png")
        background_img = background_img.resize(THUMBNAIL_SHAPE[::-1])
        background_img = background_img.filter(ImageFilter.BLUR)
        img_pil.paste(background_img, (0, 0), background_img.convert("RGBA"))

        self._thumbnail_img = PIL_to_cv2(img_pil)
        return self

    def add_characters(self, characters: list[Character]):
        img_pil = cv2_to_PIL(self._thumbnail_img)

        step_y = int(ROBLOX_SHAPE[0] * 0.2)
        step_x = int(ROBLOX_SHAPE[1] * 0.6)
        text_offset_x = 10
        for idx, character in enumerate(characters):
            # characters
            char_img = Image.open(f"{ROBLOX_IMG_DIR_PATH}/{character.roblox_character}")
            char_img = char_img.resize(ROBLOX_SHAPE)
            px, py = idx * step_x, ROBLOX_SHAPE[1] // 2 - idx * step_y
            img_pil.paste(char_img, (px, py), char_img.convert("RGBA"))

            # names
            _, _, txt_w, txt_h = self._name_font.getbbox(character.name)
            txt_img = Image.new("RGBA", img_pil.size)
            d = ImageDraw.Draw(txt_img)
            d.text(
                (px + text_offset_x, py+step_y//2),
                character.name,
                font=self._name_font,
                fill="white",
                stroke_width=5,
                stroke_fill="red",
            )
            px, py = 0, 0
            img_pil.paste(txt_img, (px, py), txt_img)


        self._thumbnail_img = PIL_to_cv2(img_pil)

        return self

    def add_emoji(self):
        img_pil = cv2_to_PIL(self._thumbnail_img)
        emoji_file_name = random.choice(os.listdir(f"{THUMBNAIL_DATA_DIR_PATH}/emoji"))
        emoji_img = Image.open(f"{THUMBNAIL_DATA_DIR_PATH}/emoji/{emoji_file_name}")
        emoji_img = ImageOps.expand(emoji_img, emoji_img.size[0]//20, fill=0)
        emoji_img = emoji_img.resize(EMOJI_SHAPE)

        shadow_img_cv2 = PIL_to_cv2(emoji_img, alpha=True)
        bw = shadow_img_cv2[:, :, 3]
        contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            cv2.drawContours(shadow_img_cv2, [contour], -1, (0, 0, 255, 255), 20)

        emoji_shadow_img = cv2_to_PIL(shadow_img_cv2, alpha=True)

        # bottom right corner
        px, py = (
            THUMBNAIL_SHAPE[1] - EMOJI_SHAPE[1],
            THUMBNAIL_SHAPE[0] - EMOJI_SHAPE[0],
        )
        img_pil.paste(emoji_shadow_img, (px, py), emoji_shadow_img.convert("RGBA"))
        img_pil.paste(emoji_img, (px, py), emoji_img.convert("RGBA"))
        self._thumbnail_img = PIL_to_cv2(img_pil)

        return self

    def add_thumbnail_phrase_random(self):
        phrase = self._get_random_thumbnail_phrase()
        self._add_thumbnail_phrase(phrase)

        return self

    def _get_random_thumbnail_phrase(self) -> str:
        return random.choice(self._thumbnail_data["phrases"]).upper()

    def _add_thumbnail_phrase(self, phrase: str):
        img_pil = cv2_to_PIL(self._thumbnail_img)

        _, _, txt_w, txt_h = self._phrase_font.getbbox(phrase)
        txt_img = Image.new("RGBA", THUMBNAIL_SHAPE[::-1])
        d = ImageDraw.Draw(txt_img)
        d.text(
            ((THUMBNAIL_SHAPE[1] - txt_w) // 2, THUMBNAIL_SHAPE[0] // 2),
            phrase,
            font=self._phrase_font,
            fill="yellow",
            stroke_width=10,
            stroke_fill="red",
        )

        w = txt_img.rotate(22, expand=False)
        px, py = 0, 0
        img_pil.paste(w, (px, py), w)

        self._thumbnail_img = PIL_to_cv2(img_pil)

        return self

