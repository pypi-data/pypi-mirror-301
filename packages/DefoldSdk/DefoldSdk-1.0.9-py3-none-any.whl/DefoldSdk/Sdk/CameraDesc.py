
from google.protobuf.text_format import  MessageToString
from DefoldSdk.Naitivesdk import sdk 


class CameraDesc(sdk.CameraDesc) : 
	__mule__ = True
	__ext__ = ".camera"
	def on_field_changed(self,name = None, value = None) : 
		if self.PARENT is not None : 
			self.PARENT.data = MessageToString(self.to_proto(),as_one_line = False)