import unittest
import logging
from memu.drug_interaction import DrugInteractionChecker

class TestDrugInteractionChecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.memu_api_key = "dev_api_key_12345"
        cls.checker = DrugInteractionChecker(cls.memu_api_key)

    def test_get_rxcui_by_string(self):
        """Test RXCUI retrieval with live API request."""
        drug_name = "Metformin"
        rxcui = self.checker.get_rxcui_by_string(drug_name)
        self.assertIsNotNone(rxcui)
        self.assertEqual(rxcui, "6809")  # Example RXCUI for Metformin

    def test_check_drug_interactions(self):
        """Test checking drug interactions between medications."""
        # Define a map of drugs and their RXCUIs
        rxcui_map = {
            "Metformin": "6809",
            "Lisinopril": "29046",
            "Furosemide": "4603",
            "Potassium Chloride": "8591"
        }

        # Test drug interaction check between medications
        drug_interactions = self.checker.check_drug_interactions(rxcui_map)

        # Print the results for manual validation
        print("Drug Interactions:", drug_interactions)

        # Assert that interactions were checked and returned correctly
        self.assertIsInstance(drug_interactions, list, "Expected a list of drug interactions.")
        self.assertGreater(len(drug_interactions), 0, "There should be at least one drug interaction checked.")

        # Ensure each interaction has the required fields
        for interaction in drug_interactions:
            self.assertIn("drug1", interaction, "Missing 'drug1' key in interaction.")
            self.assertIn("drug2", interaction, "Missing 'drug2' key in interaction.")
            self.assertIn("rxcui1", interaction, "Missing 'rxcui1' key in interaction.")
            self.assertIn("rxcui2", interaction, "Missing 'rxcui2' key in interaction.")
            self.assertIn("interactions", interaction, "Missing 'interactions' key in interaction.")

    def test_validate_and_correct_interactions(self):
        """Test validation and correction of drug interaction data."""
        drug_interactions = [
            {
                "drug1": "Metformin",
                "rxcui1": "6809",
                "drug2": "Lisinopril",
                "rxcui2": "29046",
                "interactions": []
            },
            {
                "drug1": "Metformin",
                "rxcui1": "6809",
                "drug2": "Furosemide",
                "rxcui2": "4603",
                "interactions": []
            }
        ]

        # Call the validate_and_correct_interactions function
        corrected_interactions = self.checker.validate_and_correct_interactions(drug_interactions)

        # Print the corrected interactions to observe the output
        print("Corrected Drug Interactions:", corrected_interactions)

        # Assert that the response contains the correct structure
        self.assertIn("interactions", corrected_interactions, "Missing 'interactions' key in corrected response.")
        self.assertIsInstance(corrected_interactions["interactions"], list, "Expected 'interactions' to be a list.")
        self.assertGreater(len(corrected_interactions["interactions"]), 0, "There should be at least one corrected interaction.")

        # Ensure the corrected interactions contain the correct fields
        for interaction in corrected_interactions["interactions"]:
            self.assertIn("drug1", interaction, "Missing 'drug1' key in corrected interaction.")
            self.assertIn("drug2", interaction, "Missing 'drug2' key in corrected interaction.")
            self.assertIn("rxcui1", interaction, "Missing 'rxcui1' key in corrected interaction.")
            self.assertIn("rxcui2", interaction, "Missing 'rxcui2' key in corrected interaction.")
            self.assertIn("interactions", interaction, "Missing 'interactions' key in corrected interaction.")
            self.assertIsInstance(interaction["interactions"], list, "Expected 'interactions' to be a list.")

    def test_orchestrate_interaction_check(self):
        """Test the orchestrator function that handles the full interaction check flow."""
        medication_list = ["Metformin", "Lisinopril", "Furosemide", "Potassium Chloride"]

        # Call the orchestrator function
        final_output = self.checker.orchestrate_interaction_check(medication_list)

        # Print the final output for manual validation
        print("Final Corrected Interactions:", final_output)

        # Assert the final output has the correct structure
        self.assertIn("interactions", final_output, "Missing 'interactions' key in final output.")
        self.assertIsInstance(final_output["interactions"], list, "Expected 'interactions' to be a list.")
        self.assertGreater(len(final_output["interactions"]), 0, "There should be at least one interaction in the final output.")

        # Ensure the final interactions contain the correct fields
        for interaction in final_output["interactions"]:
            self.assertIn("drug1", interaction, "Missing 'drug1' key in final interaction.")
            self.assertIn("drug2", interaction, "Missing 'drug2' key in final interaction.")
            self.assertIn("rxcui1", interaction, "Missing 'rxcui1' key in final interaction.")
            self.assertIn("rxcui2", interaction, "Missing 'rxcui2' key in final interaction.")
            self.assertIn("interactions", interaction, "Missing 'interactions' key in final interaction.")
            self.assertIsInstance(interaction["interactions"], list, "Expected 'interactions' to be a list.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
