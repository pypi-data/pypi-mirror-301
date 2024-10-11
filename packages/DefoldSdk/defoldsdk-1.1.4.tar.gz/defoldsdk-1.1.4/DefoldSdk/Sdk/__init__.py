import sys , os 
import importlib , glob 
from PyDefold import Defold
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.text_format import  Parse , MessageToString
from google.protobuf.json_format import MessageToDict , MessageToJson , ParseDict
import json , os , sys , glob  , collections , traceback , copy , jinja2 

class sdk : 
	pass 

doc_template = '''
# {{Class}} : 
## ```Memebers```    
```rust
{% for memeber , typememeber in Memebers.items() -%}  
{{memeber}} : {{typememeber}}  
{% endfor -%}
```

{% for enumname , typememeber in Enums.items() -%}  
## ``[ENUM]`` : `{{enumname}}`    
```python
{% for key , value in typememeber.items() -%}  
{{key}}
{% endfor -%}
```
{% endfor -%}
'''

class SdkListType(list) : 

	def __init__(self,data = list(),PARENT = None , typ = None , name = None) : 
		super().__init__(data)
		self.PARENT = PARENT
		self.name = name  
		self.types = {typ}

	def add_types(self,*args) : 
		self.types.update(args)


	def append(self,item) : 
		assert item.__class__.__name__ in self.types , f"can not append {item.__class__.__name__ } to List[{self.type}]"
		super().append(item)
		if self.PARENT != None : 
			self.PARENT.on_field_changed(msg = "")

	def extend(self,items) : 
		for itm in items : 
			self.append(item=itm )



class SdkType : 
	__id__ = None
	__sdk__ = None 
	def __init__(self,__init__ = True , **kwargs): 
		self.GAME = kwargs.get('GAME' , None)
		self.PARENT = kwargs.get('PARENT' , None)
		self.__preinit__(**kwargs)
		self.__init_message__(**kwargs)
		self.__postinit__(**kwargs)

	def __setAttr__(self,value , name) : 
		setattr(self,f"_{value}",name)
		self.on_field_changed()

	def __init_message__(self,**kwargs) : 
		self.on_field_changed()
		for name in self.fields() : 
			value = kwargs.get(name,None)
			if value is not None : 
				self.__setAttr__(value =  name , name = value )




	def __getAttr__(self,name) : 
		if not hasattr(self,f'_{name}') : self.__init__field__(name)
		return getattr(self,f'_{name}')

	def __init__field__(self,field_name) : 
		field = self.___naitive___.DESCRIPTOR.fields_by_name.get(field_name)
		if field.type == field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type message
			memeber_type_string  = field.message_type._concrete_class.__name__ 
			message_type = getattr(self.__class__ , memeber_type_string , None) 
			message_type = getattr(self.__class__.__sdk__,memeber_type_string) if message_type is None else message_type
			assert message_type is not None 
			setattr(self,f'_{field_name}' , message_type() )
		if field.type == field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of message
			setattr(self,f'_{field_name}' , SdkListType(typ=field.message_type._concrete_class.__name__ , PARENT = self , name = field_name ) )
		if field.type != field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of prirmitive_types
			setattr(self,f'_{field_name}' , SdkListType(typ = self.__sdk__.PROTOBUF_TYPE_TO_PYTHON_TYPE.get(field.type) ,  PARENT = self , name = field_name) )		
		if field.type != field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type prirmitive
			setattr(self , f'_{field_name}',field.default_value)	




	def to_proto(self) : 
		self.on_proto()
		instance = self.___naitive___()
		for field_name in self.fields() : 
			attr = getattr(self,field_name,None) # field did not intialized 
			if attr is not None : 
				attr = getattr(self,f'_{field_name}')
				field = instance.DESCRIPTOR.fields_by_name.get(field_name)
				if field.type == field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type message
					memeber_type  = field.message_type._concrete_class.__name__ 
					getattr(instance , field_name).CopyFrom(attr.to_proto())
				if field.type == field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of message
					[getattr(instance , field_name).append(elem.to_proto()) for elem in attr ] 
				if field.type != field.TYPE_MESSAGE and field.label == field.LABEL_REPEATED  : # memeber type list of prirmitive_types
					[getattr(instance , field_name).append(elem) for elem in attr ] 				
				if field.type != field.TYPE_MESSAGE and field.label != field.LABEL_REPEATED  : # memeber type prirmitive
					setattr(instance , field_name,attr)	
		return instance 

	def on_proto(self) : 
		return True 
		pass 

	def update(self , **kwargs) : 
		for k , v in kwargs.items() : 
			setattr(self,k , v )
	@classmethod
	def fields(cls) : 
		return {property_name for property_name, field in cls.___naitive___.DESCRIPTOR.fields_by_name.items() }

	@classmethod
	def enums(cls) : 
		return {enum_name for enum_name in cls.___naitive___.DESCRIPTOR.enum_types_by_name  }


	def __preinit__(self, **kwargs): 
		pass 

	def __postinit__(self, **kwargs): 
		pass 

	def on_field_changed(self,msg = "") : 
		pass







