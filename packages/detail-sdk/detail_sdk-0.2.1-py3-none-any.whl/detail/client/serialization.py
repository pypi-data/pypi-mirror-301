_O='struct_time'
_N='initargs'
_M='builtin_type'
_L='protobuf'
_K='possible_modules'
_J='message'
_I='init_kwargs'
_H='init_args'
_G='Column'
_F='iso8601'
_E='utf-8'
_D='utf8'
_C='tuple'
_B='name'
_A=None
import builtins,dataclasses,importlib,json,sys,time,typing
from base64 import b64decode,b64encode
from datetime import date,datetime,timedelta,timezone
from io import BytesIO
from typing import Any,Dict,Type
from uuid import UUID
import google.protobuf,google.protobuf.descriptor,google.protobuf.descriptor_pb2,google.protobuf.message,google.protobuf.reflection
from detail.client.logs import get_detail_logger
from detail.client.models import Call
proto_pool=google.protobuf.descriptor._message.default_pool
psycopg2_types={_G:_A,'AsIs':_A,'QuotedString':_A,'Binary':_A}
try:import psycopg2.extensions
except ImportError:pass
else:
	for name in psycopg2_types:psycopg2_types[name]=getattr(psycopg2.extensions,name,_A)
TYPE_KEY='__detail_json_type__'
known_lossy_type_strs={"<class 'dateutil.tz.tz.tzutc'>","<class 'dateutil.tz.tz.tzlocal'>","<class 'dateutil.tz.tz.tzwinlocal'>"}
LOSSY_REPR='lossy-repr'
builtin_types={A for A in builtins.__dict__.values()if isinstance(A,type)}
logger=get_detail_logger(__name__)
def decode_bytes(obj):
	A=obj
	if _D in A:return A[_D].encode(_E)
	else:return b64decode(A['b64'])
def encode_bytes(obj):
	B=obj;A={}
	try:A[_D]=B.decode(_E)
	except UnicodeDecodeError:A['b64']=b64encode(B).decode(_E)
	A[TYPE_KEY]=str(B.__class__.__name__);return A
def encode_psycopg2_type(type,obj):
	A=obj;B=[];C={}
	if type==psycopg2_types[_G]:E=[A for A in dir(A)if not A.startswith('_')];C={B:getattr(A,B)for B in E}
	else:B=[A.adapted]
	D={_H:B,_I:C};D[TYPE_KEY]=f"psycopg2.extensions.{type.__name__}";return D
def encode_proto(message):A=message;B=[B for B in sys.modules if B.endswith(A.__module__)];return{TYPE_KEY:_L,_J:A.SerializeToString(),_B:A.DESCRIPTOR.full_name,_K:B}
def decode_proto(obj):
	A=obj
	for B in A[_K]:importlib.import_module(B)
	C=proto_pool.FindMessageTypeByName(A[_B]);return google.protobuf.reflection.ParseMessage(C,A[_J])
def encode_call(call):A=dataclasses.asdict(call);A['TYPE_KEY']='Call';return A
def decode_call(obj):return Call(**obj)
class DetailEncoder(json.JSONEncoder):
	def default(G,obj):
		F='repr';D='type';A=obj
		try:hash(A)
		except TypeError:pass
		else:
			if A in builtin_types:B={_B:A.__name__};B[TYPE_KEY]=_M;return B
		if isinstance(A,(datetime,date)):B={_F:A.isoformat()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timezone):assert hasattr(A,'__getinitargs__');B={_N:A.__getinitargs__()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timedelta):B={'days':A.days,'seconds':A.seconds,'microseconds':A.microseconds};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,bytes):return encode_bytes(A)
		if isinstance(A,UUID):B={'str':str(A)};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,google.protobuf.message.Message):return encode_proto(A)
		if isinstance(A,Call):return encode_call(A)
		if isinstance(A,memoryview):return encode_bytes(A.tobytes())
		if isinstance(A,BytesIO):return encode_bytes(A.read())
		for C in psycopg2_types.values():
			if C is not _A and isinstance(A,C):return encode_psycopg2_type(C,A)
		try:E=super().default(A)
		except TypeError:
			B={D:str(type(A)),F:repr(A)};B[TYPE_KEY]=LOSSY_REPR
			if B[D]not in known_lossy_type_strs:logger.warning("encoding %s with lossy repr '%s'; add serilization support or add to known_lossy_type_strs",B[D],B[F],stack_info=True)
			return B
		assert isinstance(E,dict);return E
	def encode(A,obj):
		def B(item):
			A=item
			if isinstance(A,time.struct_time):C={_C:B(tuple(A))};C[TYPE_KEY]=_O;return C
			elif isinstance(A,tuple):return{TYPE_KEY:_C,'items':[B(A)for A in A]}
			elif isinstance(A,list):return[B(A)for A in A]
			elif isinstance(A,dict):return{A:B(C)for(A,C)in A.items()}
			else:return A
		return super().encode(B(obj))
class DetailDecoder(json.JSONDecoder):
	def __init__(A,*B,**C):json.JSONDecoder.__init__(A,*B,object_hook=A.object_hook,**C)
	def object_hook(E,obj):
		A=obj;B=A.pop(TYPE_KEY,_A)
		if B==_M:return builtins.__dict__[A[_B]]
		if isinstance(B,str)and B.startswith('psycopg2.extensions'):D=B.rsplit('.')[-1];C=psycopg2_types[D];assert C is not _A,f"psycopg2 is required to deserialize {B}; was detail installed with the replay extras?";return C(*A[_H],**A[_I])
		if B==_C:return tuple(A['items'])
		if B=='datetime':return datetime.fromisoformat(A[_F])
		if B=='date':return date.fromisoformat(A[_F])
		if B=='timezone':return timezone(*A[_N])
		if B=='timedelta':return timedelta(**A)
		if B==_O:return time.struct_time(A[_C])
		if B=='bytes':return decode_bytes(A)
		if B=='UUID':return UUID(A['str'])
		if B==_L:return decode_proto(A)
		if B=='Call':return decode_call(A)
		if B=='memoryview':return memoryview(decode_bytes(A))
		if B=='BytesIO':return BytesIO(decode_bytes(A))
		if B==LOSSY_REPR:A[TYPE_KEY]=B;return A
		return A