import json
import logging
from typing import Dict, List
import xmltodict
from benedict import benedict
from deepdiff import DeepDiff



@staticmethod
def compare_data(actual_data: Dict, expected_data: Dict, filtered_attributes: List, exclude_data: List
                     ) -> bool:
        actual_data_dict = benedict(actual_data)
        expected_data_dict = benedict(expected_data)
        error_list = []
        # Check if only specific attributes to be validated
        if filtered_attributes is not None:
            logging.info("Compare only the filtered attributes")
            # Compare only the filtered list of attributes
            for node_path in filtered_attributes:
                actual_data_node = actual_data_dict.subset(node_path)
                if actual_data_node is not None:
                    expected_data_node = expected_data_dict.subset(node_path)
                    if expected_data_node is not None:
                        result = DeepDiff(expected_data_node, actual_data_node, ignore_order=True)
                        if result:
                            error_list.append(result)
                    else:
                        error_list.append(f"{node_path} missing in expected data")
                else:
                    error_list.append(f"{node_path} missing in current data")

        elif exclude_data is not None:
            logging.info("Exclude Attributes and then compare")
            modified_actual_data = actual_data_dict
            modified_expected_data = expected_data_dict
            for node_path in exclude_data:
                # Remove from the data
                modified_actual_data.remove(node_path)
                modified_expected_data.remove(node_path)
            # Compare
            result = DeepDiff(modified_expected_data, modified_actual_data, ignore_order=True)
            logging.info(f"Exclude attributes and validate - Result = {result}")
            if result:
                error_list.append(result)
        else:
            logging.info("Compare all attributes")
            # Compare all attributes
            result = DeepDiff(expected_data_dict, actual_data_dict, ignore_order=True)
            logging.info(f"Exclude attributes and validate - Result = {result}")
            if result:
                error_list.append(result)
        if error_list:
            logging.error(f"ERROR: Output data is not as expected *****: {error_list}")
            return False
        else:
            return True
@staticmethod
def Validate_xml_or_json_file(Expected_file,Actual_file,Filtered_attributes, exclude_data):
        File_extention=""
        if Expected_file.lower().endswith('xml'):
            if  Actual_file.lower().endswith('xml'):
                File_extention="xml"
        elif Expected_file.lower().endswith('json'):
            if  Actual_file.lower().endswith('json'):
                File_extention="json"
        print("Both file extention is" +" "+ File_extention)
        if File_extention.lower().endswith('xml'):
            print("Input xml file")
            actual_file = open(Actual_file, "r")
            actual_data = actual_file.read()
            xml_dict = xmltodict.parse(actual_data)
            actualxml_to_json = json.dumps(xml_dict)
            #Expected data
            Expected_filedata = open(Expected_file)
            expected_data = Expected_filedata.read()
            xml_dict = xmltodict.parse(expected_data)
            expect_xml_to_json = json.dumps(xml_dict)
            flag = compare_data(actualxml_to_json, expect_xml_to_json, Filtered_attributes, exclude_data)
            print(f"Valid data file comparison - Valid = ", {flag})

        elif File_extention.lower().endswith('json'):
            print("Input json file")
            actual_file = open(Actual_file, "r")
            actual_data = actual_file.read()
            Expected_filedata = open(Expected_file)
            expected_data = Expected_filedata.read()
            flag = compare_data(actual_data, expected_data, Filtered_attributes, exclude_data)
            print(f"Valid data file comparison - Valid = ", {flag})
        else:
            logging.error("Invalid file format upload only XML or json files")




