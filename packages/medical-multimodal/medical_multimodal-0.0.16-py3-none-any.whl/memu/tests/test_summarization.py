import unittest
import json
from memu.summarization import MedicalSummarizer

class TestMedicalSummarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"
        cls.summarizer = MedicalSummarizer(cls.memu_api_key)

        cls.transcript = """Good morning Jane, before we update your medication list, let's start by checking your weight and height. 
        Your BMI is currently 28, which classifies as overweight. We'll discuss potential lifestyle adjustments with the doctor later. 
        Now please sit down so I can measure your blood pressure and pulse. Blood pressure is 145 over 90, pulse is 88 bpm. 
        Your blood pressure is a bit high today, have you been monitoring it at home? I have, and it's been up and down. 
        Let's also check your oxygenation level and temperature. Oxygen saturation is 94%, your temperature is normal. 
        I'll note all this for the doctor, how have you been feeling overall? Overall good, but have been having hot flashes and mood swings."""

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
                },
                "MedicalCodes": {},
                "FullSummary": ""
            }
        ]

    def test_summarization(self):
        """Test the summarization process and output validity."""
        # Call the summarizer to generate a medical summary
        summary = self.summarizer.summarize_medical_info(self.transcript, self.medical_records)

        # Ensure the output contains the necessary keys
        self.assertIn("PatientSummary", summary, "Summary should contain 'PatientSummary' key.")
        patient_summary = summary["PatientSummary"]

        self.assertIn("MedicalStatus", patient_summary, "Patient summary should contain 'MedicalStatus'.")
        self.assertIn("Medications", patient_summary, "Patient summary should contain 'Medications'.")
        self.assertIn("TreatmentPlan", patient_summary, "Patient summary should contain 'TreatmentPlan'.")
        self.assertIn("Summary", patient_summary, "Patient summary should contain 'Summary'.")
        self.assertIn("Recommendations", patient_summary, "Patient summary should contain 'Recommendations'.")

        # Check if the medications and recommendations are valid
        self.assertIsInstance(patient_summary["Medications"], list, "Medications should be a list.")
        self.assertIsInstance(patient_summary["Recommendations"], str, "Recommendations should be a string.")

        # Output the summary for manual review (optional)
        summary_json = json.dumps(summary, indent=4)
        print("Generated Summary JSON:")
        print(summary_json)

        # Optionally, write the summary to a file for validation
        with open("generated_summary_output.json", "w") as f:
            f.write(summary_json)

if __name__ == '__main__':
    unittest.main()
