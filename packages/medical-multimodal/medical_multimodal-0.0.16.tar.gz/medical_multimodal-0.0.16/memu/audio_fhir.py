import os
import requests
import base64
import datetime
import pytz
import uuid
from openai import OpenAI
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import logging
import json  # Add json import to ensure correct JSON formatting

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioFHIR:
    BASE_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"  # Replace with actual backend API URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()
        self.openai_api_key = self.get_openai_api_key()
        self.client = OpenAI(api_key=self.openai_api_key)
        self.supported_languages = [
            "af", "ar", "hy", "az", "be", "bs", "bg", 
            "ca", "zh", "hr", "cs", "da", "nl", "en", "et", 
            "fi", "fr", "gl", "de", "el", "he", "hi", "hu", 
            "is", "id", "it", "ja", "kn", "kk", "ko", 
            "lv", "lt", "mk", "ms", "mr", "mi", "ne", 
            "no", "fa", "pl", "pt", "ro", "ru", "sr", 
            "sk", "sl", "es", "sw", "sv", "tl", "ta", "th", 
            "tr", "uk", "ur", "vi", "cy"
        ]

    def validate_api_key(self) -> str:
        """Validate MeMu API key by calling the backend."""
        response = self.make_request("GET", "/validate_api_key", params={"api_key": self.memu_api_key})
        return response.get("client_name")

    def get_openai_api_key(self):
        """Fetch the OpenAI API key from the backend."""
        try:
            response = self.make_request("GET", "/openai_api_key", params={"api_key": self.memu_api_key})
            if response and "openai_api_key" in response:
                return response["openai_api_key"]
            else:
                raise ValueError("OpenAI API key not found in the response.")
        except Exception as e:
            logger.error(f"Failed to get OpenAI API key: {e}")
            raise

    def make_request(self, method: str, endpoint: str, params=None, json=None) -> dict:
        """Generic method to handle API calls to the backend."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=json)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Error in API request to {endpoint}")

    def check_balance(self, minimum_required: float) -> bool:
        """Helper method to check if the client has enough balance."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        if current_balance < minimum_required:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required} is required to proceed. Current balance: ${current_balance}.")
        return True

    def deduct_client_balance(self, total_cost: float):
        """Deduct the total cost from the client's balance by calling the backend API."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")

        # Check if there is enough balance to cover the cost
        if current_balance < total_cost:
            logger.error(f"Insufficient balance to cover the cost. Current balance: ${current_balance}, total cost: ${total_cost}")
            raise ValueError(f"Insufficient balance to cover transcription cost. Total cost: ${total_cost}, current balance: ${current_balance}")

        # Proceed with deduction if balance is sufficient
        new_balance = current_balance - total_cost
        self.make_request("POST", "/balance/update", params={"api_key": self.memu_api_key}, json={"balance": new_balance})
        logger.info(f"Deducted ${total_cost} from {self.client_name}. New balance: ${new_balance}.")

    def reencode_audio(self, input_path: str, output_path: str, target_format: str = "wav") -> str:
        """Re-encodes the audio file to a specified format."""
        logger.info(f"Re-encoding audio file: {input_path} to {output_path}")
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format, parameters=["-ar", "16000", "-ac", "1"])
        return output_path

    def split_audio(self, audio_file_path: str, chunk_length_ms: int = 600000) -> list:
        """Splits an audio file into smaller chunks and returns file paths."""
        logger.info(f"Splitting audio file: {audio_file_path}")
        audio = AudioSegment.from_file(audio_file_path)
        chunk_file_paths = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_file_path = f"{audio_file_path}_{i // chunk_length_ms}.wav"
            chunk.export(chunk_file_path, format="wav")
            chunk_file_paths.append(chunk_file_path)
        return chunk_file_paths

    def transcribe_audio_chunk(self, audio_file_path: str, language: str = "en") -> dict:
        """Transcribes a single audio chunk using OpenAI Whisper with verbose response."""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    temperature=0,
                    response_format="verbose_json",
                    prompt= "You are the best medical transcriber in the world. Transcribe the following audio file. Ensure accuracy and correct any errors."
                )
            logger.info(f"Verbose transcription response: {transcription}")
            return transcription
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise e
        
    def translate_audio_chunk(self, audio_file_path: str) -> str:
        """Translates audio to English using Whisper."""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                translation = self.client.audio.translations.create(
                    model="whisper-1",
                    file=audio_file
                )
            return translation
        except Exception as e:
            raise e
        
    def translate_back_text(self, text: str, target_language: str) -> str:
        """Translates text from English back to the target language."""
        system_prompt = (
            "You are the best medical interpreter in the world. You excel at translating medical terminology, patient information, "
            "and other healthcare-related texts accurately and fluently. Ensure that all medical terms are translated correctly "
            "into the target language, maintaining the meaning and context of the original English text. "
            "Please pay attention to cultural sensitivities and ensure clarity for the medical team."
        )
        
        user_prompt = f"Please translate the following text from English to {target_language}:"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{user_prompt}\n\n{text}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise e
        
    def correct_transcription(self, transcription_text: str, language: str = "en") -> tuple:
        """Post-processes and corrects the transcription using OpenAI GPT."""
        system_prompt = (
            "You are a helpful assistant for the medical team. "
            "Correct any transcription errors, ensure medical terms are spelled correctly, "
            "and apply appropriate punctuation."
            f"Your corrections must be in the same language as the original {transcription_text}, in this case, {language}."
        )
        # Check if the client has enough balance before proceeding with correction
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        minimum_required_balance = 10.00
        logger.info(f"Balance before correction: ${current_balance}")

        if current_balance < minimum_required_balance:
            logger.warning(f"Insufficient balance for correction. Current balance: ${current_balance}")
            raise ValueError(f"Insufficient balance for transcription correction. A minimum balance of ${minimum_required_balance} is required to proceed.")

        # Proceed with correction if the balance is sufficient
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcription_text}
            ]
        )
        
        corrected_transcription = response.choices[0].message.content.strip()
        total_input_tokens = response.usage.prompt_tokens
        total_output_tokens = response.usage.completion_tokens
        logger.info(f"Total tokens used: {response.usage.total_tokens}")

        return corrected_transcription, total_input_tokens, total_output_tokens

    def create_fhir_document(self, corrected_transcription, patient_id):
        """Creates a FHIR DocumentReference with the corrected transcription."""
        # Base64 encode the corrected transcription
        corrected_transcription_base64 = base64.b64encode(corrected_transcription.encode('utf-8')).decode('utf-8')

        # Generate the narrative text (human-readable summary) with double quotes for XHTML compliance
        narrative_text = f'<div xmlns="http://www.w3.org/1999/xhtml"><p>{corrected_transcription}</p></div>'

        # Get current time with timezone info
        now = datetime.datetime.now(pytz.utc)
        timestamp = now.isoformat()

        # Fix timezone format if necessary
        if timestamp.endswith('+0000'):
            timestamp = timestamp[:-5] + '+00:00'

        # Generate a unique ID for the DocumentReference
        resource_id = str(uuid.uuid4())

        # Create FHIR DocumentReference resource
        fhir_document = {
            "resourceType": "DocumentReference",
            "id": resource_id,
            "text": {
                "status": "generated",
                "div": narrative_text  # Ensure double quotes in XHTML
            },
            "status": "current",
            "docStatus": "final",
            "type": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11488-4",
                        "display": "Consult note"
                    }
                ],
                "text": "Consult note"
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "date": timestamp,
            "content": [
                {
                    "attachment": {
                        "contentType": "text/plain",
                        "data": corrected_transcription_base64
                    }
                }
            ]
        }

        return fhir_document


    def transcribe_audio_file(self, file_path: str, patient_id: str, language: str = "en") -> str:
        """Handles the complete flow of re-encoding, splitting, translating/transcribing, correcting, generating FHIR, and billing."""

        # Step 1: Ensure the client has at least $10 balance before proceeding
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before transcription: ${current_balance}")

        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        # Step 2: Re-encode the audio file
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            reencoded_file_path = self.reencode_audio(file_path, f"{temp_audio_file.name}_reencoded.wav")

        # Step 3: Split the audio into chunks
        audio_chunks = self.split_audio(reencoded_file_path)

        full_transcription = ""
        total_duration = 0

        # Step 4: Check if the language is supported by Whisper for transcription
        if language not in self.supported_languages:
            # Language not supported, translate each chunk to English
            logger.info(f"Language {language} not supported. Translating audio chunks to English for transcription.")
            for chunk_file_path in audio_chunks:
                translation_data = self.translate_audio_chunk(chunk_file_path)
                full_transcription += translation_data.text + "\n"

                # Calculate the duration of the audio chunk using pydub
                audio_segment = AudioSegment.from_file(chunk_file_path)
                total_duration += len(audio_segment) / 60000  # Convert milliseconds to minutes

                os.remove(chunk_file_path)  # Clean up chunk files

            # Step 4a: Now translate the full transcription back to the original language
            logger.info(f"Translating transcription back to {language}.")
            full_transcription = self.translate_back_text(full_transcription, language)

            transcription_language = language  # After translation back to the target language
        else:
            # Transcribe each chunk in the original language
            logger.info(f"Language {language} is supported. Transcribing audio chunks.")
            for chunk_file_path in audio_chunks:
                transcription_data = self.transcribe_audio_chunk(chunk_file_path, language=language)
                full_transcription += transcription_data.text + "\n"
                total_duration += transcription_data.duration / 60  # Convert to minutes
                os.remove(chunk_file_path)  # Clean up chunk files

            transcription_language = language

        # Clean up the re-encoded file
        os.remove(reencoded_file_path)

        if full_transcription.strip():
            # Step 5: Deduct the transcription cost BEFORE checking balance for correction
            total_input_tokens = len(full_transcription.split())  # Estimate token count for input
            total_output_tokens = total_input_tokens  # Simplified token count

            # Step 6: Calculate cost using backend API
            total_cost = self.make_request("POST", "/calculate_cost", json={
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": total_duration
            }).get("total_cost")

            # Step 7: Deduct the cost from the client's balance
            self.deduct_client_balance(total_cost)
            logger.info(f"Deducted cost: ${total_cost}.")

            # Step 8: Ensure the client still has at least $10 before proceeding with correction
            current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
            logger.info(f"Balance before correction: ${current_balance}")

            if current_balance < minimum_required_balance:
                logger.warning(f"Insufficient balance for transcription correction. Current balance: ${current_balance}")
                raise ValueError(f"Insufficient balance for transcription correction. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

            # Step 9: Correct the transcription (or translation)
            corrected_transcription, total_input_tokens, total_output_tokens = self.correct_transcription(full_transcription, language=transcription_language)

            # Step 10: Generate FHIR document using the corrected transcription
            fhir_document = self.create_fhir_document(corrected_transcription, patient_id)

            # Step 11: Log the usage
            log_payload = {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": total_duration
            }
            logger.info(f"Logging transcription usage with payload: {log_payload}")

            # Make the request to log transcription usage
            try:
                self.make_request("POST", "/log_transcription_usage", params={"api_key": self.memu_api_key}, json=log_payload)
                logger.info("Successfully logged transcription usage.")
            except Exception as e:
                logger.error(f"Failed to log transcription usage: {e}")
                raise e

            # Return the FHIR document as a JSON string
            return json.dumps(fhir_document, indent=4)  # Ensure valid JSON format
        else:
            raise ValueError("Transcription failed: no text was transcribed.")
