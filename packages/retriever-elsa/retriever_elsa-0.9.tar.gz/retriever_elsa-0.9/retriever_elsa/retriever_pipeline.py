import sys
import os
import requests
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import time

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)


QDRANT_SERVER_URL = "http://localhost:8100"

class SearchQuery(BaseModel):
    search_phrase: str = ''
    filter: Optional[Dict[str, Any]] = None
    top_k: int = 20

def get_user_memory(
    search_string: str,
    folders: List[str] = [],
    start_time_unix: int = 0,
    end_time_unix: int = int(time.time()),
    top_k: int = 5,
    image_present: Optional[bool] = None,
    document_present: Optional[bool] = None
) -> List[Dict[str, Any]]:
    search_query = SearchQuery(
        search_phrase=search_string,
        filter={
            "must": [
                {
                    "key": "timestamp_unix",
                    "range": {
                        "gte": start_time_unix,
                        "lte": end_time_unix
                    }
                }
            ]
        },
        top_k=top_k
    )

    # Add image and document filters if specified
    if image_present is not None:
        search_query.filter["must"].append({
            "key": "image_present",
            "match": {"value": image_present}
        })
    
    if document_present is not None:
        search_query.filter["must"].append({
            "key": "document_present",
            "match": {"value": document_present}
        })

            
    result = []
    
    for folder in folders:
        try:
            endpoint = f"{QDRANT_SERVER_URL}/search_{folder}"
            response = requests.post(endpoint, json=search_query.dict())
            response.raise_for_status()
            search_result = response.json()
            print(f"{folder.upper()} CONTEXT: ", search_result)
            if search_result:
                result.extend(search_result)
        except requests.RequestException as e:
            print(f"Error querying {folder} from Qdrant server: {e}")

    return result