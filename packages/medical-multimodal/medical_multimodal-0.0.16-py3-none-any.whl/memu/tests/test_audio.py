import unittest
import os
from memu.audio import Audio
from backend.app.database import get_client_balance, update_client_balance
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAudioTranscription(unittest.TestCase):
    def setUp(self):
        """Set up the Audio class before each test."""
        # Use the Development API key for testing
        self.dev_api_key = "dev_api_key_12345"

        if not self.dev_api_key:
            raise ValueError("API Key not found for DevelopmentClient")
        else:
            logger.info(f"Using Development API Key: {self.dev_api_key}")

        # Initialize the Audio class with the API key. The OpenAI API key will be fetched automatically.
        self.audio = Audio(self.dev_api_key)

        # Define a test file path (ensure this file exists in the test directory)
        self.test_file = "memu/tests/nurse_full.wav"
        if not os.path.exists(self.test_file):
            raise FileNotFoundError(f"Test audio file not found: {self.test_file}")

    def tearDown(self):
        """Cleanup method to reset client balance after each test to avoid cross-test contamination."""
        update_client_balance("DevelopmentClient", 1000.00)
        logger.info(f"Reset DevelopmentClient's balance to $1000 after test")

    def test_transcribe_audio_file(self):
        """Test the entire transcription flow (including correction) and ensure balance deduction."""
        update_client_balance("DevelopmentClient", 1000.00)  # Set balance to $1000 for testing
        
        start_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Starting balance: ${start_balance}")

        # Run the transcription
        transcription = self.audio.transcribe_audio_file(self.test_file, language="en")
        self.assertIsNotNone(transcription, "Transcription should not be None")  # Check that transcription was successful
        logger.info(f"Corrected Transcription: {transcription}")  # Log the transcription

        end_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Ending balance: ${end_balance}")

        # Ensure the balance has been deducted after transcription
        self.assertLess(end_balance, start_balance, "Balance should be deducted after transcription")

    def test_insufficient_balance_for_transcription(self):
        """Test that transcription fails if the client doesn't have at least $10 balance."""
        update_client_balance("DevelopmentClient", 9.99)
        logger.info(f"Set DevelopmentClient's balance to $9.99 for insufficient balance test")

        with self.assertRaises(ValueError, msg="Should raise ValueError for insufficient balance"):
            self.audio.transcribe_audio_file(self.test_file, language="en")
        logger.info("Insufficient balance test passed, ValueError raised as expected.")

    def test_sufficient_balance_for_transcription_but_insufficient_for_correction(self):
        """Test transcription succeeds but correction fails if balance goes below $10 after transcription."""
        
        # Set the client's balance to just above $10, which is sufficient for transcription but insufficient for correction
        update_client_balance("DevelopmentClient", 10.01)  # This should barely cover transcription, but not correction
        logger.info(f"Set DevelopmentClient's balance to $10.01 for insufficient balance during correction test")

        # Run the transcription, which should succeed as the balance is sufficient for the transcription part
        with self.assertRaises(ValueError, msg="Should raise ValueError for insufficient balance during correction"):
            # This method handles both transcription and correction, and it should fail during the correction phase
            transcription = self.audio.transcribe_audio_file(self.test_file, language="en")

        # After the error is raised, check the balance to confirm it dropped below the threshold during correction
        current_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Balance after failed correction: ${current_balance}")
        self.assertLess(current_balance, 10.00, "Balance should be below $10 after failed correction")

    def test_balance_sufficient_for_transcription_and_correction(self):
        """Test transcription and correction succeed with sufficient balance."""
        update_client_balance("DevelopmentClient", 100.00)

        start_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Starting balance: ${start_balance}")

        transcription = self.audio.transcribe_audio_file(self.test_file, language="en")
        self.assertIsNotNone(transcription, "Transcription should not be None")

        end_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Ending balance: ${end_balance}")

        self.assertLess(end_balance, start_balance, "Balance should be deducted after transcription")

    def test_no_negative_balance_after_transcription(self):
        """Ensure no balance deduction occurs if the client's balance is below $10."""
        update_client_balance("DevelopmentClient", 9.50)
        logger.info(f"Set DevelopmentClient's balance to $9.50")

        with self.assertRaises(ValueError, msg="Should raise ValueError for insufficient balance"):
            self.audio.transcribe_audio_file(self.test_file, language="en")

        balance_after = get_client_balance("DevelopmentClient")
        logger.info(f"Balance after failed transcription attempt: ${balance_after}")
        self.assertEqual(balance_after, 9.50, "Balance should remain the same after failed transcription due to insufficient funds")

    def test_exact_10_dollar_balance(self):
        """Test that transcription succeeds with exactly $10 balance, but correction fails."""
        
        # Set the client's balance to exactly $10
        update_client_balance("DevelopmentClient", 10.00)
        logger.info(f"Set DevelopmentClient's balance to exactly $10.00 for the test")

        # We expect transcription to succeed, but correction to fail due to insufficient balance afterward
        with self.assertRaises(ValueError, msg="Should raise ValueError for insufficient balance during correction"):
            transcription = self.audio.transcribe_audio_file(self.test_file, language="en")

        # After the error is raised, check that the balance dropped due to transcription cost
        current_balance = get_client_balance("DevelopmentClient")
        logger.info(f"Balance after failed correction: ${current_balance}")
        self.assertLess(current_balance, 10.00, "Balance should be below $10 after transcription and failed correction")

if __name__ == '__main__':
    unittest.main()
