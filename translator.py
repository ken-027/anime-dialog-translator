import os
import requests
from IPython.display import Markdown, display, update_display
from anthropic import Anthropic
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from exceptions import RateLimitError

load_dotenv(override=True)

anthropic_key = os.getenv('ANTHROPIC_API_KEY')
openai_key = os.getenv('OPENAI_API_KEY')
request_token = os.getenv('REQUEST_TOKEN')
ratelimit_api = os.getenv('RATELIMIT_API')

CLAUDE_MODEL = "claude-3-haiku-20240307"
OPENAI_MODEL = "gpt-4o-mini"

anthropic = Anthropic(api_key=anthropic_key)
openai = OpenAI(api_key=openai_key)

class DialogTranslator():
    def __prompt(self, transcript):
        system_prompt = """
            You are a translation assistant that translates Japanese dialogue from anime into two languages: English and Filipino (Tagalog).
            For each spoken line, follow this format in Markdown:

            **Original Japanese (Romaji)**: {romaji_transcription_here}

            **Translated to English**: english_translation_here

            **Translated to Filipino (Tagalog)**: filipino_translation_here

            Make sure:
            - The Romaji is accurate and phonetically reflects the original Japanese audio.
            - The English translation is natural and contextually appropriate.
            - The Filipino translation is conversational and culturally adapted where needed.
            - Maintain respectful or emotional tone based on the speaker’s intent in the anime.
            - Use proper punctuation and spacing for each line to make it easy to read.
        """

        user_prompt = f"Here is the transcript japanese audio and translate it into two languages: '{transcript}'. No explanation just the translated languages only."

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]


    def __transcript(self, file):
        audio_file = open(file, "rb")

        _transcript = openai.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format="text",
            language="ja"
        )

        return _transcript


    def translate(self, file):
        try:
            yield "converting audio..."
            # implementation of ratelimiter here
            response = requests.post(
                ratelimit_api,
                headers={
                    "custom-header": request_token
                }
            )
            status_code = response.status_code

            if (status_code == 429):
                raise RateLimitError()

            elif (status_code != 201):
                raise Exception(f"Unexpected status code from rate limiter: {status_code}")

            transcript = self.__transcript(file)

            yield "translating text..."
            messages = self.__prompt(transcript)
            system_prompt = system=messages[0]["content"]
            user_prompt = system=messages[1]

            text = ""

            with anthropic.messages.stream(model=CLAUDE_MODEL, max_tokens=1024, system=system_prompt, messages=[user_prompt]) as stream:
                for chunk in stream.text_stream:
                    text += chunk
                    yield text

        except Exception as err:
            return str(err)
