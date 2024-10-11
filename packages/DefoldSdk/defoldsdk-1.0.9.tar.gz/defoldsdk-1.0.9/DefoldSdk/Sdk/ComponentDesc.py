
from DefoldSdk.Naitivesdk import sdk 

class ComponentDesc(sdk.ComponentDesc) : 
	__mule__ = True
	def __preinit__(self,*args,**kwargs) : 
		self.component = ""