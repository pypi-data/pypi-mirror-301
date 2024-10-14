import multiprocessing
from multiprocessing import Process, Queue
from pydantic import BaseModel, create_model
from fastapi import FastAPI, BackgroundTasks
from jarvislabs import App
from typing import Callable, Any
import uvicorn
import inspect
import asyncio
import json
import os
import uuid

class Server:
    def __init__(self, app: App):
        self.app = app
        self.fastapi_app = FastAPI()
        self.task_queue = Queue()
        self.worker_process = None
        self._setup()
        self._setup_routes()

    def _setup(self):
        if self.app.setup_fn:
            self.app.setup_fn()

    def _setup_routes(self):
        for name, method in self.app.api_endpoints.items():
            print(f"Route name {name}")
            self._create_route(method)
            self._create_get_route(name)

    def _create_route(self, method: Callable):
        method_name = method.__name__
        signature = inspect.signature(method)
        parameters = signature.parameters

        model_param = next((param for name, param in parameters.items() if name != 'self'), None)
        
        if model_param is None or not issubclass(model_param.annotation, BaseModel):
            raise ValueError(f"Method {method_name} must have a Pydantic BaseModel parameter")

        BodyModel = model_param.annotation
        
        ExtendedBodyModel = create_model(
            f'Extended{BodyModel.__name__}',
            prediction_id=(str, None),
            **{field: (field_info.annotation, field_info.default) for field, field_info in BodyModel.__fields__.items()}
        )

        @self.fastapi_app.post(f"/{method_name}")
        async def endpoint(body: ExtendedBodyModel):
            if body.prediction_id is None:
                body.prediction_id = str(uuid.uuid4())

            original_body = BodyModel(**{k: v for k, v in body.dict().items() if k in BodyModel.__fields__})
            
            self.task_queue.put((method_name, original_body, body.prediction_id))
            
            return {"prediction_id": body.prediction_id, "status": "Processing"}

    def _create_get_route(self, method_name: str):
        @self.fastapi_app.get(f"/{method_name}/{{prediction_id}}")
        async def get_prediction(prediction_id: str):
            print(prediction_id)
            file_path = os.path.join("/home/predictions", f"{prediction_id}.json")
            if not os.path.exists(file_path):
                print("pending")
                return {"status": "Pending"}
            
            with open(file_path, "r") as f:
                result = json.load(f)
            print("completed")
            return result

    @staticmethod
    def save_response(response: dict):
        prediction_id = response["prediction_id"]
        output_dir = "/home/predictions"
        
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, f"{prediction_id}.json")
        
        with open(file_path, "w") as f:
            json.dump(response["result"], f, indent=2)
        
        print(f"Response saved to {file_path}")

    @staticmethod
    def worker_process_func(app: App, task_queue: Queue):
        while True:
            method_name, body, prediction_id = task_queue.get()
            try:
                result = asyncio.run(app.api_endpoints[method_name](body))
                Server.save_response({"prediction_id": prediction_id, "result": result})
            except Exception as e:
                error_message = f"Error processing request: {str(e)}"
                Server.save_response({"prediction_id": prediction_id, "error": error_message})

    def run(self, host: str = "0.0.0.0", port: int = 6006):
        @self.fastapi_app.get("/health")
        async def health():
            return {"success": True}

        self.worker_process = Process(target=self.worker_process_func, args=(self.app, self.task_queue))
        self.worker_process.start()

        try:
            uvicorn.run(self.fastapi_app, host=host, port=port, workers=1)
        finally:
            if self.worker_process:
                self.worker_process.terminate()
                self.worker_process.join()