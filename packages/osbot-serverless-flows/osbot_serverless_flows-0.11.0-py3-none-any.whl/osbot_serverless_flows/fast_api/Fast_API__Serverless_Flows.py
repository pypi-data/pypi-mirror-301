from osbot_fast_api.api.Fast_API                            import Fast_API
from osbot_prefect.flows.Flow_Events__To__Prefect_Server import Flow_Events__To__Prefect_Server
from osbot_serverless_flows.fast_api.routes.Routes__Debug   import Routes__Debug
from osbot_serverless_flows.fast_api.routes.Routes__GSuite import Routes__GSuite
from osbot_serverless_flows.fast_api.routes.Routes__Info    import Routes__Info
from osbot_serverless_flows.fast_api.routes.Routes__Browser import Routes__Browser
from osbot_utils.decorators.methods.cache_on_self           import cache_on_self


class Fast_API__Serverless_Flows(Fast_API):
    prefect_enabled : bool = False

    def setup(self):
        self.setup__prefect_cloud()
        super().setup()
        return self

    @cache_on_self
    def flow_events_to_prefect_server(self):
        return Flow_Events__To__Prefect_Server()

    def setup__prefect_cloud(self):
        with self.flow_events_to_prefect_server()  as _:
            if _.prefect_cloud_api.prefect_rest_api.prefect_is_server_online():
                _.add_event_listener()
                self.prefect_enabled = True



    def setup_routes(self):
        self.add_routes(Routes__Info   )
        self.add_routes(Routes__Debug  )
        self.add_routes(Routes__Browser)
        self.add_routes(Routes__GSuite )



    # todo: BUG: chrome is not being picked up from the install folder from the docker image
    #       the code below on start up was not consistently installing ok chrome (in some cases the processes would not unzip all the files, I think this is because of the LWA and Lambdas boot timeout)
    # def ensure_browser_is_installed(self):
    #     from osbot_serverless_flows.playwright.Playwright__Serverless import Playwright__Serverless
    #     playwright_browser = Playwright__Serverless()
    #     result = playwright_browser.browser__install()
    #     print(f"*****************************************")
    #     print(f"*****    Chrome installed:  { result }    *****")
    #     print(f"*****************************************")