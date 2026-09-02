from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, ProfessionalProfile


class ProfessionalProfileEditTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='owner@example.com',
			email='owner@example.com',
			password='test-password',
		)
		self.category = Category.objects.create(
			name='Електричар',
			slug='elektrichar',
			meta_title='Електричар',
			meta_description='Професионални електро услуги.',
			h1_title='Електричар',
			description='Електро услуги.',
		)
		self.profile = ProfessionalProfile.objects.create(
			user=self.user,
			title='Електричар в София',
			slug='elektrichar-v-sofiya',
			description='Първоначално описание.',
			email='owner@example.com',
			city='София',
		)
		self.profile.categories.add(self.category)
		self.edit_url = reverse('edit_professional_profile', kwargs={'slug': self.profile.slug})

	def test_owner_can_edit_profile(self):
		self.client.login(username='owner@example.com', password='test-password')

		response = self.client.post(self.edit_url, {
			'title': 'Обновен електричар',
			'description': 'Обновено описание.',
			'categories': [self.category.id],
			'phone': '+359888123456',
			'email': 'owner@example.com',
			'website': '',
			'facebook': '',
			'city': 'София',
			'address': '',
		})

		self.assertRedirects(response, reverse('professional_profile', kwargs={'slug': self.profile.slug}))
		self.profile.refresh_from_db()
		self.assertEqual(self.profile.title, 'Обновен електричар')

	def test_other_user_cannot_edit_profile(self):
		other_user = User.objects.create_user('other@example.com', password='test-password')
		self.client.force_login(other_user)

		response = self.client.get(self.edit_url)

		self.assertEqual(response.status_code, 404)

# Create your tests here.