class SdkDefold : 
	__CREATED__ = False 
	PROTOBUF_TYPE_TO_PYTHON_TYPE = {
		FieldDescriptor.TYPE_DOUBLE: 'float',
		FieldDescriptor.TYPE_FLOAT: 'float',
		FieldDescriptor.TYPE_INT64: 'int',
		FieldDescriptor.TYPE_UINT64: 'int',
		FieldDescriptor.TYPE_INT32: 'int',
		FieldDescriptor.TYPE_FIXED64: 'int',
		FieldDescriptor.TYPE_FIXED32: 'int',
		FieldDescriptor.TYPE_BOOL: 'bool',
		FieldDescriptor.TYPE_STRING: 'str',
		FieldDescriptor.TYPE_BYTES: 'bytes',
		FieldDescriptor.TYPE_UINT32: 'int',
		FieldDescriptor.TYPE_ENUM: 'int',
		FieldDescriptor.TYPE_SFIXED32: 'int',
		FieldDescriptor.TYPE_SFIXED64: 'int',
		FieldDescriptor.TYPE_SINT32: 'int',
		FieldDescriptor.TYPE_SINT64: 'int',
	}

	@classmethod
	def CreateSdkType(cls , defold_type) : 
		attributes = {
			'___naitive___' : defold_type , 
			'__sdk__' : cls 
		}
		for property_name, field in defold_type.DESCRIPTOR.fields_by_name.items(): 
			def property_getter(self, name=property_name): return self.__getAttr__(name)
			def property_setter(self, value, name=property_name): self.__setAttr__(name, value)
			attributes[f'{property_name}'] = property(property_getter , property_setter)
		## nested types 
		for member in dir(defold_type) : 
			if not (member in defold_type.DESCRIPTOR.fields_by_name) : 
				if type(getattr(defold_type,member)).__name__ == 'MessageMeta' : 
					attributes[member] = cls.CreateSdkType(getattr(defold_type,member))
		## add enum related types  
		for enum_type in defold_type.DESCRIPTOR.enum_types_by_name : 
			defold_enum = getattr(defold_type ,enum_type)
			enum_dict = {
				enum_key : enum_val
				for enum_key , enum_val in defold_enum.items()
			}
			attributes[enum_type] = collections.namedtuple(enum_type , enum_dict.keys())(**enum_dict)

		sdk_type = type(defold_type.__name__, (SdkType,), attributes)
		return sdk_type

	@classmethod
	def CreateSdk(cls) : 
		for typ_name, typ in Defold._asdict().items() : 
			sdktype = cls.CreateSdkType(typ)
			setattr(sdk , typ_name , sdktype  )
		cls.__CREATED__ = True 


SdkDefold.CreateSdk()



################################################################################################################################################

class ModelDesc(sdk.ModelDesc) : 
	__mule__ = True
	def setMaterial(self,name = "model") : 
		self.materials = [sdk.Material(name = "default" , material = self.GAME.get_material_by_name(name))]

	def setMesh(self,name) : 
		self.mesh = self.GAME.get_mesh_by_name(name)

	def setTexture(self,key,name) : 
		# check key is valid  : !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		material_proto_file = self.GAME.projectpath_2_fullpath(self.materials[0].material)
		texture_path = self.GAME.get_material_texture_by_name(name)
		texture_found  = False 
		for index , texture in enumerate(self.materials[0].textures) : 
			if texture.sampler == key : 
				self.self.materials[0].textures[index].texture = texture_path
				texture_found  = True 
		if not texture_found  : 
			self.materials[0].textures.append(
				sdk.Texture(sampler = key, texture = texture_path)
			)
		self.on_field_changed()

	def on_field_changed(self,name = None, value = None) : 
		if self.PARENT is not None : 
			self.PARENT.data = MessageToString(self.to_proto(),as_one_line = False)


