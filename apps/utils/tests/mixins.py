import json

# import rstr
from cerberus import Validator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

# from main_app.redis import REDIS_SERVER_DB_1

User = get_user_model()


# class AuthMixin:
#     TEST_USER_PASSWORD = '123456789'
#
#     def generate_user(
#             self,
#             username=None,
#             email=None,
#             make_user_password=True,
#             **kwargs
#     ):
#         if not email:
#             email = '{0}@{1}.{2}'.format(
#                 rstr.nonwhitespace(exclude='@'),
#                 rstr.domainsafe(),
#                 rstr.letters(3)
#             )
#         if not username:
#             username = 'user_' + email
#
#         user = User(
#             username=username,
#             email=email,
#             level_id=1,
#             **kwargs
#         )
#         if make_user_password:
#             user.password = make_password(self.TEST_USER_PASSWORD)
#
#         user.save()
#         return user
#
#     @staticmethod
#     def get_token(user):
#         user.generate_tokens()
#         return {
#             "refresh_token": user.refresh_token,
#             "access_token": user.access_token
#         }
#
#     def get_authenticated_client(self, user):
#         token = self.get_token(user)['access_token']
#         client = APIClient()
#         client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#         return client


class BaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def check_response_schema(self, schema, response):
        validator = Validator(schema)
        is_valid = validator.validate(response)
        if not is_valid:
            print(f'Validator Error:{validator.errors}')
        self.assert_(validator.validate(response))

    def tearDown(self) -> None:
        super(BaseAPITestCase, self).tearDown()
        # REDIS_SERVER_DB_1.flushdb()

