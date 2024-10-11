from contextlib import ContextDecorator
from contextvars import ContextVar
from typing import Any,Optional,Type
class DisableDetail(ContextDecorator):
	_cvar=ContextVar('disable',default=False)
	def __enter__(A):A._cvar_token=A._cvar.set(True)
	def __exit__(A,exc_type,exc_value,exc_traceback):A._cvar.reset(A._cvar_token)
	@classmethod
	def is_disabled(A):return A._cvar.get()