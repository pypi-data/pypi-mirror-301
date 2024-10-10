from osbot_utils.utils.Misc import wait_for

from osbot_utils.helpers.flows.decorators.task import task

from osbot_utils.helpers.flows.Flow import Flow

from osbot_utils.helpers.flows.decorators.flow import flow

from osbot_utils.base_classes.Type_Safe import Type_Safe


class Flow__Http__Raw_Html(Type_Safe):

    @task()
    def check_config(self):
        print('checking config')
        self.before_http_request()
        self.during_http_request()
        self.after_http_request()

    @task()
    def before_http_request(self):
        print('before_http_request')

    @task()
    def during_http_request(self):
        wait_for(0.5)
        print('during_http_request')

    @task()
    def after_http_request(self):
        print('after_http_request')

    @flow()
    async def flow__http_raw_html(self) -> Flow:
        self.check_config       ()


    def run(self):
        with self.flow__http_raw_html() as _:
            _.execute_flow()
            return _
            #return _.data