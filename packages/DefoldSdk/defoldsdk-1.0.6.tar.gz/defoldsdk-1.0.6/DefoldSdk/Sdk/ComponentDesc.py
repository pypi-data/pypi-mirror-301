
from DefoldSdk.naitivesdk import SdkDefold
if SdkDefold.__CREATED__ == False  : 
	SdkDefold.CreateSdk()

class ComponentDesc(SdkDefold.ComponentDesc) : 
	__mule__ = True
	def __preinit__(self,*args,**kwargs) : 
		self.component = ""