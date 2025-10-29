from pathlib import Path
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse


app = FastAPI(title="Simple Upload API")


@app.get("/", response_class=HTMLResponse)
def index_page() -> str:
    return (
        """
        <html>
          <head><title>Upload</title></head>
          <body>
            <h1>Upload pliku</h1>
            <form action="/upload" enctype="multipart/form-data" method="post">
              <input name="file" type="file" />
              <button type="submit">Wyślij</button>
            </form>
          </body>
        </html>
        """
    )


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    destination_path = uploads_dir / file.filename

    # Zapis w kawałkach, aby nie trzymać całego pliku w pamięci
    with destination_path.open("wb") as destination:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            destination.write(chunk)

    return {
        "filename": file.filename,
        "saved_to": str(destination_path.resolve()),
        "size_bytes": destination_path.stat().st_size,
        "content_type": file.content_type,
    }