#
# class TestListMixin(AuthMixin):
#     """
#         usage example:
#             self.list_params = {
#                 'allow_any': False,
#                 'legal_users': [self.staff1, ],
#                 'url': '/api/v1/plan/step/',
#                 'forbidden_users':[self.client1,],
#                 'validator': step_list
#             }
#         warning: if allow_any:True the API is public and you don't need to set legal_users
#     """
#
#     def test_list(self):
#
#         self.assertTrue(hasattr(self, 'list_params'), 'list_params must be defined')
#
#         self.assertTrue(isinstance(self.list_params, dict), 'list_params must be a dictionary.')
#
#         self.assertIsNotNone(self.list_params.get('url'), 'list_params: url must be defined')
#
#         self.assertIsNotNone(self.list_params.get('validator'), 'list_params: validator must be defined')
#
#         self.__run_list_test()
#
#     def __run_list_test(self):
#         if self.list_params.get('allow_any'):
#             response = self.client.get(self.list_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.check_response_schema(self.list_params['validator'], json.loads(response.content))
#
#         else:
#             self.__check_list_401()
#
#             if self.list_params.get('forbidden_users'):
#                 self.__check_list_403()
#
#             self.__check_list_200()
#
#     def __check_list_401(self):
#         response = self.client.get(self.list_params['url'])
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def __check_list_403(self):
#         for forbidden_user in self.list_params['forbidden_users']:
#             authenticated_forbidden_client = self.get_authenticated_client(forbidden_user)
#             response = authenticated_forbidden_client.get(self.list_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def __check_list_200(self):
#         self.assertGreater(len(self.list_params['legal_users']), 0, 'list_params:legal_users list must not be empty!')
#
#         for legal_user in self.list_params['legal_users']:
#             authenticated_legal_client = self.get_authenticated_client(legal_user)
#             response = authenticated_legal_client.get(self.list_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.check_response_schema(self.list_params['validator'], json.loads(response.content))
#
#             self.assertGreater(len(json.loads(response.content)['results']), 0)
#
#
# class TestRetrieveMixin(AuthMixin):
#     """
#         usage example:
#         self.retrieve_params = {
#               'url': f'/api/v1/article/{id}/',
#               'legal_users': [self.staff1, ],
#               'forbidden_users':[self.user_1,],
#               'not_found_users':[self.user_2,],
#               'validator':article_validator
#           }
#
#            Note : not-found-users --> check 404 error
#    """
#
#     def test_retrieve(self):
#         self.assertTrue(hasattr(self, 'retrieve_params'), 'retrieve_params must be defined')
#
#         self.assertTrue(isinstance(self.retrieve_params, dict), 'retrieve_params must be a dictionary.')
#
#         self.assertIsNotNone(self.retrieve_params.get('url'), 'retrieve_params: url must be defined')
#
#         self.assertIsNotNone(self.retrieve_params.get('validator'), 'retrieve_params: validator must be defined')
#
#         self.__run_retrieve_test()
#
#     def __run_retrieve_test(self):
#
#         if self.retrieve_params.get('allow_any'):
#             response = self.client.get(self.retrieve_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.check_response_schema(self.retrieve_params['validator'], json.loads(response.content))
#         else:
#             self.__check_retrieve_401()
#
#             if self.retrieve_params.get('forbidden_users'):
#                 self.__check_retrieve_403()
#
#             if self.retrieve_params.get('not_found_users'):
#                 self.__check_retrieve_404()
#
#             self.__check_retrieve_200()
#
#     def __check_retrieve_401(self):
#         response = self.client.get(self.retrieve_params['url'])
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def __check_retrieve_403(self):
#         for forbidden_user in self.retrieve_params.get('forbidden_users'):
#             authenticated_forbidden_client = self.get_authenticated_client(forbidden_user)
#             response = authenticated_forbidden_client.get(self.retrieve_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def __check_retrieve_404(self):
#         for not_found_user in self.retrieve_params.get('not_found_users'):
#             authenticated_not_found_client = self.get_authenticated_client(not_found_user)
#             response = authenticated_not_found_client.get(self.retrieve_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def __check_retrieve_200(self):
#         self.assertGreater(len(self.retrieve_params['legal_users']), 0,
#                            'retrieve_params:legal_users list must not be empty!')
#
#         for legal_user in self.retrieve_params.get('legal_users'):
#             authenticated_legal_user = self.get_authenticated_client(legal_user)
#             response = authenticated_legal_user.get(self.retrieve_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.check_response_schema(self.retrieve_params['validator'], json.loads(response.content))
#
#
# class TestDestroyMixin(AuthMixin):
#     """
#       usage example:
#       self.staff1 = TestDestroyMixin.generate_user(is_staff=True)
#       self.staff2 = TestDestroyMixin.generate_user(is_staff=True)
#       self.client1 = TestDestroyMixin.generate_user()
#       self.base_object = Article.objects.create(title="title1",author=self.staff1)
#
#       self.destroy_params = {
#             'object': self.base_object,
#             'model': Article,
#             'url': f'/api/v1/article/{self.base_object.id}/',
#             'legal_users': [self.staff1, ]
#             'not_found_users': [self.staff2 ]
#             'forbidden_users':[self.client1,]
#         }
#
#       Note : not-found-users --> check 404 error
#    """
#
#     def test_destroy(self):
#         self.assertTrue(hasattr(self, 'destroy_params'), 'destroy_params must be defined')
#
#         self.assertTrue(isinstance(self.destroy_params, dict), 'destroy_params must be a dictionary.')
#
#         self.assertIsNotNone(self.destroy_params.get('url'), 'destroy_params: url must be defined')
#
#         self.assertIsNotNone(self.destroy_params.get('model'), 'destroy_params: model class must be defined')
#
#         self.assertIsNotNone(self.destroy_params.get('object'), 'destroy_params: object must be defined')
#
#         self.__run_destroy_test()
#
#     def __run_destroy_test(self):
#         self.__check_destroy_401()
#
#         if self.destroy_params.get('forbidden_users'):
#             self.__check_destroy_403()
#
#         if self.destroy_params.get('not_found_users'):
#             self.__check_destroy_404()
#
#         self.__check_destroy_200()
#
#     def __check_destroy_401(self):
#         response = self.client.delete(self.destroy_params['url'])
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def __check_destroy_403(self):
#         for forbidden_user in self.destroy_params['forbidden_users']:
#             authenticated_forbidden_client = self.get_authenticated_client(forbidden_user)
#             response = authenticated_forbidden_client.delete(self.destroy_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def __check_destroy_404(self):
#         for not_found_user in self.destroy_params['not_found_users']:
#             authenticated_not_found_client = self.get_authenticated_client(not_found_user)
#             response = authenticated_not_found_client.delete(self.destroy_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def __check_destroy_200(self):
#         self.assertGreater(len(self.destroy_params['legal_users']), 0,
#                            'destroy_params:legal_users list must not be empty!')
#
#         for legal_user in self.destroy_params['legal_users']:
#             authenticated_legal_client = self.get_authenticated_client(legal_user)
#             response = authenticated_legal_client.delete(self.destroy_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#             self.assertEqual(self.destroy_params['model'].objects.filter(id=self.destroy_params['object'].id).exists(),
#                              False)
#
#
# class TestCreateMixin(AuthMixin):
#     """
#       usage example:
#           self.create_params = {
#                 'allow_any':False,
#                 'model': Article,
#                 'url': f'/api/v1/article/',
#                 'legal_users': [self.user, ]
#                 'forbidden_users':[self.user,]
#                 'valid_data':{
#                     required_params:{'author':self.admin.id},
#                     optional_params:{'title':'title1'},
#                 }
#                 'invalids_data':[{some key and values},]
#                 'validator':article_validator
#             }
#
#        warning: if allow_any:True the API is public and you don't need to set legal_users and forbidden_users
#     """
#
#     def test_create(self):
#         self.assertTrue(hasattr(self, 'create_params'), 'create_params must be defined')
#
#         self.assertTrue(isinstance(self.create_params, dict), 'create_params must be a dictionary.')
#
#         self.assertIsNotNone(self.create_params.get('url'), 'create_params: url must be defined')
#
#         self.assertIsNotNone(self.create_params.get('model'), 'create_params: model class must be defined')
#
#         self.assertIsNotNone(self.create_params.get('valid_data'),
#                              'create_params: valid_data dictionary must be defined')
#
#         self.assertIsNotNone(self.create_params['valid_data'].get('required_params'),
#                              'create_params: required_params dictionary in valid_data must be defined')
#
#         self.assertIsNotNone(self.create_params.get('validator'),
#                              'create_params: validator must be defined')
#
#         self.__run_create_test()
#
#     def __run_create_test(self):
#         if self.create_params.get('allow_any'):
#             clients = [self.client, ]
#             self.__check_create_400(clients)
#
#             self.__check_create_201(clients)
#
#         else:
#             self.__check_create_401()
#
#             if self.create_params.get('forbidden_users'):
#                 self.__check_create_403()
#
#             self.assertGreater(len(self.create_params['legal_users']), 0,
#                                'create_params:legal_users list must not be empty!')
#
#             legal_clients = [self.get_authenticated_client(user) for user in self.create_params['legal_users']]
#
#             self.__check_create_400(legal_clients)
#
#             self.__check_create_201(legal_clients)
#
#     def __check_create_201(self, clients):
#         for client in clients:
#             before_count = self.create_params['model'].objects.count()
#             response = client.post(self.create_params['url'], data=self.create_params['valid_data']['required_params'])
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=json.loads(response.content))
#
#             self.check_response_schema(self.create_params['validator'], json.loads(response.content))
#
#             if self.create_params['valid_data'].get('optional_params'):
#                 # clear table for prevent error with unique fields
#                 self.create_params['model'].objects.last().delete()
#
#                 all_params = {**self.create_params['valid_data']['required_params'],
#                               **self.create_params['valid_data']['optional_params']}
#                 response = client.post(self.create_params['url'], data=all_params)
#                 self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#                 self.check_response_schema(self.create_params['validator'], json.loads(response.content))
#
#         after_count = self.create_params['model'].objects.count()
#         self.assertEqual(after_count, before_count + 1)
#
#         object_id = json.loads(response.content)['id']
#         self.assertTrue(self.create_params['model'].objects.filter(id=object_id).exists(),
#                         'test_create:object did not created in database')
#
#     def __check_create_401(self):
#         response = self.client.post(self.create_params['url'])
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def __check_create_403(self):
#         for forbidden_user in self.create_params['forbidden_users']:
#             authenticated_forbidden_client = self.get_authenticated_client(forbidden_user)
#             response = authenticated_forbidden_client.post(self.create_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def __check_create_405(self):
#         pass
#
#     def __check_create_400(self, clients):
#         for client in clients:
#             if self.create_params.get('invalids_data'):
#                 for invalid_data in self.create_params['invalids_data']:
#                     response = client.post(self.create_params['url'], data=invalid_data)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#             response = client.post(self.create_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#             invalid_data_total = dict()
#             items_count = len(self.create_params['valid_data']['required_params'].items())
#
#             for key, value in self.create_params['valid_data']['required_params'].items():
#                 items_count -= 1
#                 invalid_data = dict()
#                 invalid_data.update({key: value})
#                 invalid_data_total.update({key: value})
#
#                 if items_count != 0:
#                     response = client.post(self.create_params['url'], data=invalid_data)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#                     response = client.post(self.create_params['url'], data=invalid_data_total)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class TestUpdateMixin(AuthMixin):
#     """
#      usage example:
#         self.base_object = Article.objects.create(title="title1",author=self.staff1)
#
#         self.update_params = {
#            'model': Article,
#            'object':self.base_object,
#            'url': f'/api/v1/article/{self.base_object.id}/',
#            'legal_users': [self.user1, ]
#            'forbidden_users':[self.user2,]
#            'not_found_users':[self.user3,]
#            'valid_data':{
#                 required_params:{'author':self.admin.id},
#                 optional_params:{'title':'title1'},
#             }
#            'invalids_data':[{some key and values},]
#            'validator':article_validator
#         }
#
#         Note : not-found-users --> check 404 error
#     """
#
#     def test_update(self):
#
#         self.assertTrue(hasattr(self, 'update_params'), 'update_params must be defined')
#
#         self.assertTrue(isinstance(self.update_params, dict), 'update_params must be a dictionary.')
#
#         self.assertIsNotNone(self.update_params.get('url'), 'update_params: url must be defined')
#
#         self.assertIsNotNone(self.update_params.get('model'), 'update_params: model class must be defined')
#
#         self.assertIsNotNone(self.update_params.get('object'), 'update_params: object must be defined')
#
#         self.assertIsNotNone(self.update_params.get('valid_data'),
#                              'update_params: valid_data dictionary must be defined')
#
#         self.assertIsNotNone(self.update_params['valid_data'].get('required_params'),
#                              'update_params: required_params dictionary in valid_data must be defined')
#
#         self.assertIsNotNone(self.update_params.get('validator'),
#                              'update_params: validator must be defined')
#
#         self.__run_update_test()
#
#     def __run_update_test(self):
#
#         self.__check_update_401()
#
#         if self.update_params.get('forbidden_users'):
#             self.__check_update_403()
#
#         if self.update_params.get('not_found_users'):
#             self.__check_update_404()
#
#         self.__check_update_400()
#
#         self.__check_update_200()
#
#     def __check_update_200(self):
#         self.assertGreater(len(self.update_params['legal_users']), 0,
#                            'update_params:legal_users list must not be empty!')
#
#         for user in self.update_params['legal_users']:
#             authenticated_legal_client = self.get_authenticated_client(user)
#             response = authenticated_legal_client.put(self.update_params['url'],
#                                                       data=self.update_params['valid_data']['required_params'])
#             self.assertEqual(response.status_code, status.HTTP_200_OK)
#             self.check_response_schema(self.update_params['validator'], json.loads(response.content))
#
#             if self.update_params['valid_data'].get('optional_params'):
#                 all_params = {**self.update_params['valid_data']['required_params'],
#                               **self.update_params['valid_data']['optional_params']}
#                 response = authenticated_legal_client.put(self.update_params['url'], data=all_params)
#                 self.assertEqual(response.status_code, status.HTTP_200_OK)
#                 self.check_response_schema(self.update_params['validator'], json.loads(response.content))
#
#             changed_object = self.update_params['model'].objects.get(id=self.update_params['object'].id)
#
#             attrs_values = [(key, value) for key, value in changed_object.__dict__.items() if
#                             key in self.update_params['valid_data'].keys() or key in list(
#                                 map(lambda x: x + '_id', list(self.update_params['valid_data'].keys())))]
#
#             for attr_value in attrs_values:
#                 self.assertEqual(attr_value[1], self.update_params['valid_data'][attr_value[0].replace('_id', '')])
#
#     def __check_update_400(self):
#         self.assertGreater(len(self.update_params['legal_users']), 0,
#                            'update_params:legal_users list must not be empty!')
#
#         for user in self.update_params['legal_users']:
#             authenticated_legal_client = self.get_authenticated_client(user)
#             response = authenticated_legal_client.put(self.update_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#             if self.update_params.get('invalids_data'):
#                 for invalid_data in self.update_params['invalids_data']:
#                     response = authenticated_legal_client.put(self.update_params['url'], data=invalid_data)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#             invalid_data_total = dict()
#             items_count = len(self.update_params['valid_data']['required_params'].items())
#
#             for key, value in self.update_params['valid_data']['required_params'].items():
#                 items_count -= 1
#                 invalid_data = dict()
#                 invalid_data.update({key: value})
#                 invalid_data_total.update({key: value})
#
#                 if items_count != 0:
#                     response = authenticated_legal_client.put(self.update_params['url'], data=invalid_data)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#                     response = authenticated_legal_client.put(self.update_params['url'], data=invalid_data_total)
#                     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def __check_update_401(self):
#         response = self.client.put(self.update_params['url'])
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def __check_update_403(self):
#         for forbidden_user in self.update_params['forbidden_users']:
#             authenticated_forbidden_client = self.get_authenticated_client(forbidden_user)
#             response = authenticated_forbidden_client.put(self.update_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def __check_update_404(self):
#         for not_found_user in self.update_params['not_found_users']:
#             authenticated_not_found_client = self.get_authenticated_client(not_found_user)
#             response = authenticated_not_found_client.put(self.update_params['url'])
#             self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def __check_update_405(self):
#         pass
#
#
# class ModelViewSetTestMixin(TestRetrieveMixin, TestListMixin, TestCreateMixin, TestUpdateMixin, TestDestroyMixin):
#     pass
