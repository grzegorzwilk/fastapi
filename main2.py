from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import subprocess as sub 
import os
import tempfile
import platform
import uuid



DARWIN  = 0
WINDOWS = 1
LINUX   = 2
def whatPlatform():
    if platform.system() == "Darwin":
        return DARWIN
    if platform.system() == "Windows":
        return WINDOWS
    if platform.system() == "Linux":
        return LINUX


def converter_path():
    lp=os.path.dirname(__file__)
    if whatPlatform()==WINDOWS:
        path=os.path.join(lp,'WIN','LP_XMLConverter.exe')    
    if whatPlatform()==LINUX:
        lp=os.path.dirname(lp)
        path=os.path.join(lp,'LP','LP_XMLConverter.exe')    
    
    if whatPlatform()==DARWIN:
        path=os.path.join(lp,'OSX','MakeGDLLib_X86','LP_XMLConverter.app','Contents','MacOS','LP_XMLConverter')
    return path 


#dest temp folder
lp=os.path.dirname(__file__)
folder_up=os.path.dirname(lp)
TMP_FOLDER = os.path.join(lp, 'TMP')
GSM_FOLDER = os.path.join(lp, 'GSM')
if whatPlatform()==LINUX:
    TMP_FOLDER = os.path.join(folder_up, 'TMP')
    GSM_FOLDER = os.path.join(folder_up, 'GSM')
# Create folders if they don't exist
os.makedirs(TMP_FOLDER, exist_ok=True)
os.makedirs(GSM_FOLDER, exist_ok=True)


CONVERTER_PATH = converter_path()




app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

# items = []


@app.get("/lpx")
def run_lpx():
    _command = [CONVERTER_PATH]
    if whatPlatform()==LINUX:_command.insert(0,'wine')
    out = sub.check_output(_command)
    return {"result": out}
@app.get("/help")
def run_lpx_help():
    _command = [CONVERTER_PATH,'help']
    if whatPlatform()==LINUX:_command.insert(0,'wine')
    out = sub.check_output(_command)
    return {"result": out}


@app.post("/xml2lp")
async def xml2lp(
    dest: str = None,
    source_file: UploadFile = File(None),
    source: str = None,
    lang: str = None, 
    img: str = None, 
    toplatform: str = None, 
    def_file: str = None, 
    cur: str = None,
    keepimagepath: bool = False, 
    excludesvg: bool = False,
    copyright_author: str = None, 
    copyright_type: str = None,
    copyright_version: str = None, 
    password: str = None
):
    """
    Convert XML file to library part using xml2libpart command.
    Required: either source_file (upload) or source (file path).
    Optional: dest file path (if not provided, temporary file will be created),
              lang, img, toplatform, def_file, cur, keepimagepath, excludesvg,
              copyright_author, copyright_type, copyright_version, password
    """
    # Handle file upload
    temp_source = None
    if source_file:
        # Save uploaded file to TMP folder
        filename = f"{uuid.uuid4()}.xml"
        filepath = os.path.join(TMP_FOLDER, filename)
        with open(filepath, 'wb') as f:
            content = await source_file.read()
            f.write(content)
        temp_source = filepath
        actual_source = temp_source
    elif source:
        actual_source = source
    else:
        return {"error": "Either source_file or source parameter is required"}
    
    # Create temporary destination file if not provided
    temp_dest = None
    if dest:
        # Save destination file to GSM folder
        actual_dest = os.path.join(GSM_FOLDER, dest)
    else:
        # Generate unique filename in GSM folder
        filename = f"{uuid.uuid4()}.gsm"
        actual_dest = os.path.join(GSM_FOLDER, filename)
        temp_dest = actual_dest
    
    # lp=os.path.dirname(__file__)
    # lp=os.path.dirname(lp)
    # path=os.path.join(lp,'LP','LP_XMLConverter.exe')
    

    command = [CONVERTER_PATH, 'xml2libpart']
    if whatPlatform()==LINUX: command.insert(0,'wine')
    if lang:
        command.extend(['-l', lang])
    if img:
        command.extend(['-img', img])
    if toplatform:
        command.extend(['-toplatform', toplatform])
    if def_file:
        command.extend(['-def', def_file])
        if cur:
            command.extend(['-cur', cur])
            if keepimagepath:
                command.append('-keepimagepath')
    if excludesvg:
        command.append('-excludesvg')
    if copyright_author and copyright_type and copyright_version:
        command.extend(['-setcopyright', copyright_author, copyright_type, copyright_version])
    if password:
        command.extend(['-password', password])
    
    command.extend([actual_source, actual_dest])
    
    try:
        out = sub.check_output(command)
        result = {
            "result": out.decode('utf-8') if isinstance(out, bytes) else str(out),
            "output_file": actual_dest
        }
        return result
    finally:
        # Clean up temporary source file if it was created
        if temp_source and os.path.exists(temp_source):
            os.remove(temp_source)
