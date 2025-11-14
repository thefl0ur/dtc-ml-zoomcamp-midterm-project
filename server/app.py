import os
from litestar import Litestar, Request, post
from litestar.di import Provide
import xgboost as xgb

async def on_startup(app: Litestar) -> None:
    model = xgb.XGBClassifier()
    model.load_model(os.environ["MODEL_NAME"])
    app.state.model = model


async def provide_model(request: Request) -> xgb.XGBClassifier:
    return request.app.state.model


@post("/predict")
async def predict(data: dict, booster: xgb.XGBClassifier) -> dict[str, str]:
    return booster.predict(data)


def create_app() -> Litestar:
    app = Litestar(
        on_startup=[on_startup],
        dependencies={
            "rpc_client": Provide(provide_model),
        },
        openapi_config=None,
    )

    return app