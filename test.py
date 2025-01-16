import unittest
from test2.app import create_app, db
from test2.models import Product

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_product(self, name="Test Product", description="Test Description"):
        return self.client.post('/resource', json={"name": name, "description": description})

    def test_create_product(self):
        response = self.create_test_product()
        self.assertEqual(response.status_code, 201)

    def test_create_duplicate_product(self):
        self.create_test_product(name="Unique Product")
        response = self.create_test_product(name="Unique Product")
        self.assertEqual(response.status_code, 400)  # Assuming duplicates are not allowed

    def test_get_products(self):
        self.create_test_product()
        response = self.client.get('/resource')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

    def test_get_product_by_id(self):
        self.create_test_product()
        response = self.client.get('/resource/1')
        self.assertEqual(response.status_code, 200)

    def test_get_product_not_found(self):
        response = self.client.get('/resource/999')
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        self.create_test_product()
        response = self.client.put('/resource/1', json={"name": "Updated Name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Updated Name")

    def test_delete_product(self):
        self.create_test_product()
        response = self.client.delete('/resource/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product deleted", response.json["message"])

    def test_delete_nonexistent_product(self):
        response = self.client.delete('/resource/999')
        self.assertEqual(response.status_code, 404)
