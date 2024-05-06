class Helpers:
    """Class containing helper functions for capra_webapp"""

    @staticmethod
    def handle_upload_file(f):
        """Handles uploading files"""
        with open("capra_webapp/uploads/name.json", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
