import base64
from fastapi import APIRouter, File, Form, UploadFile
from app.domain.model.Incident import IncidentResource
from app.domain.IncidentServices import IncidentsService

router = APIRouter()
service = IncidentsService()


@router.post("/api/v1/incidents")
async def create_incident(
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    images: list[UploadFile] = File(...)
):
    try:
        images_base64 = []
        for image in images:
            image_bytes = await image.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            images_base64.append(image_base64)
            
        data = IncidentResource(
            title=title,
            description=description,
            status=status,
            images=images_base64
        )
        return service.save_data(data)
    except Exception as e:
        return {"error": str(e)}


@router.delete("/incidents/{key}")
def delete_incident(key: str):
    try:
        return service.delete_data(key)
    except Exception as e:
        return {"error": str(e)}


@router.put("/incidents/{key}")
def update_incident(key: str, data: IncidentResource):
    try:
        return service.update_data(key, data)
    except Exception as e:
        return {"error in put": str(e)}


@router.get("/incidents/{key}")
def read_incident(key: str):
    try:
        return service.get_data(key)
    except Exception as e:
        return {"error": str(e)}


@router.get("/incidents/")
def read_all_incidents():
    try:
        return service.get_all_data()
    except Exception as e:
        return {"error": str(e)}
