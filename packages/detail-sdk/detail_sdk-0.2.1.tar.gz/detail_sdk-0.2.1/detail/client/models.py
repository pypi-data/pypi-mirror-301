import typing
from dataclasses import dataclass,field,replace
from detail.client.logs import truncated_repr
@dataclass
class Call:
	name:str;args:typing.Tuple=field(default_factory=tuple);kwargs:typing.Dict[(str,typing.Any)]=field(default_factory=dict)
	@classmethod
	def build(A,name,*B,**C):return A(name,B,C)
	def override(A,*B,**C):return replace(A,args=B,kwargs=C)
	def __str__(B):
		C=', ';A='';D=C.join([truncated_repr(A)for A in B.args]);E=C.join(['%s=%s'%(A,truncated_repr(B))for(A,B)in B.kwargs.items()])
		if D:A=D
		if E:
			if A:A+=C
			A+=E
		return f"{B.name}({A})"