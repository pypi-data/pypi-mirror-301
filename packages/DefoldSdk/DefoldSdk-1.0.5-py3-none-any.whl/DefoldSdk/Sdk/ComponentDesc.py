
from DefoldSdk.naitivesdk import SdkDefold as nsdk 

class ComponentDesc(nsdk.ComponentDesc) : 
	__mule__ = True
	def __preinit__(self,*args,**kwargs) : 
		self.component = ""