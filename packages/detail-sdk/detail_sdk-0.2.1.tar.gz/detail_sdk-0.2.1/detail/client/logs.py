import base64,hashlib,logging,os,typing
from logging.config import dictConfig
from detail.client.disable import DisableDetail
TRACE=logging.DEBUG-5
MAX_PARAM_LEN=4096
def _truncate(s,max_len):
	A=max_len
	if len(s)>A:
		try:hash='hash:'+base64.b64encode(hashlib.md5(s.encode()).digest()).decode()
		except Exception:hash='<unable to hash>'
		B=s[:A];s=f"{B}...[len:{len(s)} {hash}]'"
	return s
def truncated_str(s,max_len=MAX_PARAM_LEN):
	if isinstance(s,bytes):
		try:A=s.decode('utf-8')
		except UnicodeDecodeError:A=repr(s)
	else:A=s
	return _truncate(A,max_len=max_len)
def truncated_repr(val,max_len=MAX_PARAM_LEN):return _truncate(repr(val),max_len=max_len)
def init():
	J='logging.StreamHandler';I='formatter';H='class';G='console_verbose';F='format';E='withfile';D='simple';C=False;B='handlers';A=os.environ.get('DETAIL_LOG_LEVEL')
	if A:logging.addLevelName(TRACE,'TRACE');dictConfig({'version':1,'disable_existing_loggers':C,'formatters':{D:{F:'%(levelname)s: [%(asctime)s] %(name)s: %(message)s'},E:{F:'%(levelname)s: [%(asctime)s] (%(module)s:%(lineno)s): %(message)s'}},B:{'console_simple':{H:J,I:D},G:{H:J,I:E}},'loggers':{'detail':{B:[G],'level':A,'propagate':C}}});get_detail_logger(__name__).info('detail logging enabled at level %s',A)
class DetailLogger(logging.Logger):
	def trace(A,msg,*B,**C):A.log(TRACE,msg,*B,**C)
	def _log(C,*A,**B):
		with DisableDetail():return super()._log(*A,**B,stacklevel=2)
def get_detail_logger(*B,**C):A=logging.Logger.manager;D=A.loggerClass;A.loggerClass=DetailLogger;E=logging.getLogger(*B,**C);A.loggerClass=D;return E