sdk.ModelDesc = ModelDesc 
################################################################################################################################################
class MaterialDesc(sdk.MaterialDesc) : 
	__mule__ = True
	__ext__ = ".material"
	__form__ = '{name}.material'

	def __postinit__(self, **kwargs): 
		self.max_page_count = 1

	def __preinit__(self,*args,**kwargs) : 
		self.vp = ""
		self.fp = ""
		self.CONSTANT_TYPE = dict(Viewproj=getattr(self.ConstantType,"CONSTANT_TYPE_VIEWPROJ") ,
			User=getattr(self.ConstantType,"CONSTANT_TYPE_USER" ),
			World=getattr(self.ConstantType,"CONSTANT_TYPE_WORLD" ),
			Texture=getattr(self.ConstantType,"CONSTANT_TYPE_TEXTURE" ),
			View=getattr(self.ConstantType,"CONSTANT_TYPE_VIEW" ),
			Projection=getattr(self.ConstantType,"CONSTANT_TYPE_PROJECTION" ),
			Worldview=getattr(self.ConstantType,"CONSTANT_TYPE_WORLDVIEW" ),
			User_Matrix4=getattr(self.ConstantType,"CONSTANT_TYPE_USER_MATRIX4" ),
			Worldviewproj = getattr(self.ConstantType,"CONSTANT_TYPE_WORLDVIEWPROJ" ),
			Normal=getattr(self.ConstantType,"CONSTANT_TYPE_NORMAL") 
			)
		self.WRAP_MODES = dict(
			edge = getattr(self.WrapMode,"WRAP_MODE_CLAMP_TO_EDGE"), 
			repeat = getattr(self.WrapMode,"WRAP_MODE_REPEAT"),
			mirror = getattr(self.WrapMode,"WRAP_MODE_MIRRORED_REPEAT")
		)
		self.FILTER_MODE_MAG = dict(
			default = getattr(self.FilterModeMag , "FILTER_MODE_MAG_DEFAULT") , 
			linear = getattr(self.FilterModeMag , "FILTER_MODE_MAG_LINEAR"),
			nearest = getattr(self.FilterModeMag , "FILTER_MODE_MAG_NEAREST")
		)
		self.FILTER_MODE_MIN = {
			'default'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_DEFAULT"), 
			'linear'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_LINEAR"),
			'nearest' : getattr(self.FilterModeMin , "FILTER_MODE_MIN_NEAREST" ), 
			'linear-linear'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_LINEAR_MIPMAP_LINEAR"),
			'linear-nearest'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_LINEAR_MIPMAP_NEAREST"),
			'nearest-linear'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_NEAREST_MIPMAP_LINEAR"), 
			'nearest-nearest'  : getattr(self.FilterModeMin , "FILTER_MODE_MIN_NEAREST_MIPMAP_NEAREST")
		}

	def on_proto(self) : 
		if (self.name != "") and (self.GAME is not None) : 
			saving_folder = self.GAME.saving_folder(self)
			os.makedirs(saving_folder,exist_ok = True)
			print(saving_folder)
			vp_file = os.path.join(saving_folder,f'{self.name}.vp')
			fp_file = os.path.join(saving_folder,f'{self.name}.fp')
			print(self.vp , file = open(vp_file,"w"))
			print(self.fp , file = open(fp_file,"w"))
			self.fragment_program = self.GAME.get_project_path(fp_file)
			self.vertex_program = self.GAME.get_project_path(vp_file)

	def setvertex_constant(self,name,typ,value = None) :
		constant = self.Constant(name = name , type = self.CONSTANT_TYPE.get(typ) )
		self.vertex_constants.append(constant)

	def setfragment_constant(self,name,typ,value = None ) :
		constant = self.Constant(name = name , type =  self.CONSTANT_TYPE.get(typ))
		self.fragment_constants.append(constant)

	def setvertex_space(self,typ = 'local') : 
		self.vertex_space = {'world' : getattr(self.VertexSpace,'VERTEX_SPACE_WORLD') , 'local' : getattr(self.VertexSpace,'VERTEX_SPACE_LOCAL')}[typ]

	def setTexture(self,name,u = 'edge',v = 'edge' ,min = 'linear',mag ='linear') : 
		tex = self.Sampler(name = name , 
			wrap_u = self.WRAP_MODES.get(u), wrap_v = self.WRAP_MODES.get(v),
			filter_mag = self.FILTER_MODE_MAG.get(mag) , filter_min = self.FILTER_MODE_MIN.get(min)
		)
		self.samplers.append(tex)

	def export(self) : 
		self.on_proto()
