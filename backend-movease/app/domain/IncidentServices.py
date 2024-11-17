import logging
from datetime import datetime
import json
from app.core.infrastructure.redis_client import get_redis_client
from app.domain.model.Incident import Incident, IncidentResource


class IncidentsService:
    def __init__(self):
        self.client = get_redis_client()
        self.incident_counter_key = "incidents_counter"
    
    def save_data(self, data: IncidentResource):
        with self.client.pipeline() as pipe:
            incident_id = pipe.incr(self.incident_counter_key).execute()[0]
            incident_to_save = Incident(
                id=incident_id,
                title=data.title,
                description=data.description,
                status=data.status,
                images=data.images,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
            )
            serialized_data = json.dumps(incident_to_save.__dict__)
            try:
                pipe.json().set(f"incidents:{incident_id}", "$" , serialized_data).execute()
                return incident_to_save
            except Exception as e:
                self.client.decr(self.incident_counter_key)
                return {"error in IncidentsService": str(e)}

    def delete_data(self, incident_id: int):
        try:
            key = f"incidents:{incident_id}"
            result = self.client.delete(key)
            if result == 1:
                return {"message": f"Incident with ID {incident_id} deleted"}
            return {"message": "Incident not found"}
        except Exception as e:
            return {"error": str(e)}

    def update_data(self, key: str, data: IncidentResource):
        saved_incident_json = self.get_data(key)
        if not saved_incident_json:
            return {"error": "Incident not found"}
        try:
            self.client.json().set(f"incidents:{key}", "$.title", data.title)
            self.client.json().set(f"incidents:{key}", "$.description", data.description)
            self.client.json().set(f"incidents:{key}", "$.status", data.status)
            self.client.json().set(f"incidents:{key}", "$.images", data.images)
            self.client.json().set(f"incidents:{key}", "$.updated_at", datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
            return {
                "message": f"Incident with ID {key} updated",
                "data": Incident(
                    id=int(key),
                    title=data.title,
                    description=data.description,
                    status=data.status,
                    images=data.images,
                    created_at=saved_incident_json.get("created_at"),
                    updated_at=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                ),
            }
        except Exception as e:
            return {"error in update": str(e)}

    def get_data(self, key: str):
        try:
            data = self.client.json().get(f"incidents:{key}")
            return data
        except Exception as e:
            return {"error": str(e)}
    def get_all_data(self):
        try:
            keys = []
            number_of_incidents = self.client.get(self.incident_counter_key)
            for i in range(1, int(number_of_incidents) + 1):
                keys.append(self.client.json().get(f"incidents:{i}"))
            converted_keys = [json.loads(key) for key in keys]
            return converted_keys
        
        except (ConnectionError, KeyError) as e:
            logging.error(f"An error occurred while fetching data: {e}")
            return {"error": str(e)}

    def _is_valid_format(self, item):
        return isinstance(item, dict) and "expected_key" in item
