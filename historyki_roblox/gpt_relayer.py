import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


class GtpRelayerException(Exception):
    pass


class GtpRelayer:
    def simply_ask(self, message: str) -> str:
        chat_messages = [self._create_message(message)]
        try:
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=chat_messages
            )
            answer = chat["choices"][0]["message"]["content"]
        except Exception as exe:
            raise GtpRelayerException(
                f"Failed to fetch ChatGTP response: {message}"
            ) from exe
        return answer

    def _create_message(self, message: str) -> dict:
        return {"role": "user", "content": message}
