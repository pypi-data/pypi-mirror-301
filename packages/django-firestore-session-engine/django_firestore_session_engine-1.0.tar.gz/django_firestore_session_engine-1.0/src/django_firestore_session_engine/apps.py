from django.apps import AppConfig
from django.conf import settings
from . import cfg

class DjangoFirestoreSessionEngine(AppConfig):
	"""Configuration for Django app."""
	
	name = "django-firestore-session-engine"
	verbose_name = "Django Firestore Session Engine"

	def ready(self):
		"""Fetches package-specific constant values from settings. It looks
		for the following variables:

	    	FIRESTORE_SESSION_COL
	    		Auth0 application's client_id

	    If any of the above information is missing, an Exception is raised.
		"""
		
		if hasattr(settings, "FIRESTORE_SESSION_COL"):
			cfg._FIRESTORE_SESSION_COL = settings.FIRESTORE_SESSION_COL
		else:
			raise NameError("settings.FIRESTORE_SESSION_COL is Missing")
