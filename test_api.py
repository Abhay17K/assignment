import requests
import unittest


class LoginAPITestCase(unittest.TestCase):
    def setUp(self):

        self.base_url = 'http://localhost:5000'  # API URL
        self.login_url = self.base_url + '/login'  # login API endpoint
        self.headers = {'Content-Type': 'application/json'}
        
        # Create a test user in the database
        self.username = 'abhay_khanna'
        self.password = 'welcome123'

    def test_login_success(self):
        # Test a successful login scenario

        # Create the request payload with the username and password
        payload = {
            'username': self.username,
            'password': self.password
        }

        # Make a POST request to the login API endpoint
        response = requests.post(self.login_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        # Test a scenario where invalid credentials are provided

        # Create the request payload with incorrect username and password
        payload_data = {
            'username': 'invaliduser',
            'password': 'invalidpassword'
        }

        # Make a POST request to the login API endpoint
        response = requests.post(self.login_url, json=payload_data, headers=self.headers)
        print("response code :",response)
        # Assert the response status code
        self.assertEqual(response.status_code, 401)

class AdminAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        self.base_url = 'http://localhost:5000'
        self.create_user_url = self.base_url + '/admin/users'
        self.edit_user_url = self.base_url + '/admin/users/<user_id>'
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer <admin_token>'}
        
    
    def test_create_user_success(self):
        # Test a successful user creation scenario

        # Create the request payload with user details
        payload = {
            'username': 'abhay_khanna',
            'password': 'welcome123',
            'role': 'normal'  # or 'admin' based on your implementation
        }

        # Make a POST request to the create user API endpoint
        response = requests.post(self.create_user_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_edit_user_success(self):
        # Test a successful user edit scenario

        # Create the request payload with updated user details
        payload = {
            'username': 'abhay_khanna',
            'password': 'welcome1234',
            'role': 'admin'
        }

        # Replace <user_id> in the URL with the ID of the user you want to edit
        edit_user_url = self.edit_user_url.replace('<user_id>', '2')

        # Make a PUT request to the edit user API endpoint
        response = requests.put(edit_user_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)


class GroupAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        self.base_url = 'http://localhost:5000'
        self.create_group_url = self.base_url + '/groups'
        self.delete_group_url = self.base_url + '/groups/<group_id>'
        self.search_group_url = self.base_url + '/groups/search'
        self.add_members_url = self.base_url + '/groups/<group_id>/members'
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer <user_token>'}
        
    def test_create_group_success(self):
        # Test a successful group creation scenario

        # Create the request payload with group details
        payload = {
            'group_name': 'HR Payroll Group',
            'admin_id': 1  # Replace with appropriate usernames
        }

        # Make a POST request to the create group API endpoint
        response = requests.post(self.create_group_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_delete_group_success(self):
        # Test a successful group deletion scenario

        delete_group_url = self.delete_group_url.replace('<group_id>', '2')

        # Make a DELETE request to the delete group API endpoint
        response = requests.delete(delete_group_url, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_search_group_success(self):
        # Test a successful group search scenario

        # Create the request payload with search parameters
        payload = {
            'keyword': 'ADMIN GROUP G1'
        }

        # Make a POST request to the search group API endpoint
        response = requests.get(self.search_group_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_add_members_success(self):
        # Test a successful addition of members to a group

        add_members_url = self.add_members_url.replace('<group_id>', '1')

        # Create the request payload with members to add
        payload = {
            'user_id': 2,
            'group_id': 2
        }

        # Make a POST request to the add members API endpoint
        response = requests.post(add_members_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

class GroupMessagesAPITestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'
        self.send_message_url = self.base_url + '/groups/<group_id>/messages'
        self.like_message_url = self.base_url + '/groups/<group_id>/messages/<message_id>/likes'
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer <user_token>'}

    
    def test_send_message_success(self):
        # Test a successful message sending scenario

        send_message_url = self.send_message_url.replace('<group_id>', "1")

        # Create the request payload with message details
        payload = {
            'user_id': 1,
            'content': 'Hello group members!'
        }

        # Make a POST request to the send message API endpoint
        response = requests.post(send_message_url, json=payload, headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    def test_like_message_success(self):
        # Test a successful message liking scenario

        like_message_url = self.like_message_url.replace('<group_id>', '1').replace('<message_id>', '1')

        payload = {
            'user_id': 2
        }

        # Make a POST request to the like message API endpoint
        response = requests.post(like_message_url, json=payload,  headers=self.headers)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()