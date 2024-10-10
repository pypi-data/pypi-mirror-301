import io
from osbot_fast_api.api.Fast_API_Routes                                     import Fast_API_Routes
from starlette.responses                                                    import StreamingResponse
from osbot_serverless_flows.flows.gsuite.Flow__GSuite__Create_Presentation  import Flow__GSuite__Create_Presentation

ROUTES__EXPECTED_PATHS__GSUITE = ['/gsuite/presentation-create']

class Routes__GSuite(Fast_API_Routes):
    tag : str = 'gsuite'

    def presentation_create(self,  return_file:bool=False):           # todo: refactor with url_screenshot
        with Flow__GSuite__Create_Presentation() as _:
            run_data   =_.run()
            pdf_bytes  = _.pdf_bytes
            pdf_base64 = _.pdf_base_64

            if return_file is True:
                pdf_stream = io.BytesIO(pdf_bytes)
                response = StreamingResponse( pdf_stream,
                                              media_type = "application/pdf",
                                              headers    = {"Content-Disposition": "attachment; filename=document.pdf"})
            else:
                response = {'pdf_base64': pdf_base64}

            return response

    def setup_routes(self):
        self.add_route_get(self.presentation_create )
