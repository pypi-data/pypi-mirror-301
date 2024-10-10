from osbot_utils.utils.Files import file_create_from_bytes

from osbot_utils.utils.Misc import random_text, time_now, bytes_to_base64

from osbot_utils.helpers.flows.decorators.task import task

from osbot_gsuite.gsuite.slides.GSlides import GSlides
from osbot_utils.helpers.flows import Flow
from osbot_utils.helpers.flows.decorators.flow import flow

from osbot_utils.base_classes.Type_Safe import Type_Safe


class Flow__GSuite__Create_Presentation(Type_Safe):

    gslides         : GSlides
    presentation_id : str
    folder_id       : str = '1vrTS5zLeIb4LdklGy_8uVASlahzLQUQz'
    title           : str = random_text('Temp Presentation (via Prefect) ')
    pdf_bytes       : bytes
    pdf_base_64    : str

    @task()
    def check_access_to_gsuite(self):
        print('checking access to GSuite')
        for presentation in self.gslides.all_presentations():
           print(presentation.get('name'))

    @task()
    def create_presentation(self):
        print(f"creating presentation with title: {self.title}")
        presentation_data = self.gslides.presentation_create(title=self.title,folder_id=self.folder_id)
        self.presentation_id = presentation_data.presentation_id

    @task()
    def editing_presentation(self):
        presentation_id = self.presentation_id
        print('editing')
        presentation_info = self.gslides.presentation_metadata(presentation_id)

        text_1      = f'Presentation created at {time_now()}'
        text_2      = '... via prefect :) ...'
        object_id_1 = presentation_info.slides[0].pageElements[0].objectId
        object_id_2 = presentation_info.slides[0].pageElements[1].objectId
        self.gslides.element_set_text(presentation_id, object_id_1, text_1, delete_existing_text=False)
        self.gslides.element_set_text(presentation_id, object_id_2, text_2, delete_existing_text=False)

    @task()
    def creating_pdf_bytes(self):
        self.pdf_bytes   = self.gslides.pdf__bytes(self.presentation_id)
        self.pdf_base_64 = bytes_to_base64(self.pdf_bytes)
        print(f"created pdf with {len(self.pdf_bytes)} bytes")

    @task()
    def deleting_presentation(self):
        print('deleting', self.presentation_id)
        self.gslides.presentation_delete(self.presentation_id)

    # @task()
    # def save_pdf_locally(self):
    #     local_file = file_create_from_bytes("./test.pdf", self.pdf_bytes)
    #     print(f"saved pdf into {local_file}")

    @flow()
    def flow__create_presentation(self) -> Flow:
        self.create_presentation    ()
        self.editing_presentation   ()
        self.creating_pdf_bytes     ()
        self.deleting_presentation  ()
        return 'all done'

    def run(self):
        with self.flow__create_presentation() as _:
            _.execute_flow()
            return _.data