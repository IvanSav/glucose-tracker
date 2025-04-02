import uuid
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Glucose


class GlucoseAPITestCase(APITestCase):

    def setUp(self):
        """Create test data before running tests"""
        self.user_id = uuid.uuid4()
        self.glucose = Glucose.objects.create(
            user_id=self.user_id,
            timestamp=datetime(2024, 3, 28, 9, 0),
            record_type=1,
            glucose_value_trend=120,
            glucose_scan=125,
        )
        self.list_url = reverse("glucose-list")  # DRF auto-generated route
        self.detail_url = reverse("glucose-detail", args=[self.glucose.id])

    def test_list_glucose_levels(self):
        """Test retrieving a list of glucose levels"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_glucose_level(self):
        """Test retrieving a specific glucose level by ID"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.glucose.id)

    def test_create_glucose_level(self):
        """Test creating a new glucose record via API"""
        data = {
            "user_id": str(uuid.uuid4()),
            "timestamp": "2024-03-29T10:00:00",
            "record_type": 0,
            "glucose_value_trend": 110,
            "glucose_scan": 115,
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Glucose.objects.count(), 2)

    def test_filter_glucose_by_user_id(self):
        """Test filtering glucose records by user_id"""
        response = self.client.get(self.list_url, {"user_id": self.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_bulk_upload_glucose_data(self):
        """Test bulk upload endpoint for glucose data"""
        bulk_url = reverse("glucose-populate")  # Uses @action(detail=False)
        data = [
            {
                "user_id": str(uuid.uuid4()),
                "timestamp": "2024-03-29T10:00:00",
                "record_type": 0,
                "glucose_value_trend": 130,
                "glucose_scan": 135,
            },
            {
                "user_id": str(uuid.uuid4()),
                "timestamp": "2024-03-29T11:00:00",
                "record_type": 1,
                "glucose_value_trend": 140,
                "glucose_scan": 145,
            },
        ]
        response = self.client.post(bulk_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Glucose.objects.count(), 3)
