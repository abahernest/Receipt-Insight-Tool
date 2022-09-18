from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from receipt.models import *
import json


class CreateDelimiter (APITestCase):
    def setUp(self):
        self.input_data = {
            "value":"$",
            "count":4
            }
        self.input_data_without_count = {"value":"#"}

    ## POST REQUEST
    def test_should_return_200_status_code_on_post_method(self):
        """should be successful"""
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertEqual(res.status_code, 200)
        with self.subTest():
            self.assertEqual(Delimeter.objects.count(), 1)

    def test_should_convert_delimiter_value_to_json_string(self):
        """should convert delimiter value to json string"""
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.data["data"]["value"],
                            self.input_data["value"])
        self.assertEqual(res.data["data"]["value"],
                            json.dumps(self.input_data["value"]))

    def test_object_created_should_have_default_count_if_omitted(self):
        """object should be created with a default count of 1"""
        url = "/api/v1/delimeter"
        res = self.client.post(
            url, self.input_data_without_count, format="json")
        self.assertEqual(res.status_code, 200)
        
        ## Fetch created delimiter
        delimiter = Delimeter.objects.get(id=1)
        self.assertEqual(delimiter.count, 1)

    def test_should_not_create_object_if_value_already_exist(self):
        """should not allow duplicate delimiter values"""
        Delimeter.objects.create(
            value=self.input_data["value"],
            count= self.input_data["count"]
            )
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertNotEqual(res.status_code, 400)
        with self.subTest(res=res):
            self.assertNotEqual(res.data["message"], "Value already exist")

    ## GET REQUEST
    def test_should_return_all_delimiter_objects_on_get_request(self):
        """should have correct count of all delimiter objects"""
        url = "/api/v1/delimeter"
        NUMBER_OF_OBJECTS = 4
        delimiterArr=[]
        for count in range(NUMBER_OF_OBJECTS):
            delimiterArr.append( Delimeter (
                    value= self.input_data["value"] + str(count),
                    count= count+1
                ) )
        Delimeter.objects.bulk_create(delimiterArr)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['data']), NUMBER_OF_OBJECTS)


class FetchDelimiters (APITestCase):
    def setUp(self):
        self.input_data = {
            "value": "$",
            "count": 4
        }
        self.input_data_without_count = {"value": "#"}

    ## GET REQUEST
    def test_should_return_all_delimiter_objects_on_get_request(self):
        """should have correct count of all delimiter objects"""
        url = "/api/v1/delimeter"
        NUMBER_OF_OBJECTS = 4
        delimiterArr = []
        for count in range(NUMBER_OF_OBJECTS):
            delimiterArr.append(Delimeter(
                value=self.input_data["value"] + str(count),
                count=count+1
            ))
        Delimeter.objects.bulk_create(delimiterArr)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['data']), NUMBER_OF_OBJECTS)


class CreateDelimiter (APITestCase):
    def setUp(self):
        self.input_data = {
            "value": "$",
            "count": 4
        }
        self.input_data_without_count = {"value": "#"}

    ## POST REQUEST
    def test_should_return_200_status_code(self):
        """should be successful"""
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertEqual(res.status_code, 200)
        with self.subTest():
            self.assertEqual(Delimeter.objects.count(), 1)

    def test_should_convert_delimiter_value_to_json_string(self):
        """should convert delimiter value to json string"""
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.data["data"]["value"],
                            self.input_data["value"])
        self.assertEqual(res.data["data"]["value"],
                         json.dumps(self.input_data["value"]))

    def test_object_created_should_have_default_count_if_omitted(self):
        """object should be created with a default count of 1"""
        url = "/api/v1/delimeter"
        res = self.client.post(
            url, self.input_data_without_count, format="json")
        self.assertEqual(res.status_code, 200)

        ## Fetch created delimiter
        delimiter = Delimeter.objects.get(id=1)
        self.assertEqual(delimiter.count, 1)

    def test_should_not_create_object_if_value_already_exist(self):
        """should not allow duplicate delimiter values"""
        Delimeter.objects.create(
            value=self.input_data["value"],
            count=self.input_data["count"]
        )
        url = "/api/v1/delimeter"
        res = self.client.post(url, self.input_data, format="json")
        self.assertNotEqual(res.status_code, 400)
        with self.subTest(res=res):
            self.assertNotEqual(res.data["message"], "Value already exist")

    ## GET REQUEST
    def test_should_return_all_delimiter_objects_on_get_request(self):
        """should have correct count of all delimiter objects"""
        url = "/api/v1/delimeter"
        NUMBER_OF_OBJECTS = 4
        delimiterArr = []
        for count in range(NUMBER_OF_OBJECTS):
            delimiterArr.append(Delimeter(
                value=self.input_data["value"] + str(count),
                count=count+1
            ))
        Delimeter.objects.bulk_create(delimiterArr)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['data']), NUMBER_OF_OBJECTS)