sdk.MaterialDesc = MaterialDesc 
################################################################################################################################################
import os , tempfile , subprocess

class LuaSourceFile : 
	__mule__ = True
	__ext__ = ".script"
	def __init__(self,id   = None, GAME = None , PARENT = None ) :
		self.GAME  = GAME
		self.PARENT  = PARENT
		self.id = id 
		self._filename = self.GAME.get_project_path(self.GAME.get_saved_as(self))
		self._script  = "\n\nfunction init(self)\n\t-- Add initialization code here\n\t-- Learn more: https://defold.com/manuals/script/\n\t-- Remove this function if not needed\nend\n\nfunction final(self)\n\t-- Add finalization code here\n\t-- Learn more: https://defold.com/manuals/script/\n\t-- Remove this function if not needed\nend\n\nfunction update(self, dt)\n\t-- Add update code here\n\t-- Learn more: https://defold.com/manuals/script/\n\t-- Remove this function if not needed\nend\n\nfunction fixed_update(self, dt)\n\t-- This function is called if 'Fixed Update Frequency' is enabled in the Engine section of game.project\n\t-- Can be coupled with fixed updates of the physics simulation if 'Use Fixed Timestep' is enabled in\n\t-- Physics section of game.project\n\t-- Add update code here\n\t-- Learn more: https://defold.com/manuals/script/\n\t-- Remove this function if not needed\nend\n\nfunction on_message(self, message_id, message, sender)\n\t-- Add message-handling code here\n\t-- Learn more: https://defold.com/manuals/message-passing/\n\t-- Remove this function if not needed\nend\n\nfunction on_input(self, action_id, action)\n\t-- Add input-handling code here. The game object this script is attached to\n\t-- must have acquired input focus:\n\t--\n\t--    msg.post(\".\", \"acquire_input_focus\")\n\t--\n\t-- All mapped input bindings will be received. Mouse and touch input will\n\t-- be received regardless of where on the screen it happened.\n\t-- Learn more: https://defold.com/manuals/input/\n\t-- Remove this function if not needed\nend\n\nfunction on_reload(self)\n\t-- Add reload-handling code here\n\t-- Learn more: https://defold.com/manuals/hot-reload/\n\t-- Remove this function if not needed\nend"
		self.on_field_changed()

	@property
	def script(self) : 
		return self._script

	@script.setter
	def script(self,value) : 
		self._script = self.prettyLua(value)
		if self.GAME is not None : 
			with open(self.GAME.projectpath_2_fullpath(self._filename),"w") as buff : 
				buff.write(self.script)
		self.on_field_changed()	

	@property
	def filename(self) : 
		return self._filename

	@filename.setter
	def filename(self,value) : 
		'''
		if is set the old file deleted and the new one will be created and write the script in it 
		'''
		file_fullpath  = self.GAME.projectpath_2_fullpath(self._filename)
		if os.path.exists(file_fullpath) : 
			self.script = open(file_fullpath).read()
			os.remove(file_fullpath)
		self._filename = value
		if self.GAME is not None : 
			with open(self.GAME.projectpath_2_fullpath(self._filename),"w") as buff : 
				buff.write(self.script)
		self.on_field_changed()

	def read(self,file) : 
		if self.GAME.is_in_project(file): 
			with open(file) as buff : self.source = buff.read()
			self.filename = self.GAME.get_project_path(file) 
			self.id = os.path.basename(self.filename).replace(".script","")
		else : 
			# project path 
			full_path = file 
			with open(full_path) as buff : self.source = buff.read()
			if self.GAME.is_in_project(file) : 
				self.filename = self.GAME.get_project_path(file)
				self.id = os.path.basename(self.filename).replace(".script","")
		self.on_field_changed()

		

	def on_field_changed(self,msg = "") : 
		if self.PARENT is not None : 
			self.PARENT.component = self.filename 

	def prettyLua(self,luacode) : 
		result = luacode
		temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False) 
		temp_file.write(luacode)
		temp_file.flush()
		temp_file_path = temp_file.name
		luaformatter_binary = os.path.join(os.path.split(__file__)[0],"lua-format")
		luaformatter_binary_config = os.path.join(os.path.split(__file__)[0],"lua-format.config")
		cmd = [luaformatter_binary,temp_file_path,"-c" , luaformatter_binary_config ]
		process = subprocess.Popen(
				cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)
		output = bytes.decode(process.stdout.read())
		error = bytes.decode(process.stderr.read())
		if error == "": 
			print(error)
			result = output
		temp_file.close()
		return result
