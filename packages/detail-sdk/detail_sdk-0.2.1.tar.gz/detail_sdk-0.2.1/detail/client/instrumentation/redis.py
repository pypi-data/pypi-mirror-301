from typing import Collection
from opentelemetry.trace import SpanKind,get_tracer
from wrapt import wrap_function_wrapper
from detail.client.instrumentation.wrappers import get_pure_wrapper
from detail.client.instrumentor import Instrumentor
class RedisInstrumentor(Instrumentor):
	__version__='0.1'
	def instrumentation_dependencies(A):return['redis >= 2.6']
	@staticmethod
	def get_targets():A='redis.client';import redis as B;C='BasePipeline'if B.VERSION<(3,0,0)else'Pipeline';D='StrictRedis'if B.VERSION<(3,0,0)else'Redis';return[('redis',f"{D}.execute_command"),(A,f"{C}.execute"),(A,f"{C}.immediate_execute_command"),(A,'PubSub.execute_command'),(A,'PubSub.parse_response')]
	def _instrument(A,**D):
		B=get_tracer(__name__)
		for C in A.get_targets():wrap_function_wrapper(*C,get_pure_wrapper(B,'redis',kind=SpanKind.CLIENT))
	def _uninstrument(A,**B):0