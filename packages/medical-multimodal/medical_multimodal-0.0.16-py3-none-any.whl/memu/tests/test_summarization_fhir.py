import json
import unittest
from memu.summarization_fhir import MedicalSummarizer

class TestMedicalSummarizerFHIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"
        cls.summarizer = MedicalSummarizer(cls.memu_api_key)
        cls.patient_id = "example_patient_123"

        # Sample transcript and medical records for summarization
        cls.transcript = """Good morning Jane, before we update your medication list, let's start by checking your weight and height. 
                            Your BMI is currently 28, which classifies as overweight. We'll discuss potential lifestyle adjustments with the doctor later.
                            Now please sit down so I can measure your blood pressure and pulse. Blood pressure is 145 over 90, pulse is 88 bpm. 
                            Your blood pressure is a bit high today, have you been monitoring it at home? I have, and it's been up and down."""
        cls.medical_records = [
            {
                "PatientID": "cea64247-e29a-40db-b052-b4af44dda1b2",
                "Name": "Jane Doe",
                "Age": 45,
                "Gender": "Female",
                "MedicalHistory": "Hypertension, Diabetes",
                "Medications": "Metformin, Lisinopril, Furosemide, Potassium Chloride",
                "TestResults": "Blood pressure: 130/85",
                "TreatmentPlans": "Continue current medication",
                "Notes": "Patient is stable",
                "MedicationsRXCUIs": {
                    "Metformin": "6809",
                    "Lisinopril": "29046",
                    "Furosemide": "4603",
                    "Potassium Chloride": "8591"
                }
            }
        ]

    def test_fhir_summarization_to_composition(self):
        """Test the medical summarization process and conversion to a FHIR Composition resource."""

        # Perform the medical summarization
        summary_data = self.summarizer.summarize_medical_info(self.transcript, self.medical_records)

        # Convert the summary data into a FHIR Composition resource
        fhir_composition = self.summarizer.create_fhir_composition(summary_data, self.patient_id)

        # Check if the output is already a FHIR Composition
        if "resourceType" in fhir_composition and fhir_composition["resourceType"] == "Composition":
            print("Output is already a FHIR Composition.")
        else:
            self.fail(f"Expected FHIR Composition, but got: {fhir_composition}")

        # Ensure the FHIR Composition contains sections
        self.assertGreater(len(fhir_composition["section"]), 0, "FHIR Composition should contain sections.")

        # Output the full FHIR Composition for validation purposes
        fhir_composition_json = json.dumps(fhir_composition, indent=4)
        print("FHIR Composition JSON Output:")
        print(fhir_composition_json)

        # Optionally, write the FHIR Composition to a file for further use or validation
        with open("fhir_medical_summary_composition_output.json", "w") as f:
            f.write(fhir_composition_json)

if __name__ == '__main__':
    unittest.main()
