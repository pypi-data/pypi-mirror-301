from typing import Any
from django.contrib.sessions.backends.base import CreateError, SessionBase, UpdateError
from django.utils import timezone
from . import cfg

class SessionStore(SessionBase):
	def __init__(self, session_key: str | None = None, **kwargs: Any) -> None:
		super().__init__(session_key, **kwargs)
		cfg._bool()

	def get_snap(self, id):
		snap = None
		doc_ref = cfg._FIRESTORE_SESSION_COL.document(id)
		snapshot = doc_ref.get()
		if snapshot.exists:
			snap = snapshot

		return snap

	def _get_session_from_db(self) -> dict | None:
		try:
			session_snap = self.get_snap(self.session_key)
			if session_snap:
				session = session_snap.to_dict()
				if session and session["expire_date"] > timezone.now().isoformat():
					return session
		except:
			pass

		self._session_key = None
		return None

	def exists(self, session_key):
		session_snap = self.get_snap(session_key)
		return session_snap.exists if session_snap else False

	def create(self):
		while True:
			self._session_key = self._get_new_session_key()
			try:
				# Save immediately to ensure we have a unique entry in the
				# database.
				self.save(must_create=True)
			except CreateError:
				# Key wasn't unique. Try again.
				continue
			self.modified = True
			return
	
	def save(self, must_create=False):

		if self.session_key is None:
			return self.create()
		
		session_data = self._get_session(no_load=must_create)
		doc_ref = cfg._FIRESTORE_SESSION_COL.document(self.session_key)

		data = {
			"session_key": self.session_key,
			"session_data": self.encode(session_data),
			"expire_date": self.get_expiry_date().isoformat(),
		}

		doc_created = doc_ref.set(data)

		if not doc_created:
			if must_create:
				raise CreateError
			else:
				raise UpdateError
		
		return True

	def delete(self, session_key=None):
		if session_key is None:
			if self.session_key is None:
				return
			session_key = self.session_key

		doc_ref = cfg._FIRESTORE_SESSION_COL.document(self.session_key)
		doc_ref.delete()
	
	def load(self):
		session = self._get_session_from_db()
		session_data = self.decode(session["session_data"]) if session else {}
		return session_data
	
	@classmethod
	def clear_expired(cls):
		stream = cfg._FIRESTORE_SESSION_COL.where("expire_date", "<", timezone.now().isoformat()).stream()

		for doc in stream:
			doc.reference.delete()