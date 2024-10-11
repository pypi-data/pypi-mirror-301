import sys , os 
from DefoldSdk.naitivesdk import SdkDefold as sdk 
import importlib , glob 
sdk.CreateSdk()

local_files = {
    os.path.basename(file).removesuffix(".py")
    for file in glob.glob(os.path.join(os.path.dirname(__file__),'*.py'))
    if not os.path.basename(file) in {'__init__.py','naitivesdk.py'}
    }

for local_file in local_files : 
    sub_module = importlib.import_module(f'.{local_file}', package = 'DefoldSdk.Sdk')
    for cls_name in dir(sub_module) :
        cls = getattr(sub_module,cls_name)
        if hasattr(cls,'__mule__') : 
            if getattr(cls , '__mule__') == True  : 
                setattr(sdk,cls_name,cls)


