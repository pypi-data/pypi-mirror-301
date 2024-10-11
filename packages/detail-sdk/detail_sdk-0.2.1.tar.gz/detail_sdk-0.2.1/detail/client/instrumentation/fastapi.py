_B='headers'
_A='http'
import json,typing
from typing import Any
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from detail.client.attrs import Attributes,build_attributes,is_active,set_attributes
from detail.client.serialization import DetailEncoder
def server_request_hook(span,scope):
	C='http.route';A=span
	if is_active(A):
		B={};B['request.headers']=json.dumps(scope[_B],cls=DetailEncoder)
		if C in A.attributes:B['request.route']=A.attributes[C]
		D=build_attributes(_A,B);set_attributes(A,D)
def client_request_hook(span,scope,message):
	A=message
	if is_active(span):
		B={};C=A['type']
		if C=='http.request':B['request.bodychunk']=json.dumps(A.get('body',b''),cls=DetailEncoder)
		D=build_attributes(_A,B);set_attributes(span,D)
def client_response_hook(span,scope,message):
	A=message
	if is_active(span):
		B={};C=A['type']
		if C=='http.response.start':B['response.headers']=json.dumps(A.get(_B,[]),cls=DetailEncoder)
		elif C=='http.response.body':B['response.bodychunk']=json.dumps(A.get('body',b''),cls=DetailEncoder)
		D=build_attributes(_A,B);set_attributes(span,D)
class DetailFastAPIInstrumentor(FastAPIInstrumentor):
	def _instrument(B,**A):A['server_request_hook']=server_request_hook;A['client_request_hook']=client_request_hook;A['client_response_hook']=client_response_hook;super()._instrument(**A)