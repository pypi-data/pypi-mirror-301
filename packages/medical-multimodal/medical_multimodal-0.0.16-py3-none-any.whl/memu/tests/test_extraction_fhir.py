import json
import unittest
from memu.extraction_fhir import MedicalEntityExtractorFHIR

class TestMedicalEntityExtractionFHIR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"
        cls.entity_extractor = MedicalEntityExtractorFHIR(cls.memu_api_key)
        cls.transcript = """Good morning Jane, before we update your medication list, let's start by checking your weight and height. Your BMI is currently 28..."""
        cls.medical_records = [{
            "PatientID": "cea64247-e29a-40db-b052-b4af44dda1b2",
            "Name": "John Doe",
            "Age": 45,
            "Gender": "Male",
            "MedicalHistory": "Hypertension, Diabetes",
            "Medications": "Metformin, Furosemide, Potassium Chloride, Lisinopril",
            "TestResults": "Blood pressure: 130/85",
            "TreatmentPlans": "Continue current medication",
            "Notes": "Patient is stable",
        }]
        cls.patient_id = "test_patient_123"

    def test_extraction_to_fhir_bundle(self):
        """Test the extraction process and conversion to a FHIR bundle."""
        # Extract entities and ensure 'MedicalEntities' exists in the response
        extracted_entities, _ = self.entity_extractor.extract_medical_entities(
            self.transcript, self.medical_records, self.patient_id
        )

        # Check if the output is already a FHIR bundle
        if "resourceType" in extracted_entities and extracted_entities["resourceType"] == "Bundle":
            fhir_bundle = extracted_entities  # The output is already a FHIR bundle
            print("Output is already a FHIR Bundle.")
        else:
            # Process the extracted entities
            if "MedicalEntities" in extracted_entities:
                medical_entities = extracted_entities["MedicalEntities"]
            else:
                self.fail(f"Key 'MedicalEntities' not found in extraction response: {extracted_entities}")

            # Convert extracted entities into a FHIR-compliant bundle
            fhir_bundle = self.entity_extractor.create_fhir_bundle(medical_entities, self.patient_id)

        # Ensure the FHIR bundle contains entries
        self.assertGreater(len(fhir_bundle["entry"]), 0, "FHIR bundle should contain entries.")

        # Output the full FHIR bundle for validation purposes
        fhir_bundle_json = json.dumps(fhir_bundle, indent=4)
        print("FHIR Bundle JSON Output:")
        print(fhir_bundle_json)

        # Optionally, write the FHIR bundle to a file for further use or validation
        with open("fhir_bundle_output.json", "w") as f:
            f.write(fhir_bundle_json)

if __name__ == '__main__':
    unittest.main()
