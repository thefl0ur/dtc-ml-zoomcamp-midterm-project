import os
import xgboost as xgb
import numpy as np

from pathlib import Path

from litestar import Litestar, Request, post
from litestar.di import Provide


MODEL_NAME = os.getenv("MODEL_PATH", "model.json")


async def on_startup(app: Litestar) -> None:
    if not Path(MODEL_NAME).exists():
        raise RuntimeError("Environment variable MODEL_PATH is required but missing.")

    model = xgb.XGBClassifier()
    model.load_model(MODEL_NAME)
    app.state.model = model


async def provide_model(request: Request) -> xgb.XGBClassifier:
    return request.app.state.model


@post("/predict")
async def predict(data: dict, booster: xgb.XGBClassifier) -> dict:
    prediction = booster.predict_proba(np.array([list(data.values())], dtype=float))[0][1]
    return { "prediction": round(float(prediction), 2) }


def create_app() -> Litestar:
    app = Litestar(
        on_startup=[on_startup],
        dependencies={
            "booster": Provide(provide_model),
        },
        openapi_config=None,
        route_handlers=[predict]
    )

    return app