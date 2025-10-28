from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import subprocess as sub 
import os
import tempfile
import platform

lp=os.path.dirname(__file__)
def isWindows():
    if platform.system() == "Windows":
        return True
    if platform.system() == "Darwin":
        return False
def converter_path():
    lp=os.path.dirname(__file__)
    if isWindows():
        path=os.path.join(lp,'WIN','LP_XMLConverter.exe')    
    else:
        path=os.path.join(lp,'OSX','MakeGDLLib_X86','LP_XMLConverter.app','Contents','MacOS','LP_XMLConverter')
    return path 

CONVERTER_PATH = converter_path()




app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}

# items = []


@app.get("/lpx")
def run_lpx():
    out = sub.check_output([CONVERTER_PATH])
    return {"result": out}
@app.get("/help")
def run_lpx_help():
    out = sub.check_output([CONVERTER_PATH,'help'])
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
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as tmp_file:
            content = await source_file.read()
            tmp_file.write(content)
            temp_source = tmp_file.name
        actual_source = temp_source
    elif source:
        actual_source = source
    else:
        return {"error": "Either source_file or source parameter is required"}
    
    # Create temporary destination file if not provided
    temp_dest = None
    if dest:
        actual_dest = dest
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gsm') as tmp_dest:
            actual_dest = tmp_dest.name
        temp_dest = actual_dest
    
    # lp=os.path.dirname(__file__)
    # lp=os.path.dirname(lp)
    # path=os.path.join(lp,'LP','LP_XMLConverter.exe')
    
    command = [CONVERTER_PATH, 'xml2libpart']
    
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
