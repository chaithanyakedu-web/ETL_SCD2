import unittest

from ETL.ETL_Process import transform_data

class Test_etl_source_validations(unittest.TestCase):

    def test_etl_source_validations(self):
        print("ETL Source Validations Started")
        transform_data(r'K:\ETL_And_SCD2_project\SOURCE_DATA\json\day0_orgs.json')
        print("ETL Source Validations Finished")





