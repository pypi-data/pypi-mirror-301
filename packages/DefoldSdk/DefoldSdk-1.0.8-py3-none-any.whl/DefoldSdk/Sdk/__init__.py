import sys , os 
from DefoldSdk.Naitivesdk import sdk 
import importlib , glob 


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