import unittest
import os
import pandas as pd
import numpy as np
from PyFIRSTClassifier import FIRSTClassifier

classifier = FIRSTClassifier.Classifiers()
class TestFIRSTClassifier(unittest.TestCase):

    def test_exist_single_source_classification(self):
        """
        Test classification for a single radio source based on its coordinates.
        """
        # Example coordinates (Right Ascension and Declination)
        ra = 223.47337	
        dec = 26.80928
        
        # Call the classification function
        fits_file_link, predicted_class, probability, image = classifier.single_source(ra, dec, plot= False)
        
        # Assert that the result is not None or empty
        self.assertIsNotNone(predicted_class)
        self.assertTrue(len(probability) > 0)
        self.assertIsNotNone(image)
        self.assertIsNotNone(fits_file_link)

    def test_non_exist_single_source_classification(self):
        """
        Test classification for a single radio source based on its coordinates.
        """
        # Example coordinates (Right Ascension and Declination)
        ra = 565747847.2541085
        dec = 7586748.2541085
        
        # Call the classification function
        fits_file_link, predicted_class, probability, image = classifier.single_source(ra, dec, plot=False)
        
        # Assert that the result is not None or empty
        self.assertTrue(np.isnan(predicted_class))
        self.assertTrue(np.isnan(probability))
        self.assertTrue(np.isnan(image))
        self.assertTrue(np.isnan(fits_file_link))

    def test_multi_source_classification(self):
        """
        Test classification for multiple radio sources using a CSV file.
        """
        output_file = "results.csv"
        input_file = "test.csv"
        classifier.multi_sources(file=input_file, ra_col=0, dec_col=1, output_file=output_file )
        
        
        # Read the output file and check for expected columns and data
        output_df = pd.read_csv(output_file)
        input_df = pd.read_csv(input_file)
        output_df = pd.read_csv(output_file)
        self.assertIn("RA", output_df.columns)
        self.assertIn("DEC", output_df.columns)
        self.assertIn("CLASS", output_df.columns)
        self.assertIn("PROB", output_df.columns)
        self.assertIn("URL", output_df.columns)
        self.assertEqual(output_df.shape[0], input_df.shape[0]) # Ensure there's 15 results

        # Clean up test files
        os.remove(output_file)
    

if __name__ == '__main__':

    unittest.main()
