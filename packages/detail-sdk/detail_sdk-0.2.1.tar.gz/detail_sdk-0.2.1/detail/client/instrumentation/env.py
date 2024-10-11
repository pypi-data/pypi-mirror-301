import json,os,sys
from typing import Collection
from opentelemetry.trace import get_tracer
from detail.client.attrs import build_attributes,is_active,set_attributes
from detail.client.instrumentor import Instrumentor
from detail.client.serialization import DetailEncoder
class EnvInstrumentor(Instrumentor):
	def instrumentation_dependencies(A):return[]
	def _instrument(E,**F):
		B='environ';C=get_tracer(__name__)
		with C.start_as_current_span(B)as A:
			if is_active(A):D=build_attributes('env',{B:json.dumps(dict(os.environ),cls=DetailEncoder),'argv':json.dumps(sys.argv,cls=DetailEncoder)});set_attributes(A,D)
	def _uninstrument(A,**B):0