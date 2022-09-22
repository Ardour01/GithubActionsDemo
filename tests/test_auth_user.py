# python -m pytest -s --alluredir=test_results/ tests/test_auth_user.py

from src.base_test import BaseCase
from src.my_request import Request
from src.asserts import Asserts
import pytest


class TestListUsers(BaseCase):
    def test_list_all_users(self):
        """
        GET request
        :return:
        """
        params = {"page": 2}
        response = Request.get('api/users', params=params)
        Asserts.assert_code_status(response, 200)
        Asserts.assert_json_has_key(response, "data")
        Asserts.assert_response_not_has_cookie(response, 'auth_sid')
        Asserts.assert_response_not_has_headers(response, "x-csrf-token")

    @pytest.mark.parametrize("id", [2, 6, pytest.param(42, marks=pytest.mark.xfail)])
    def test_list_particular_user(self, id):
        """
        GET request with parameterization
        :return:
        """
        response = Request.get(f'api/users/{id}')
        Asserts.assert_code_status(response, 200)
        Asserts.assert_json_has_key(response, "data")
        Asserts.assert_response_not_has_cookie(response, 'auth_sid')
        Asserts.assert_response_not_has_headers(response, "x-csrf-token")

    def test_create_user(self):
        """
        POST request to create user
        :return:
        """
        data = {
                "name": "morpheus",
                "job": "leader"
        }
        response = Request.post('api/users', data)
        Asserts.assert_code_status(response, 201)
        Asserts.assert_time_is_less_than(response, 1)
        Asserts.assert_json_has_key(response, "name")
        Asserts.assert_json_value_by_key(response, "job", "leader")

    def test_register_user(self):
        """
        POST request to register user
        :return:
        """
        data = {
                "email": "eve.holt@reqres.in",
                "password": "pistol"
        }
        response = Request.post('api/register', data)
        Asserts.assert_code_status(response, 200)
        Asserts.assert_time_is_less_than(response, 1)
        Asserts.assert_json_has_key(response, "id")
        Asserts.assert_json_has_key(response, "token")

    #
    # def test_change_created_user_data(self):
    #     email = self.create_unique_email('vinkotov')
    #     password = '123'
    #     username = 'vinkotov'
    #
    #     data = {
    #         'email': email,
    #         'password': password,
    #         'username': username,
    #         'firstName': 'Vitalii',
    #         'lastName': 'Kotov',
    #     }
    #
    #     response = Request.post('user', data)
    #     user_id_after_registration = response.json()['id']
    #
    #     response = Request.post('user/login', {'password': password, 'email': email})
    #     user_id_after_auth = response.json()['user_id']
    #
    #     Asserts.assert_equals(user_id_after_registration, user_id_after_auth, "I've logged in as another user")
    #
    #     auth_cookie = self.get_cookie(response, 'auth_sid')
    #     auth_header = self.get_header(response, 'x-csrf-token')
    #
    #     response = Request.get(f'user/{user_id_after_auth}', headers=auth_header, cookies=auth_cookie)
    #     Asserts.assert_equals(username, response.json()['username'], "I've logged in as another user")
    #
    #     new_user_name = "Vitaliy"
    #     response = Request.put(
    #         f'user/{user_id_after_auth}',
    #         data={'username': new_user_name},
    #         headers=auth_header,
    #         cookies=auth_cookie
    #     )
    #     Asserts.assert_code_status(response, 200)
    #
    #     response = Request.get(f'user/{user_id_after_auth}', headers=auth_header, cookies=auth_cookie)
    #     Asserts.assert_equals(new_user_name, response.json()['username'], "Couldn't change name via put request")
