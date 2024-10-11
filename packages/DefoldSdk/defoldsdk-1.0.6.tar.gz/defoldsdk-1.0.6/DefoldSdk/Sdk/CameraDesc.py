
from google.protobuf.text_format import  MessageToString
from DefoldSdk.naitivesdk import SdkDefold
if SdkDefold.__CREATED__ == False  : 
	SdkDefold.CreateSdk()

class CameraDesc(SdkDefold.CameraDesc) : 
	__mule__ = True
	__ext__ = ".camera"
	def on_field_changed(self,name = None, value = None) : 
		if self.PARENT is not None : 
			self.PARENT.data = MessageToString(self.to_proto(),as_one_line = False)