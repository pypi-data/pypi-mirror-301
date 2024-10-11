_C='informational'
_B='qualname'
_A='sqlalchemy'
import typing,wrapt
from opentelemetry.trace import SpanKind,get_tracer
from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2
from detail.client.attrs import build_attributes,is_active,set_attributes
from detail.client.disable import DisableDetail
from detail.client.instrumentor import Instrumentor
def create_connection_wrapper(wrapped,instance,args,kwargs):
	B=kwargs;A=wrapped
	if DisableDetail.is_disabled():return A(*args,**B)
	with get_tracer(__name__).start_as_current_span(A.__qualname__,kind=SpanKind.CLIENT)as C:
		D=A(*args,**B)
		if is_active(C):E=build_attributes(_A,{_B:A.__qualname__,_C:True});set_attributes(C,E)
		return D
def dialect_initialize_wrapper(wrapped,instance,args,kwargs):
	B=kwargs;A=wrapped
	if DisableDetail.is_disabled():return A(*args,**B)
	with get_tracer(__name__).start_as_current_span(A.__qualname__,kind=SpanKind.CLIENT)as C:
		D=A(*args,**B)
		if is_active(C):E=build_attributes(_A,{_B:A.__qualname__,_C:True});set_attributes(C,E)
		return D
class SQLAlchemyInstrumentor(Instrumentor):
	def instrumentation_dependencies(A):return[_A]
	def _instrument(A,**B):from sqlalchemy.pool.base import Pool;wrapt.wrap_function_wrapper(Pool,'_create_connection',create_connection_wrapper);wrapt.wrap_function_wrapper(PGDialect_psycopg2,'initialize',dialect_initialize_wrapper)
	def _uninstrument(A,**B):0