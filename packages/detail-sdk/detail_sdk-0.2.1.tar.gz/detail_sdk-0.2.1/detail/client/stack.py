import inspect,pathlib,re,threading
_install_path=pathlib.Path(__file__).parent.parent.resolve()
assert str(_install_path).endswith('/detail'),f"Install path is {_install_path}, which doesn't look like the detail package root. If {__file__} changed directory depth _install_path must be updated."
install_prefix=str(pathlib.Path(_install_path).parent)
_IGNORED_CALLER_PATTERNS=[re.compile(A)for A in['/opentelemetry','/python[^/]+/asyncio/','/python[^/]+/logging/','/python[^/]+/http/server.py','/structlog/processors.py','/gunicorn/workers/workertmp.py','/gunicorn/arbiter.py','/segment/','/ddtrace/','/prometheus_client/','/httpx/_utils.py','/sqlalchemy/sql/compiler.py','/[c|C]overage']]
def get_caller_path():return _format_caller_path(_find_true_caller_path())
def is_ignored_caller(caller_path):return in_ignored_thread()or _is_in_patterns(caller_path,_IGNORED_CALLER_PATTERNS)
def get_thread_name():return threading.current_thread().name
def in_ignored_thread():return get_thread_name()=='OtelBatchSpanProcessor'
def _is_in_patterns(s,patterns):
	for B in patterns:
		A=B.search(s)
		if A:return A
def _format_caller_path(caller_path):
	B='site-packages';A=caller_path
	if A.startswith(install_prefix):A=A[len(install_prefix):]
	if B in A:A=''.join(A.split(B)[1:])
	return A
def _is_false_caller(caller_path):A=caller_path;A=_format_caller_path(A);return A.startswith('/detail/')or A.startswith('/wrapt/')
def _find_true_caller_path():
	A=inspect.currentframe();assert A is not None,'Detail requires an interpreter with inspect.currentframe() support.'
	try:
		while _is_false_caller(A.f_code.co_filename):
			if A.f_back is None:break
			A=A.f_back
		return A.f_code.co_filename
	finally:del A