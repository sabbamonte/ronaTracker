from django.test import Client, TestCase

from .models import New_Post

# Create your tests here.
class New_PostTestCase(TestCase):

    def setUp(self):
        # Create a new_post
        New_Post.objects.create(city="New York", state="NY", zip=11102, diagnosis="Healthy")
        New_Post.objects.create(city="Los Angeles", state="NY", zip=111, diagnosis="Healthy")
        New_Post.objects.create(city="Louisville", state="KY", zip=40245, diagnosis="Infected")

    def test_state_count(self):
        p = New_Post.objects.get(city="New York")
        self.assertEqual(len(p.state), 2)

    def test_valid_zip(self):
        p = New_Post.objects.get(city="New York")
        z_code = p.zip
        self.assertTrue(z_code != 0 and len(str(z_code)) == 5)

    def test_invalid_zip(self):
        p = New_Post.objects.get(city="Los Angeles")
        z_code = p.zip
        self.assertTrue(z_code == 0 or len(str(z_code)) < 5)

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

