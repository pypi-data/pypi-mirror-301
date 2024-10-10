import requests
from time import sleep
from typing import Optional, Dict

from tonic_textual.classes.common_api_responses.label_custom_list import LabelCustomList
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.tonic_exception import FileNotReadyForDownload

class DatasetFile:
    """
    Class to store the metadata for a dataset file.

    Parameters
    ----------
    id : str
        The identifier of the dataset file.

    name: str
        The file name of the dataset file.

    num_rows : long
        The number of rows in the dataset file.

    num_columns: int
        The number of columns in the dataset file.

    processing_status: string
        The status of the dataset file in the processing pipeline. Possible values are
        'Completed', 'Failed', 'Cancelled', 'Running', and 'Queued'.

    processing_error: string
        If the dataset file processing failed, a description of the issue that caused
        the failure.

    label_allow_lists: Dict[str, LabelCustomList]
        A dictionary of custom entity detection regex for the dataset file. The keys are the pii type to be detected,
        and the values are LabelCustomList objects, whose regexes should be recognized as said pii type.
    """

    def __init__(
        self,
        client: HttpClient,
        id: str,
        dataset_id: str,
        name: str,
        num_rows: Optional[int],
        num_columns: int,
        processing_status: str,
        processing_error: Optional[str],
        label_allow_lists: Optional[Dict[str, LabelCustomList]] = None
    ):
        self.client = client
        self.id = id
        self.dataset_id = dataset_id
        self.name = name
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.processing_status = processing_status
        self.processing_error = processing_error
        self.label_allow_lists = label_allow_lists

    def describe(self) -> str:
        """Returns the dataset file metadata as string. Includes the identifier, file
        name, number of rows, and number of columns."""
        description = f"File: {self.name} [{self.id}]\n"
        description += f"Number of rows: {self.num_rows}\n"
        description += f"Number of columns: {self.num_columns}\n"
        description += f"Status: {self.processing_status}\n"
        if self.processing_status != "" and self.processing_error is not None:
            description += f"Error: {self.processing_error}\n"
        return description

    def download(
        self,
        random_seed: Optional[int] = None,
        num_retries: int = 6,
    ) -> bytes:
        """
        Download a redacted file

        Parameters
        --------
        random_seed: Optional[int] = None
            An optional value to use to override Textual's default random number
            seeding. Can be used to ensure that different API calls use the same or
            different random seeds.

        num_retries: int = 6
            An optional value to specify how many times to attempt to download the
            file.  If a file is not yet ready for download, there will be a 10 second
            pause before retrying. (The default value is 6)

        Returns
        -------
        bytes
            The redacted file as byte array
        """
        retries = 1
        while retries <= num_retries:
            try:
                if random_seed is not None:
                    additional_headers = {"textual-random-seed": str(random_seed)}
                else:
                    additional_headers = {}
                with requests.Session() as session:
                    return self.client.http_get_file(
                        f"/api/dataset/{self.dataset_id}/files/{self.id}/download",
                        additional_headers=additional_headers,
                        session=session
                    )

            except FileNotReadyForDownload:
                retries = retries + 1
                if retries <= num_retries:
                    sleep(10)

        retryWord = "retry" if num_retries == 1 else "retries"
        raise FileNotReadyForDownload(
            f"After {num_retries} {retryWord} the file is not yet ready for download. "
            "This is likely due to a high service load. Please try again later."
        )