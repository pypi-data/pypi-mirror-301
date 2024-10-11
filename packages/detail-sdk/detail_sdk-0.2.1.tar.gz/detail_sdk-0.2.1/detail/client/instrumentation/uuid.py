import uuid
from typing import Collection
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation.wrappers import get_pure_wrapper
from detail.client.instrumentor import Instrumentor
class UUIDInstrumentor(Instrumentor):
	uuid_functions=['getnode','uuid1','uuid3','uuid4','uuid5']
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in A.uuid_functions:wrap_function_wrapper(uuid,C,get_pure_wrapper(B,'uuid'))
	def _uninstrument(A,**B):0