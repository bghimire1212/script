import allure
from pprint import pprint
from testrail import *
import datetime

#Test rail status ID
#1: Passed
#2: Blocked
#3: Untested (not allowed when adding a new result)
#4: Retest
#5: Failed

client = APIClient('https://reachpower.testrail.io/')
client.user = 'xxx'
client.password = 'xxx'
project_id = 6
case = client.send_get(f'get_runs/{project_id}') #6 is a project id
pprint(case)
#import pdb; pdb.set_trace()
now = datetime.datetime.now().strftime("%d-%m-%Y %T")
data = {
    "suite_id": project_id,  #this is the project id
    "name": f"Test Run - {now}",
    "include_all": False,
    "case_ids": [125, 126, 127, 128] # these are test case ids
}
client.send_post(f"add_run/{project_id}", data=data)

case = client.send_get(f'get_runs/{project_id}') #6 is a project id
RUN_ID = case['runs'][0]['id']
class Test_Feature1():
    def setup_method(self):
        self.STATUS = 5
        print("Calling setup")

    def teardown_method(self):
        now = datetime.datetime.now().strftime("%d-%m-%Y %T")
        result = {"test_id": self.ID,
                  "status_id": self.STATUS,
                  "comment": f"Updated from pytest @{now}"}
        case = client.send_post(f'add_result_for_case/{RUN_ID}/{self.ID}', data=result)
        print("Calling teardown")


    def test_addition(self):
        """checking addition

        steps:
        1. define two numbers
        2. add them
        3. check the result
        """
        self.ID=125
        print("This is the addition function")
        a = 10
        b = 5
        assert a + b == 15, "Test failed"
        self.STATUS = 1

    def test_subtraction(self):
        """checking subtraction

        steps:
        1. define two numbers
        2. substract them
        3. check the result
        """
        self.ID=126
        print("This is the subtraction function")
        a = 10
        b = 5
        assert a - b == 5, "Test failed"
        self.STATUS = 1

    def test_multiplication(self):
        """checking multiplication

        steps:
        1. define two numbers
        2. multiply them
        3. check the result
        """
        self.ID=127
        print("This is the multiplication function")
        a = 10
        b = 5
        assert a * b == 50, "Test failed"
        self.STATUS = 1

    def test_division(self):
        """checking division

        steps:
        1. define two numbers
        2. divide them
        3. check the result
        """
        self.ID=128
        print("This is the division function")
        a = 10
        b = 5
        assert a / b == 2, "Test failed"
        self.STATUS = 1


