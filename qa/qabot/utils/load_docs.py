from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.indexes import VectorstoreIndexCreator

# chroma_db = ChromaDB(
#     url="sqlite:///my_db.sqlite",
# )

def load_docs(file):
    name, ext = os.path.splitext(file.name)
    if ext == ".pdf":
        loader = PyPDFLoader(file)
    elif ext == ".docx":
        loader = UnstructuredWordDocumentLoader(file)
    elif ext == ".txt":
        loader = TextLoader(file)
    
    index = VectorstoreIndexCreator(name=name).from_loaders([loader])
    # chroma_db.save_index(index)