class FetchReceipts (APITestCase):
    def setUp(self):
        self.input_data = {
            "value": "$",
            "count": 4
        }
        self.input_data_without_count = {"value": "#"}

    ## GET REQUEST
    def test_should_return_all_receipt_objects(self):
        """should have correct count of all receipt objects"""
        blocksArray = []
        NUMBER_OF_BLOCK_OBJECTS=2
        document = Document.objects.create(name="samplefile.txt")
        
        for count in range(NUMBER_OF_BLOCK_OBJECTS):
            blocksArray.append(Block(
                begin_row=count,
                begin_column=count+1,
                end_row=count,
                document=document,
                end_column=count+3
            ))
        Block.objects.bulk_create(blocksArray)

        url = "/api/v1/receipts"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['data']), 1)
        blocks = res.data["data"][0]["blocks"]
        self.assertEqual(len(blocks), NUMBER_OF_BLOCK_OBJECTS)

# class EstimatorDetailViewTestCase (APITestCase):
#     def setUp(self):
#         url = "/api/v1/on-covid-19/"
#         for count in range(1, 6):
#             self.client.post(url, {"name": f"Africa{count}",
#                                    "avgAge": 19.7,
#                                    "avgDailyIncomeInUSD": 5,
#                                    "avgDailyIncomePopulation": 0.71,
#                                    "periodType": "days",
#                                    "timeToElapse": 58,
#                                    "reportedCases": 674,
#                                    "population": 66622705,
#                                    "totalHospitalBeds": 1380614
#                                    }, format='json')

#     def test_should_return_object_at_given_id(self):
#         url = "/api/v1/on-covid-19/1/"
#         res = self.client.get(url)
#         self.assertEqual(res.data['input_data']['name'], "Africa1")
#         with self.subTest(res=res):
#             self.assertNotEqual(res.data['impact'], [])
#             self.assertNotEqual(res.data['severeImpact'], [])

#     def test_should_return_status_404_if_id_passed_to_get_method_is_invalid(self):
#         url = "/api/v1/on-covid-19/100/"
#         res = self.client.get(url)
#         self.assertEqual(res.status_code, 404)

#     def test_put_method(self):
#         url = "/api/v1/on-covid-19/1/"
#         res = self.client.get(url)
#         # old_impact,old_severeImpact = res.data['impact'],res.data['severeImpact']

#         new_data = {"name": "Changed_name",
#                     "avgAge": 19.7,
#                     "avgDailyIncomeInUSD": 5,
#                     "avgDailyIncomePopulation": 0.71,
#                     "periodType": "days",
#                     "timeToElapse": 58,
#                     "reportedCases": 674,
#                     "population": 66622705,
#                     "totalHospitalBeds": 1380614
#                     }
#         res = self.client.put(url, data=new_data)
#         new_data.update({'id': 1})
#         self.assertEqual(res.data, new_data)
#         # with self.subTest (res=res):
#         #     self.assertEqual (res.data['impact'],old_impact)
#         #     self.assertEqual (res.data['severeImpact'],old_severeImpact)

#     def test_should_return_404_if_input_to_put_method_is_invalid(self):
#         url = "/api/v1/on-covid-19/100/"
#         res = self.client.get(url)
#         # old_impact,old_severeImpact = res.data['impact'],res.data['severeImpact']

#         new_data = {"name": "Changed_name",
#                     "avgAge": 19.7,
#                     "avgDailyIncomeInUSD": 5,
#                     "avgDailyIncomePopulation": 0.71,
#                     "periodType": "days",
#                     "timeToElapse": 58,
#                     "reportedCases": 674,
#                     "population": 66622705,
#                     "totalHospitalBeds": 1380614
#                     }
#         res = self.client.put(url, data=new_data)
#         self.assertEqual(res.status_code, 404)

#     def test_should_check_that_id_of_input_isequal_to_that_of_impact_and_severeImpact(self):
#         url = "/api/v1/on-covid-19/1/"
#         res = self.client.get(url)

#         self.assertEqual(res.data['input_data']['id'], 1)
#         self.assertEqual(res.data['impact']['id'], 1)
#         self.assertEqual(res.data['severeImpact']['id'], 1)

#     def test_delete_method(self):
#         url = "/api/v1/on-covid-19/1/"
#         res = self.client.delete(url)

#         self.assertEqual(res.status_code, 204)
#         with self.subTest(url=url):
#             res = self.client.get(url)
#             self.assertEqual(res.status_code, 404)

#     def test_should_return_status_404_if_id_passed_to_delete_method_is_invalid(self):
#         url = "/api/v1/on-covid-19/100/"
#         res = self.client.delete(url)

#         self.assertEqual(res.status_code, 404)
