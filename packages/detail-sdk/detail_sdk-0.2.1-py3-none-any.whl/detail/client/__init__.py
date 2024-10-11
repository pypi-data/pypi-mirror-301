import importlib.metadata,importlib.util,os,sys
from pathlib import Path
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor,SimpleSpanProcessor
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from opentelemetry.trace.span import format_trace_id
from detail.client import constants
from detail.client.logs import get_detail_logger
output_dir_path=Path(os.environ.get('__DETAIL_OUTPUT_DIR','.'))
logger=get_detail_logger(__name__)
try:version=importlib.metadata.version('detail-sdk')
except Exception:logger.warning("couldn't read package version",exc_info=True);version='unknown'
class BufferedExporter:
	def __init__(A):A.buffer=[];A.active=True
	def export(A,spans):
		if A.active:
			for B in spans:A.buffer.append(B)
		return 0
	def shutdown(A):A.active=False
	def force_flush(A,timeout_millis=30000):0
def instrument(api_key=None):
	K='true';J='__DETAIL_SERVICE_START_ID';E=api_key;print(f"Instrumenting with detail (pid {os.getpid()}; argv {repr(' '.join(sys.argv))})");A=TracerProvider(shutdown_on_exit=True);trace.set_tracer_provider(A);D=BufferedExporter();F=SimpleSpanProcessor(D);A.add_span_processor(F)
	for G in load_classes_from_defs(instrumentor_defs,'detail.client.instrumentation.'):logger.debug('instrument %s',G.__name__);G().instrument()
	logger.info('all instrumentors installed');from detail.client.otel import JsonLSpanExporter as L,OTLPJsonHttpExporter as M;B=os.environ.get(J)
	if not B:B=f"0x{format_trace_id(RandomIdGenerator().generate_trace_id())}";os.environ[J]=B;logger.info('generated service_start_id %s',B)
	else:logger.info('reusing parent process service_start_id %s',B)
	N=os.environ.get('__DETAIL_DEV','').lower()==K;O=os.environ.get('__DETAIL_USE_LOCAL_BACKEND','').lower()==K;C=None;E=E or os.environ.get('DETAIL_API_KEY')
	if E:
		if O:H=os.environ.get('__DETAIL_LOCAL_BACKEND_URL',constants.LOCAL_BACKEND_URL)
		else:H=constants.PROD_BACKEND_URL
		C=M(endpoint=f"{H}/v1/traces",headers={constants.PREFLIGHT_CUSTOMER_HEADER:E,constants.PREFLIGHT_VERSION_HEADER:version,constants.PREFLIGHT_CLIENT_LIBRARY_HEADER:'python',constants.PREFLIGHT_SERVICE_START_ID_HEADER:B})
	elif N:C=L(output_dir_path/'spans.jsonl')
	else:print("No Detail API key set. Use instrument(api_key='...') or the DETAIL_API_KEY env var to send traces to the Detail backend.")
	D.shutdown()
	if C:
		I=A._active_span_processor._span_processors[-1];assert I==F,f"most recent span processor is not ours: {I}";A._active_span_processor._span_processors=A._active_span_processor._span_processors[:-1];P=BatchSpanProcessor(C,max_export_batch_size=10);A.add_span_processor(P);logger.debug('configured exporter %s',C)
		if D.buffer:logger.info('exporting %s buffered spans',len(D.buffer));C.export(D.buffer)
instrumentor_defs=[('times.TimeInstrumentor',[]),('times.DatetimeInstrumentor',[]),('random.OSRandomInstrumentor',[]),('random.SystemRandomInstrumentor',[]),('random.RandomInstrumentor',[]),('uuid.UUIDInstrumentor',[]),('thread.ThreadInstrumentor',[]),('env.EnvInstrumentor',[]),('http.HttpInstrumentor',[]),('sqlite3.SQLite3Instrumentor',[]),('redis.RedisInstrumentor',['redis']),('psycopg2.Psycopg2Instrumentor',['psycopg2']),('sqlalchemy.SQLAlchemyInstrumentor',['sqlalchemy']),('grpc.DetailGrpcClientInstrumentor',['grpc']),('flask.DetailFlaskInstrumentor',['flask']),('django.DetailDjangoInstrumentor',['django']),('fastapi.DetailFastAPIInstrumentor',['fastapi']),('celery.CeleryInstrumentor',['celery'])]
def load_classes_from_defs(class_defs,path_prefix):
	for(C,D)in class_defs:
		E=path_prefix+C;F,A=E.rsplit('.',1)
		for B in D:
			G=importlib.util.find_spec(B)
			if not G:logger.info('not loading %s due to missing %s',A,B);break
		else:H=importlib.import_module(F);I=getattr(H,A);yield I
__all__=[str(A)for A in[instrument]]