sdk.LuaSourceFile = LuaSourceFile 
################################################################################################################################################
class EmbeddedInstanceDesc(sdk.EmbeddedInstanceDesc) : 
	__mule__ = True
	def __preinit__(self, **kwargs): 
		self.COMPONENTS = list()

	def get_collection_parent(self,parent = None) : 
		_parent = self.PARENT 
		if _parent is None : 
			return None
		if type(_parent).__name__ == 'CollectionDesc' : 
			return _parent
		else : 
			return self.get_collection_parent(parent=_parent)

	def on_proto(self) : 
		for cmp in self.COMPONENTS : 
			if type(cmp).__name__ == "ComponentDesc" : 
				self.data += "components {\n " + f"{cmp.to_proto()}" + "}\n"
			if type(cmp).__name__ == "EmbeddedComponentDesc": 
				self.data += "embedded_components {\n " + MessageToString(cmp.to_proto(),as_one_line = False).replace('\n',"\n  ")  + "}\n"


	def addModel(self,id ,**kwargs) : 
		cmp = sdk.EmbeddedComponentDesc(id = id , type = "model" , PARENT = self , GAME = self.GAME)
		model = sdk.ModelDesc(**kwargs , PARENT = cmp , GAME = self.GAME)
		return model 
	def addCamera(self,id ,**kwargs) : 
		cmp = sdk.EmbeddedComponentDesc(id = id , type = "camera" , PARENT = self , GAME = self.GAME)
		model = sdk.CameraDesc(**kwargs , PARENT = cmp , GAME = self.GAME)
		return model 

	def addGameObject(self,**kwargs): 
		obj = self.get_collection_parent().addGameObject(**kwargs,GAME = self.GAME , PARENT = self)
		self.children.append(obj.id)
		return obj 

	def addScriptFile(self,id ,**kwargs) : 
		component = sdk.ComponentDesc(id = id ,  PARENT = self , GAME = self.GAME)
		scriptfile = sdk.LuaSourceFile(id = id , PARENT = component , GAME = self.GAME)
		self.COMPONENTS.append(component)
		return scriptfile
sdk.EmbeddedInstanceDesc = EmbeddedInstanceDesc 
################################################################################################################################################
class ComponentDesc(sdk.ComponentDesc) : 
	__mule__ = True
	def __preinit__(self,*args,**kwargs) : 
		self.component = ""
sdk.ComponentDesc = ComponentDesc 
################################################################################################################################################
class CollectionDesc(sdk.CollectionDesc) : 
	__mule__ = True
	__ext__ = ".collection"
	__form__ = '{name}.collection'
	def __preinit__(self, **kwargs): 
		self.scale_along_z = 0

	def addGameObject(self,**kwargs): 
		obj = sdk.EmbeddedInstanceDesc(**kwargs)
		obj.GAME = self.GAME 
		obj.PARENT = self 
		self.embedded_instances.append(obj)
		return obj 

sdk.CollectionDesc = CollectionDesc 
################################################################################################################################################
class CameraDesc(sdk.CameraDesc) : 
	__mule__ = True
	__ext__ = ".camera"
	def on_field_changed(self,name = None, value = None) : 
		if self.PARENT is not None : 
			self.PARENT.data = MessageToString(self.to_proto(),as_one_line = False)
sdk.CameraDesc = CameraDesc 
################################################################################################################################################






################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
__all__ = ['sdk']
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
























































































'''
local_files = {
    os.path.basename(file).removesuffix(".py")
    for file in glob.glob(os.path.join(os.path.dirname(__file__),'*.py'))
    if not os.path.basename(file) in {'__init__.py','naitivesdk.py'}
    }


for local_file in local_files : 
    dirname = os.path.dirname(__file__)
    #sub_module = importlib.import_module(f'.{local_file}', package = 'DefoldSdk.Sdk')
    exec(f'import DefoldSdk.Sdk.{local_file} as {local_file} ')
    sub_module = globals().get(local_file)
    print(sub_module,local_file)
    for cls_name in dir(sub_module) :
        cls = getattr(sub_module,cls_name)
        if hasattr(cls,'__mule__') : 
            if getattr(cls , '__mule__') == True  : 
                print(f"Dispatched {cls}")
                setattr(sdk,cls_name,cls)




__all__ = ['sdk']
'''