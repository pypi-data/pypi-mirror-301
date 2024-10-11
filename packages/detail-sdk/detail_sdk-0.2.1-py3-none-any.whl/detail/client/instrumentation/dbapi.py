_D='kwargs'
_C='qualname'
_B='cursor'
_A='dbapi: %s'
import json,typing,wrapt
from opentelemetry.trace import Span,SpanKind,get_tracer
from detail.client.attrs import build_attributes,format_otel_span_id,is_active,set_attributes
from detail.client.logs import get_detail_logger
from detail.client.models import Call
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
class TracedCursor(wrapt.ObjectProxy):
	def __init__(A,cursor,client,connection):super(TracedCursor,A).__init__(cursor);A._self_execute_span=None;A._self_client=client;A._self_connection=connection
	def __execute(A,function,query,*D,**E):
		C=query;B=function;logger.trace(_A,Call.build(B,C,*D,**E));G=getattr(A.__wrapped__,B);H=G(C,*D,**E)
		with get_tracer(_B).start_as_current_span(B,kind=SpanKind.CLIENT)as F:
			A._self_execute_span=F
			if is_active(F):I={'description':A.__wrapped__.description,'rowcount':A.__wrapped__.rowcount,'lastrowid':A.__wrapped__.lastrowid};J=build_attributes('dbapi',{'client':A._self_client,_C:B,'query':C,'args':json.dumps(D,cls=DetailEncoder),_D:json.dumps(E,cls=DetailEncoder),'execute_result':json.dumps(I,cls=DetailEncoder)});set_attributes(F,J)
		if H:return A
	def execute(A,query,*B,**C):return A.__execute('execute',query,*B,**C)
	def executemany(A,query,*B,**C):return A.__execute('executemany',query,*B,**C)
	def callproc(A,proc,*B,**C):return A.__execute('callproc',proc,*B,**C)
	def __fetch(B,function,*C,**D):
		A=function;E=Call(A,C,D);logger.trace(_A,E);H=getattr(B.__wrapped__,A);F=H(*C,**D)
		if not B._self_execute_span:logger.warning('fetch without previous execute; not recording %s',E)
		else:
			with get_tracer(_B).start_as_current_span(A,kind=SpanKind.CLIENT)as G:
				if is_active(G):I=build_attributes('dbapi',{_C:A,'args':json.dumps(C,cls=DetailEncoder),_D:json.dumps(D,cls=DetailEncoder),'result':json.dumps(F,cls=DetailEncoder),'execute_span_id':format_otel_span_id(B._self_execute_span.get_span_context().span_id)});set_attributes(G,I)
		return F
	def fetchall(A):return A.__fetch('fetchall')
	def fetchone(A):return A.__fetch('fetchone')
	def fetchmany(A,*B,**C):return A.__fetch('fetchmany',*B,**C)
	def __iter__(A):return A
	def __next__(B):
		A=B.fetchone()
		if A is None:raise StopIteration
		return A
	next=__next__
class TracedConnection(wrapt.ObjectProxy):
	def __init__(A,conn,client):super(TracedConnection,A).__init__(conn);A._self_client=client
	def cursor(A,*B,**C):D=A.__wrapped__.cursor(*B,**C);return TracedCursor(D,A._self_client,A)
def get_connect_wrapper(traced_conn_cls,*A,**B):
	def C(wrapped,instance,args,kwargs):C=wrapped(*args,**kwargs);return traced_conn_cls(C,*A,**B)
	return C