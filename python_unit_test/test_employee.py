import unittest
from unittest.mock import patch
from employee import Employee


class TestEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')
        # This is a good place to create a database connection or open a file
        # that will be used by all the test methods. This method is called
        # before any test method is run.

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')
        # This is a good place to close a database connection or close a file
        # that was opened in setUpClass. This method is called after all test
        # methods have been run.

    def setUp(self):
        print('setUp')
        self.emp_1 = Employee('John', 'Doe', 50000)
        self.emp_2 = Employee('Jane', 'Doe', 60000)

    def tearDown(self):
        print('tearDown\n')

    def test_email(self):
        print('test_email')
        self.assertEqual(self.emp_1.email, 'john.doe@company.com')
        self.assertEqual(self.emp_2.email, 'jane.doe@company.com')

        self.emp_1.first = 'Jim'
        self.emp_2.first = 'Janette'

        self.assertEqual(self.emp_1.email, 'jim.doe@company.com')
        self.assertEqual(self.emp_2.email, 'janette.doe@company.com')

    def test_fullname(self):
        print('test_fullname')
        self.assertEqual(self.emp_1.fullname, 'John Doe')
        self.assertEqual(self.emp_2.fullname, 'Jane Doe')

        self.emp_1.first = 'Jim'
        self.emp_2.first = 'Janette'

        self.assertEqual(self.emp_1.fullname, 'Jim Doe')
        self.assertEqual(self.emp_2.fullname, 'Janette Doe')

    def test_apply_raise(self):
        print('test_apply_raise')
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 52500)
        self.assertEqual(self.emp_2.pay, 63000)

    def test_monthly_schedule(self):
        with patch('employee.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp_1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/Doe/May')
            self.assertEqual(schedule, 'Success')

            mocked_get.return_value.ok = False

            schedule = self.emp_2.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Doe/June')
            self.assertEqual(schedule, 'Bad Response!')


if __name__ == '__main__':
    unittest.main()