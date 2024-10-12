import requests
from typing import Optional, Dict, Any

class DabarqusSDK:
    def __init__(self, base_url: str = "http://localhost:6568"):
        self.base_url = base_url.rstrip('/')

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, params=params, json=data)
        response.raise_for_status()
        return response.json()

    # Health and Admin
    def check_health(self) -> Dict[str, Any]:
        return self._request("GET", "/health")

    # Models and Downloads
    def get_models(self) -> Dict[str, Any]:
        return self._request("GET", "/api/models")

    def get_model_metadata(self, model_repo: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        params = {"modelRepo": model_repo, "filePath": file_path}
        return self._request("GET", "/api/model/metadata", params=params)

    def get_downloads(self, model_repo: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
        params = {"modelRepo": model_repo, "filePath": file_path}
        return self._request("GET", "/api/downloads", params=params)

    def enqueue_download(self, model_repo: str, file_path: str) -> Dict[str, Any]:
        params = {"modelRepo": model_repo, "filePath": file_path}
        return self._request("GET", "/api/downloads/enqueue", params=params)

    def cancel_download(self, model_repo: str, file_path: str) -> Dict[str, Any]:
        params = {"modelRepo": model_repo, "filePath": file_path}
        return self._request("GET", "/api/downloads/cancel", params=params)

    def remove_download(self, model_repo: str, file_path: str) -> Dict[str, Any]:
        params = {"modelRepo": model_repo, "filePath": file_path}
        return self._request("GET", "/api/downloads/remove", params=params)

    # Inference
    def get_inference_info(self, alias: Optional[str] = None) -> Dict[str, Any]:
        params = {"alias": alias} if alias else None
        return self._request("GET", "/api/inference", params=params)

    def start_inference(self, alias: str, model_repo: str, file_path: str, address: Optional[str] = None,
                        port: Optional[int] = None, context_size: Optional[int] = None,
                        gpu_layers: Optional[int] = None, chat_template: Optional[str] = None) -> Dict[str, Any]:
        params = {
            "alias": alias, "modelRepo": model_repo, "filePath": file_path,
            "address": address, "port": port, "contextSize": context_size,
            "gpuLayers": gpu_layers, "chatTemplate": chat_template
        }
        return self._request("GET", "/api/inference/start", params=params)

    def stop_inference(self, alias: str) -> Dict[str, Any]:
        return self._request("GET", "/api/inference/stop", params={"alias": alias})

    def get_inference_status(self, alias: Optional[str] = None) -> Dict[str, Any]:
        params = {"alias": alias} if alias else None
        return self._request("GET", "/api/inference/status", params=params)

    def reset_inference(self, alias: str) -> Dict[str, Any]:
        return self._request("GET", "/api/inference/reset", params={"alias": alias})

    def restart_inference(self) -> Dict[str, Any]:
        return self._request("GET", "/api/inference/restart")

    # Hardware
    def get_hardware_info(self) -> Dict[str, Any]:
        return self._request("GET", "/api/hardware")

    # Silk (Memory) Operations
    def get_memory_status(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk")

    def enable_memories(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/enable")

    def disable_memories(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/disable")

    def get_memory_banks(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/memorybanks")

    def activate_memory_bank(self, bank: str) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/memorybank/activate", params={"bank": bank})

    def deactivate_memory_bank(self, bank: str) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/memorybank/deactivate", params={"bank": bank})

    def query_semantic_search(self, query: str, limit: Optional[int] = None, memory_bank: Optional[str] = None) -> Dict[str, Any]:
        params = {"q": query, "limit": limit, "bank": memory_bank}
        return self._request("GET", "/api/silk/query", params=params)

    def check_silk_health(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/health")

    def get_silk_model_metadata(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/model/metadata")

    def check_silk_store_health(self) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/store/health")

    def enqueue_ingestion(self, memory_bank_name: str, input_path: str, chunk_size: Optional[int] = None,
                          chunk_overlap: Optional[int] = None, chunk_boundary: Optional[str] = None,
                          embedding_model: Optional[str] = None, overwrite: Optional[bool] = None,
                          tree_size: Optional[int] = None, embedding_port: Optional[int] = None) -> Dict[str, Any]:
        params = {
            "memoryBankName": memory_bank_name, "inputPath": input_path,
            "chunkSize": chunk_size, "chunkOverlap": chunk_overlap,
            "chunkBoundary": chunk_boundary, "embeddingModel": embedding_model,
            "overwrite": overwrite, "treeSize": tree_size, "embeddingPort": embedding_port
        }
        return self._request("GET", "/api/silk/store/enqueue", params=params)

    def cancel_ingestion(self, bank: str) -> Dict[str, Any]:
        return self._request("GET", "/api/silk/ingestions/cancel", params={"bank": bank})

    def get_ingestions(self, bank: Optional[str] = None) -> Dict[str, Any]:
        params = {"bank": bank} if bank else None
        return self._request("GET", "/api/silk/ingestions", params=params)

    # Shutdown
    def shutdown_server(self) -> Dict[str, Any]:
        return self._request("GET", "/api/shutdown")

    # Logging
    def write_to_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "/api/utils/log", data=log_data)

    # Embedding
    def get_embedding(self, input_text: str) -> Dict[str, Any]:
        return self._request("POST", "/api/silk/embedding", data={"input": input_text})

    # Enqueue ingestion (POST method)
    def enqueue_ingestion_post(self, memory_bank_name: str, input_path: str, chunk_size: Optional[int] = None,
                               chunk_overlap: Optional[int] = None, chunk_boundary: Optional[str] = None,
                               embedding_model: Optional[str] = None, overwrite: Optional[bool] = None,
                               tree_size: Optional[int] = None, embedding_port: Optional[int] = None) -> Dict[str, Any]:
        data = {
            "memoryBankName": memory_bank_name, "inputPath": input_path,
            "chunkSize": chunk_size, "chunkOverlap": chunk_overlap,
            "chunkBoundary": chunk_boundary, "embeddingModel": embedding_model,
            "overwrite": overwrite, "treeSize": tree_size, "embeddingPort": embedding_port
        }
        return self._request("POST", "/api/silk/store/enqueue", data=data)