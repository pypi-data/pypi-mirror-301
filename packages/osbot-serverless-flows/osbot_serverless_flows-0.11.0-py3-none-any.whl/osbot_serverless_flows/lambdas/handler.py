from fastapi                                import FastAPI
from mangum                                 import Mangum

from osbot_serverless_flows.fast_api.Fast_API__Serverless_Flows import Fast_API__Serverless_Flows
from osbot_serverless_flows.utils.Version   import version__osbot_serverless_flows

# app = FastAPI()
#
# @app.get("/")
# def root():
#     return {"message": "Hello World!"}
#
# @app.get("/ping")
# def ping():
#     return {"pong": "42"}
#
# @app.get("/version")
# def version():
#     return version__osbot_serverless_flows


serverless_flows = Fast_API__Serverless_Flows().setup()
app              = serverless_flows.app()
run              = Mangum(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)