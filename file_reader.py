from streamlit.runtime.uploaded_file_manager import UploadedFile
import geopandas as gpd
import laspy as lsp


def read_file(file: UploadedFile):
    if file is None:
        return FileNotFoundError("File cannot be None")
    if file.name.endswith(".geojson") or file.name.endswith(".json"):
        df = gpd.read_file(file)

    if file.name.endswith(".las") or file.name.endswith(".laz"):
        df = lsp.read(file)

    return IOError("Unsupported file type")