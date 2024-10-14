_FIRESTORE_SESSION_COL = None

def _bool():
	"""Tells whether or not the engine is properly configured."""
	
	if not _FIRESTORE_SESSION_COL:
		raise NameError("settings.FIRESTORE_SESSION_COL is Missing")