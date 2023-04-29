from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from io import BytesIO


from qabot.utils.unstructured_pdf import UnstructuredPDFLoader2
from qa.settings import db_directory

def load_docs_as_vector(file):
    file_content  = file.read()
    file_io = BytesIO(file_content)
    extra_data = {"file_name": file.name}
    loader = UnstructuredPDFLoader2(file_io, **extra_data)
    splitter =  RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,)
    pages = loader.load_and_split(splitter)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=pages, embedding=embeddings, persist_directory=db_directory)
    vectordb.persist()

# def load_file_as_documents():
    # file_content = file.read()
    # from io import BytesIO
    # import pypdf
    # import PyPDF2
    # from unstructured.partition.pdf import partition_pdf
        # loader = TextLoader('./state_of_the_union.txt')
    # load_file_as_documents(file)


    # loader = UnstructuredPDFLoader('./resume.pdf', mode="elements")
    # data = loader.load()
    # splitter =  RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,)
    # pages = splitter.split_documents(data)

    # file_io = BytesIO(file_content)
    # pdf_reader = PyPDF2.PdfReader(file_io)
    # return [
    #     Document(
    #         page_content=page.extract_text(),
    #         metadata={"source": self.file_path, "page": i},
    #     )
    #     for i, page in enumerate(pdf_reader.pages)
    # ]
    # pages = []
    # for page_number in range(len(pdf_reader.pages)):
    #     # page = pdf_reader.getPage(page_number)
    #     # text += page.extractText()
    #     page = pdf_reader.pages[page_number]
    #     pages.append(
    #         Document(
    #             page_content=page.extract_text(),
    #             metadata={"source": file.name, "page": page_number},
    #         )
    #     )
    # pages = [
    #     Document(
    #         page_content=page.extract_text(),
    #         metadata={"source": file.name, "page": i},
    #     )
    #     for i, page in enumerate(pdf_reader.pages)
    # ]
    # print(pages)

    # loader = TextLoader('./state_of_the_union.txt')
    # splitter =  RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,)
    # pages = loader.load_and_split(splitter)
    # return pages
    # # vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    # retriever = vectordb.as_retriever(search_type="mmr")
    # query = "Python"
    # return retriever.get_relevant_documents(query)

    # VectorstoreIndexCreator(name=name).from_loaders([loader])
    # chroma_db.save_index(index)
#     from langchain.prompts import PromptTemplate
# from langchain.indexes.vectorstore import VectorstoreIndexCreator
# from langchain.docstore.document import Document

