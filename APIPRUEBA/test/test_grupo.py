from django.test import TestCase
from .models import Rol

class RolModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Rol.objects.create(id_Rol='1', Descripción='Test Rol')

    def test_descripcion_label(self):
        rol = Rol.objects.get(id=1)
        field_label = rol._meta.get_field('Descripción').verbose_name
        self.assertEquals(field_label, 'v')

    def test_descripcion_max_length(self):
        rol = Rol.objects.get(id=1)
        max_length = rol._meta.get_field('Descripción').max_length
        self.assertEquals(max_length, 45)
