from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

from osbot_serverless_flows.utils.Version import version__osbot_serverless_flows


class Routes__Info(Fast_API_Routes):
    tag : str = 'info'

    def ping(self):
        return {"pong": "42"}

    def version(self):
        return { "version" : version__osbot_serverless_flows}

    def setup_routes(self):
        self.add_route_get(self.ping   )
        self.add_route_get(self.version)
        return self