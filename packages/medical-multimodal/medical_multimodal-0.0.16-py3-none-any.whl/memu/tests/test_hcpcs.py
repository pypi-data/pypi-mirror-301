import unittest
from memu.hcpcs import HCPCSCodeOrchestrator

class TestHCPCSCodeOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"  # Replace with your actual development API key
        cls.orchestrator = HCPCSCodeOrchestrator(cls.memu_api_key)

        # Sample input data for testing
        cls.procedure = "air pressure mattress"  # Example procedure
        cls.consultation_summary = (
            "The patient requires an air pressure mattress for improved comfort due to pressure sores."
        )
        cls.patient_summary = {
            "MedicalStatus": {
                "ChronicConditions": ["Pressure Sores"],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "75 bpm",
                    "OxygenSaturation": "96%",
                    "Temperature": "Normal"
                }
            },
            "Medications": ["Metformin", "Lisinopril"],
            "TreatmentPlan": ["Prescribe air pressure mattress"],
            "Summary": (
                "Jane Doe, a 70-year-old female, presents with pressure sores. "
                "The patient requires an air pressure mattress for improved comfort."
            ),
            "Recommendations": "Use the air pressure mattress as recommended."
        }

    def test_suggest_hcpcs_code(self):
        """Test the HCPCS code suggestion process and print the output."""
        result = self.orchestrator.suggest_hcpcs_code(
            self.procedure,
            self.consultation_summary,
            self.patient_summary
        )

        # Print the result for manual observation
        print("HCPCS Code Suggestion Output:")
        print(result)

        # Basic assertions to ensure the output structure is correct
        self.assertIn("fetched_codes", result, "Output should contain 'fetched_codes'.")
        self.assertIn("suggested_code", result, "Output should contain 'suggested_code'.")

if __name__ == '__main__':
    unittest.main()
