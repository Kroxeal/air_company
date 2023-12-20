import os
import io
import uuid
import csv
import openpyxl
import json
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import APIRouter, UploadFile, File, Request
from starlette.templating import Jinja2Templates

from src.services.logic.logic_flight_statistics import is_valid_json
from src.services.statistics.flight_statisctic_db import get_all_flight_statistics, \
    import_json_flight, export_json_flights

router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get('/download-flights-csv', name='download_flights_csv')
async def download_flights_csv():
    try:
        result = await get_all_flight_statistics()

        csv_data = io.StringIO()
        csv_writer = csv.DictWriter(csv_data, fieldnames=result[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(result)

        response = StreamingResponse(
            iter([csv_data.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=flights.csv"
            }
        )

        return response
    except Exception as e:
        error_message = f'Error exporting flights: {e}'
        print(error_message)
        return JSONResponse(content={"error": error_message}, status_code=500)


@router.post('/upload_file', name='upload_json_file')
async def upload_json_file(uploaded_file: UploadFile = File(...)):
    try:
        content = await uploaded_file.read()
        content_str = content.decode('utf-8')

        if not is_valid_json(content_str):
            return JSONResponse(content={"error": "Неверный формат JSON файла"}, status_code=400)

        json_data = json.loads(content_str)

        await import_json_flight(json_data)

        return JSONResponse(content={"message": "Файл успешно загружен и обработан"}, status_code=200)
    except Exception as e:
        print(f"Ошибка загрузки и обработки файла: {e}")
        return JSONResponse(content={"error": "Произошла ошибка при обработке файла"}, status_code=500)


@router.get('/export_json_flight', name='export_json_flight')
async def export_json_flight():
    data = await export_json_flights()
    json_data = json.dumps(data, indent=2, default=str)
    headers = {
        "Content-Disposition": "attachment; filename=flights_export.json",
        "Content-Type": "application/json",
    }

    return StreamingResponse(iter([json_data]), headers=headers)


@router.get('/form/csv', name='csv_form')
async def get_csv_form(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('statistics/download_flights_csv.html', context=context)


@router.get('/form/json', name='json_form')
async def get_json_form(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('statistics/json_operations.html', context=context)
