# from django.test import TestCase
# from django.contrib.auth.models import User
# from rest_framework.test import APIClient
# from rest_framework import status

# class AuthenticationTest(TestCase):
#     def setUp(self):
#         # 테스트에 사용할 유저 데이터
#         self.user_data = {
#             'email': 'test@example.com',
#             'password': '!@#testpassword',
#             'password2': '!@#testpassword',
#         }
#         self.client = APIClient()

#     def test_registration(self):
#         response = self.client.post('/users/register/', self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().email, 'test@example.com')

#     def test_login(self):
#         # 회원가입
#         response = self.client.post('/users/register/', self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # 로그인
#         response = self.client.post('/users/login/', self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)

#     def test_login_with_invalid_credentials(self):
#         # 회원가입
#         response = self.client.post('/users/register/', self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # 잘못된 비밀번호로 로그인
#         self.user_data['password'] = 'wrongpassword'
#         response = self.client.post('/users/login/', self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
