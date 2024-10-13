from __future__ import annotations

from pathlib import Path
from pprint import pformat

from magics.abstract import api_requestor
from magics.error import FileTypeError
from magics.filemanager import DownloadManager, UploadManager
from magics.magics_response import MagicsResponse
from magics.types import (
    FileDeleteResponse,
    FileList,
    FileObject,
    FilePurpose,
    FileResponse,
    MagicsClient,
    MagicsRequest,
)
from magics.utils import check_file, normalize_key


class Files:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    def upload(
        self,
        file: Path | str,
        *,
        purpose: FilePurpose | str = FilePurpose.FineTune,
        check: bool = True,
    ) -> FileResponse:
        upload_manager = UploadManager(self._client)

        if check:
            report_dict = check_file(file)
            if not report_dict["is_check_passed"]:
                raise FileTypeError(
                    f"Invalid file supplied, failed to upload. Report:\n{pformat(report_dict)}"
                )

        if isinstance(file, str):
            file = Path(file)

        if isinstance(purpose, str):
            purpose = FilePurpose(purpose)

        assert isinstance(purpose, FilePurpose)

        return upload_manager.upload("files", file, purpose=purpose, redirect=True)

    def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="GET",
                url="files",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileList(**response.data)

    def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="GET",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileResponse(**response.data)

    def retrieve_content(
        self, id: str, *, output: Path | str | None = None
    ) -> FileObject:
        download_manager = DownloadManager(self._client)

        if isinstance(output, str):
            output = Path(output)

        downloaded_filename, file_size = download_manager.download(
            f"files/{id}/content", output, normalize_key(f"{id}.jsonl")
        )

        return FileObject(
            object="local",
            id=id,
            filename=downloaded_filename,
            size=file_size,
        )

    def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=MagicsRequest(
                method="DELETE",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileDeleteResponse(**response.data)


class AsyncFiles:
    def __init__(self, client: MagicsClient) -> None:
        self._client = client

    async def upload(
        self, file: Path | str, *, purpose: FilePurpose | str = FilePurpose.FineTune
    ) -> None:
        raise NotImplementedError()

    async def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=MagicsRequest(
                method="GET",
                url="files",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileList(**response.data)

    async def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=MagicsRequest(
                method="GET",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileResponse(**response.data)

    async def retrieve_content(
        self, id: str, *, output: Path | str | None = None
    ) -> FileObject:
        raise NotImplementedError()

    async def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=MagicsRequest(
                method="DELETE",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, MagicsResponse)

        return FileDeleteResponse(**response.data)
