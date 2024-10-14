from pydantic import BaseModel, create_model
from fastapi import FastAPI
from jarvislabs import App
from typing import Callable, Any
import uvicorn
import inspect
import asyncio

class Server:
    def __init__(self, app: App):
        self.app = app
        self.fastapi_app = FastAPI()
        self._setup()
        self._setup_routes()

    def _setup(self):
        if self.app.setup_fn:
            self.app.setup_fn()

    def _setup_routes(self):
        for name, method in self.app.api_endpoints.items():
            print(f"Route name {name}")
            self._create_route(method)

    def _create_route(self, method: Callable):
        method_name = method.__name__
        signature = inspect.signature(method)
        parameters = signature.parameters

        # Get the first non-self parameter, which should be the Pydantic BaseModel
        model_param = next((param for name, param in parameters.items() if name != 'self'), None)
        
        if model_param is None or not issubclass(model_param.annotation, BaseModel):
            raise ValueError(f"Method {method_name} must have a Pydantic BaseModel parameter")

        BodyModel = model_param.annotation
        
        # Create a new model with the original BodyModel fields and prediction_id
        import uuid

        # Create a new model with the original BodyModel fields and optional prediction_id
        ExtendedBodyModel = create_model(
            f'Extended{BodyModel.__name__}',
            prediction_id=(str, None),
            **{field: (field_info.annotation, field_info.default) for field, field_info in BodyModel.__fields__.items()}
        )

        @self.fastapi_app.post(f"/{method_name}")
        async def endpoint(body: ExtendedBodyModel):
            # Generate a random prediction_id if not provided
            if body.prediction_id is None:
                body.prediction_id = str(uuid.uuid4())

            # Extract the original BodyModel fields
            original_body = BodyModel(**{k: v for k, v in body.dict().items() if k in BodyModel.__fields__})
            result = await self.app.api_endpoints[method_name](original_body)
            return {"prediction_id": body.prediction_id, "result": result}

        ExtendedBodyModel = create_model(
            f'Extended{BodyModel.__name__}',
            prediction_id=(str, None),
            **{field: (field_info.annotation, field_info.default) for field, field_info in BodyModel.__fields__.items()}
        )

        @self.fastapi_app.post(f"/{method_name}")
        async def endpoint(body: ExtendedBodyModel):
            if body.prediction_id is None:
                body.prediction_id = str(uuid.uuid4())
            # Extract the original BodyModel fields
            original_body = BodyModel(**{k: v for k, v in body.dict().items() if k in BodyModel.__fields__})
            result = await self.app.api_endpoints[method_name](original_body)
            return {"prediction_id": body.prediction_id, "result": result}

    def run(self, host: str = "0.0.0.0", port: int = 6006):
        @self.fastapi_app.get("/health")
        async def health():
            return {"success": True}
        uvicorn.run(self.fastapi_app, host=host, port=port)