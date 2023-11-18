import unittest
import data_ingestion
import utils
import pandas as pd
import os 
from unittest.mock import patch

class TestDataIngestion(unittest.TestCase):
    """ Test Data Ingestion"""
    def setUp(self):
        # Create output directory
        os.makedirs('./data', exist_ok=True)

    @patch('utils.perform_get_request') 
    def test_get_load_data_from_entsoe(self, mock_request):
        mock_request.return_value = '<xml></xml>'
        
        regions = {'UK': '10Y1001A1001A92E'}
        data_ingestion.get_load_data_from_entsoe(regions, '202301010000', '202301020000', './data')
        
        self.assertTrue(mock_request.called)
        self.assertEqual(mock_request.call_args[0][0], 'https://web-api.tp.entsoe.eu/api')
        
    def test_parse_arguments(self):
        args = data_ingestion.parse_arguments()
        self.assertEqual(args.start_time.strftime('%Y-%m-%d'), '2023-01-01')
        self.assertEqual(args.end_time.strftime('%Y-%m-%d'), '2023-01-02')
        self.assertEqual(args.output_path, './data')
        
class TestUtils(unittest.TestCase):

    def test_xml_to_load_dataframe(self):
        xml_data = '<xml></xml>'
        df = utils.xml_to_load_dataframe(xml_data)
        self.assertIsInstance(df, pd.DataFrame)
        
    def test_make_url(self):
        base_url = 'https://example.com'
        params = {'param1': 'value1'}
        url = utils.make_url(base_url, params)
        self.assertEqual(url, 'https://example.com?param1=value1')
        
if __name__ == '__main__':
    unittest.main()