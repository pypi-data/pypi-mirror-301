import threading
from contextvars import ContextVar
from typing import Optional
from detail.client import logs
logger=logs.get_detail_logger(__name__)
class ThreadIndex:
	_cvar=ContextVar('thread_index');_index=0;_lock=threading.Lock()
	@classmethod
	def get(A):
		B=threading.current_thread()
		if B is threading.main_thread():return 0
		if A._cvar.get(None)is None:
			with A._lock:A._index+=1;A._cvar.set(A._index)
			logger.info('assigned thread index %s to thread %r (id %s)',A._cvar.get(),B.name,threading.get_ident())
		return A._cvar.get()
	@classmethod
	def reset(A):
		with A._lock:A._index=0
class WsgiSpanId:
	_wsgi_span_id=None;_lock=threading.Lock()
	@classmethod
	def set(A,span_id):
		with A._lock:A._wsgi_span_id=span_id
	@classmethod
	def get(A):
		with A._lock:return A._wsgi_span_id