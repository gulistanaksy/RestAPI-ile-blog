import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


#  doğru veriler ile kayıt işlemi yap.
#  şifre invalid olabilir.
#  kullanıcı adı kullanılmış olabilir.
#  üye girişi yaptıysak sayfa o gözükmemeli.
#  token ile giriş işlemi yapıldığında 403 hatası.


class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")    # account içindeki register urli
    url_login = reverse("token_obtain_pair")

    def test_user_registration(self):
        """
            Doğru veriler ile kayıt işlemi.
        """
        data = {
            "username": "gulistantest",
            "password": "TestDeneme123"
        }
        response = self.client.post(self.url, data)  # -- register urline data verileri ile post işlemi. -- bu işlem sonucu dönen kod alınır.
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        """
            invalid password verisi ile kayıt işlemi.
        """

        data = {
            "username": "gulistantest",
            "password": "1"
        }

        response = self.client.post(self.url,
                                    data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        """
            Benzersiz isim test.
        """
        self.test_user_registration()
        data = {
            "username" : "gulistantest",
            "password" : "1"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registratation(self):
        """
            session ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()                                           # kullanıcıyı oluşturduk.
        self.client.login(username="gulistantest", password="TestDeneme123")    # kullanıcı girişi yaptık.
        response=self.client.get(self.url)                                      # url'e get isteği yaptık.
        self.assertEqual(403, response.status_code)

    def test_user_authenticated_token_registratation(self):
        """
            session ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()  # kullanıcıyı oluşturduk.
        data = {
            "username": "gulistantest",
            "password": "TestDeneme123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ token)    # her istek yaptığımızda arka planda header'a bunu yerleştiriyoruz.
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)

class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):    # otomatik çalışır.
        self.username = "Gulistantest123"
        self.password = "testDeneme123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login, {"username":"Gulistantest123","password":"testDeneme123"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):   # olmayan kullanıcı girişi.
        response = self.client.post(self.url_login, {"username": "Gulistantest12i3", "password": "testDeneme123"})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)

class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_login = reverse("token_obtain_pair")

    def setUp(self):    # otomatik çalışır.
        self.username = "Gulistantest123"
        self.password = "testDeneme123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username" : "Gulistantest123",
            "password" : "testDeneme123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ token)


    #oturum yaılmadan girildiğinde hata.
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401,response.status_code)

    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "old_password": "testDeneme123",
            "new_password": "Yenisifretest123"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_informations(self):
        self.login_with_token()
        data = {
            "old_password": "fvyjhvg",
            "new_password": "Yenisifretest123"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(400,response.status_code)


class UserProfileUpdate(APITestCase):
    url = reverse("account:me")
    url_login = reverse("token_obtain_pair")

    def setUp(self):    # otomatik çalışır.
        self.username = "Gulistantest123"
        self.password = "testDeneme123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def login_with_token(self):
        data = {
            "username" : "Gulistantest123",
            "password" : "testDeneme123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer '+ token)


    #oturum yaılmadan girildiğinde hata.
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401,response.status_code)

    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "id":"",
            "first_name":"",
            "last_name":"",
            "profile":{
                "id":1,
                "note":"",
                "twitter":""
            }
        }
        response = self.client.put(self.url, data, format='json')   # json formatında olduğunun belirttik.
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content),data)



