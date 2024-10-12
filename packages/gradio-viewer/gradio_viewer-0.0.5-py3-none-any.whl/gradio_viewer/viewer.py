from __future__ import annotations

import os
import asyncio
import time
import tempfile
import shutil
import subprocess
import gradio_client.utils as client_utils
from typing import Union
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable
from gradio import processing_utils
from gradio.components.base import Component
from gradio.data_classes import FileData, ListFiles
from gradio.utils import NamedString


if TYPE_CHECKING:
    from gradio.components import Timer


async def aconvert_to_pdf(input_file: Path, temp_dir: Path) -> Union[str, None]:
    output_file = temp_dir / input_file.with_suffix(".pdf").name
    if output_file.exists() and (time.time() - os.path.getctime(input_file) < 300):
        os.remove(output_file)
    if not output_file.exists():
        subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to",
                "pdf",
                str(input_file),
                "--outdir",
                str(temp_dir),
            ]
        )
    return str(output_file)


async def aconvert_files_in_parallel(ms_files, cache, ms_formats):
    tasks = [aconvert_file(file, cache, ms_formats) for file in ms_files]
    return await asyncio.gather(*tasks)


def is_libreoffice_installed() -> bool:
    """Vérifie si LibreOffice est installé."""
    possible_executables = ["libreoffice", "soffice"]
    for executable in possible_executables:
        if shutil.which(executable):
            return True
    return False


async def aconvert_file(file, temp_dir, ms_formats) -> str:
    if Path(file).suffix in ms_formats:
        return await aconvert_to_pdf(Path(file), Path(temp_dir))
    else:
        return file


class Viewer(Component):

    EVENTS = ["change", "upload"]

    data_model = FileData

    def __init__(
        self,
        value: Any = None,
        *,
        height: int | None = None,
        label: str | None = None,
        info: str | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int | None = None,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        load_fn: Callable[..., Any] | None = None,
        every: Timer | float | None = None,
        n: int = 0,
        files_with_original_ext: list[str] = [],
        interface_language: str = "fr",
    ):
        super().__init__(
            value,
            label=label,
            info=info,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            load_fn=load_fn,
            every=every,
        )
        self.height = height

    def _process_single_file(self, f: FileData) -> NamedString | bytes:
        file_name = f.path
        if self.type == "filepath":
            file = tempfile.NamedTemporaryFile(delete=False, dir=self.GRADIO_CACHE)
            file.name = file_name
            return NamedString(file_name)
        elif self.type == "binary":
            with open(file_name, "rb") as file_data:
                return file_data.read()
        else:
            raise ValueError(
                "Unknown type: "
                + str(type)
                + ". Please choose from: 'filepath', 'binary'."
            )

    def _download_files(self, value: str | list[str]) -> str | list[str]:
        downloaded_files = []
        if isinstance(value, list):
            for file in value:
                if client_utils.is_http_url_like(file):
                    downloaded_file = processing_utils.save_url_to_cache(
                        file, self.GRADIO_CACHE
                    )
                    downloaded_files.append(downloaded_file)
                else:
                    downloaded_files.append(file)
            return downloaded_files
        if client_utils.is_http_url_like(value):
            downloaded_file = processing_utils.save_url_to_cache(
                value, self.GRADIO_CACHE
            )
            return downloaded_file
        else:
            return value

    def postprocess(self, value: str | list[str] | None) -> ListFiles | FileData | None:
        """
        Parameters:
            value: Expects a `str` filepath or URL, or a `list[str]` of filepaths/URLs.
        Returns:
            FileViewer information as a FileData object, or a list of FileData objects.
        """
        if value is None:
            return None
        self.files_with_original_ext = [os.path.basename(f) for f in value]
        ms_formats = [".docx", ".doc", ".pptx", ".ppt", ".xls", ".xlsx"]
        non_ms_files = [
            file for file in value if all(not file.endswith(ext) for ext in ms_formats)
        ]
        if is_libreoffice_installed():
            value = asyncio.run(
                aconvert_files_in_parallel(value, self.GRADIO_CACHE, ms_formats)
            )
        else:
            self.files_with_original_ext = [os.path.basename(f) for f in non_ms_files]

        value = self._download_files(value)
        if isinstance(value, list):
            return ListFiles(
                root=[
                    FileData(
                        path=file,
                        orig_name=Path(file).name,
                        size=Path(file).stat().st_size,
                    )
                    for file in value
                ]
            )
        else:
            return FileData(
                path=value,
                orig_name=Path(value).name,
                size=Path(value).stat().st_size,
            )

    def preprocess(self, payload: FileData) -> str:
        """
        This docstring is used to generate the docs for this custom component.
        Parameters:
            payload: the data to be preprocessed, sent from the frontend
        Returns:
            the data after preprocessing, sent to the user's function in the backend
        """
        return payload.path

    def example_payload(self):
        return {"foo": "bar"}

    def example_value(self):
        return {"foo": "bar"}

    def api_info(self):
        return {"type": {}, "description": "any valid json"}
