from fastapi import UploadFile, File


async def save_file(uploaded_file: UploadFile = File(...)):
    print('saving')
    contents = uploaded_file.file.read()
    with open(f"D:/Project_air_company/src/static/images/{uploaded_file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": uploaded_file.filename}
