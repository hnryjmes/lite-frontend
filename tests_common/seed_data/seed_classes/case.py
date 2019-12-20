from .seed_class import SeedClass
from ..make_requests import make_request


class Case(SeedClass):
    def assign_case_to_queue(self, case_id=None, queue_id=None):
        queue_id = self.context["queue_id"] if queue_id is None else queue_id
        case_id = self.context["case_id"] if case_id is None else case_id
        make_request(
            "PUT",
            base_url=self.base_url,
            url="/cases/" + case_id + "/",
            headers=self.gov_headers,
            body={"queues": [queue_id]},
        )

    def assign_test_cases_to_bin(self, bin_queue_id, new_cases_queue_id):
        cases = make_request(
            "GET", base_url=self.base_url, url="/queues/" + new_cases_queue_id + "/", headers=self.gov_headers,
        ).json()["queue"]["cases"]
        for case in cases:
            make_request(
                "PUT",
                base_url=self.base_url,
                url="/cases/" + case["id"] + "/",
                headers=self.gov_headers,
                body={"queues": [bin_queue_id]},
            )

    def add_case_note(self, context, case_id):
        data = self.request_data["case_note"]
        context.case_note_text = self.request_data["case_note"]["text"]
        make_request(
            "POST",
            base_url=self.base_url,
            url="/cases/" + case_id + "/case-notes/",
            headers=self.gov_headers,
            body=data,
        )

    def edit_case(self, app_id):
        data = self.request_data["edit_case_app"]
        self.context["edit_case_app"] = self.request_data["edit_case_app"]
        make_request(
            "PUT", base_url=self.base_url, url="/applications/" + app_id + "/", headers=self.export_headers, body=data,
        )

    def add_generated_document(self, case_id, template_id):
        generated_document = make_request(
            "POST",
            base_url=self.base_url,
            url="/cases/" + case_id + "/generated-documents/",
            headers=self.gov_headers,
            body={"template": template_id, "text": "random text"},
        ).json()["generated_document"]
        self.add_to_context("generated_document", generated_document)
