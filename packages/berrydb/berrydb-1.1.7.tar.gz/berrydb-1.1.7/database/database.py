import requests
from requests import Response
import json
import logging
from urllib.parse import quote
from utils.utils import Utils
from constants.constants import debug_mode
from constants.constants import (
    documents_url,
    query_url,
    document_by_id_url,
    bulk_upsert_documents_url,
    transcription_url,
    transcription_yt_url,
    caption_url,
    create_label_studio_project_url,
    import_label_studio_project_url,
    reimport_label_studio_project_url,
    couchbase_config,
    SEMANTICS_PREDICT_URL,
    SEMANTICS_ANNOTATE_URL,
    LOGGING_LEVEL,
    NER_SE_TYPE,
    MEDICAL_NER_SE_TYPE,
    TEXT_CLASSIFICATION_SE_TYPE,
    TEXT_SUMMARIZATION_SE_TYPE,
    IMAGE_CLASSIFICATION_SE_TYPE,
    IMAGE_CAPTIONING_SE_TYPE,
    PNEUMONIA_SE_TYPE,
    ALZHEIMER_SE_TYPE,
    FASHION_SE_TYPE,
    AUDIO_TRANSCRIPTION_SE_TYPE,
    extract_pdf_url,
    chat_with_database_url,
    embed_database_url,
)
from unstructured.documents.elements import PageBreak
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

logging.basicConfig(level=LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")


logger = logging.getLogger(__name__)


class Database:
    __api_key: str
    __bucket_name: str
    __database_id: int
    __database_name: str

    def __init__(self, api_key: str, bucket_name: str, database_id: int, database_name: str):
        if api_key is None:
            Utils.print_error_and_exit("API Key cannot be None")
        if bucket_name is None:
            Utils.print_error_and_exit("Bucket name cannot be None")
        if database_id is None:
            Utils.print_error_and_exit("Database not found")
        self.__api_key = api_key
        self.__bucket_name = bucket_name
        self.__database_id = database_id
        self.__database_name = database_name

    def apiKey(self):
        return self.__api_key

    def bucketName(self):
        return self.__bucket_name

    def databaseId(self):
        """Function summary

        Args:
                No Arguments

        Returns:
                str: Get the database ID of the connected database
        """
        return self.__database_id

    def databaseName(self):
        """Function summary

        Args:
                No Arguments

        Returns:
                str: Get the database name of the connected database
        """
        return self.__database_name

    def get_all_documents(self):
        """Function summary

        Args:
                No Arguments

        Returns:
                list: Return a list of documents in the connected database
        """

        url = documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_all_documents_with_col_filter(self, col_filter=["*"]):
        """Function summary

        Args:
                arg1 (list<str>): Column list (Optional)

        Returns:
                list: Return a list of filtered documents in the connected database
        """

        url = documents_url
        """ params = {
			"columns": col_filter,
			"apiKey": self.__api_key,
			"bucket": self.__bucket_name,
			"databaseId": self.__database_id,
		} """
        url += "?apiKey=" + self.__api_key
        url += "&bucket=" + self.__bucket_name
        url += "&databaseId=" + str(self.__database_id)
        url += "&columns=" + (",".join(col_filter))

        if debug_mode:
            print("url:", url)
        try:
            response = requests.get(url)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("documents result ", response.json())
            # return response.json()
            return json.loads(response.text)
        except Exception as e:
            print("Failed to fetch document: {}".format(str(e)))
            return []

    def get_document_by_object_id(
        self,
        document_id,
        key_name=None,
        key_value=None,
    ):
        """Function summary

        Args:
                arg1 (str): Document Key/Id
                arg2 (str): Key Name (optional)
                arg3 (str): Key Value (optional)

        Returns:
                list: List of Documents matching the document ID in the connected database
        """

        url = document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if document_id is not None:
            params["docId"] = document_id
        if key_name is not None:
            params["keyName"] = key_name
        if key_value is not None:
            params["keyValue"] = key_value

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.text, response.status_code)
            jsonRes = response.json()
            if debug_mode:
                print("docById result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to fetch document by id {} : {}".format(document_id, str(e)))
            return ""

    def query(self, query: str):
        """Function summary

        Args:
                arg1 (str): Query String

        Returns:
                list: Return a list of documents that match the query on the connected database.
        """

        url = query_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }
        payload = query

        if debug_mode:
            print("url:", url)
            print("query:", query)
            print("params:", params)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            if debug_mode:
                print("query result ", response.json())
            return json.loads(response.text)
        except Exception as e:
            print("Failed to query : {}".format(str(e)))
            return ""

    def __upsert(self, documents) -> str:
        url = bulk_upsert_documents_url
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        payload = json.dumps(documents)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, data=payload, headers=headers, params=params)
            if response.status_code != 200:
                try:
                    resp_content = response.json()
                except ValueError:
                    resp_content = response.text
                Utils.handleApiCallFailure(resp_content, response.status_code)
            if debug_mode:
                print("upsert result ", response)
            return response.text
        except Exception as e:
            print("Failed to upsert document: {}".format(str(e)))
            return ""

    def upsert(self, documents) -> str:
        """Function summary

        Args:
                arg1 (str): List of documents Object to add/update (Each document should have a key 'id' else a random string is assigned)

        Returns:
                str: Success/Failure message
        """
        try:
            if type(documents) != list:
                documents = [documents]
            return self.__upsert(documents)
        except Exception as e:
            print("Failed to upsert documents: {}".format(str(e)))
            return ""

    def upsert_document(self, documents) -> str:
        """(DEPRECATED)
        Function summary

        Args:
                arg1 (str): List of documents Object to add/update (Each document should have a key 'id' else a random string is assigned)

        Returns:
                str:  Success/Failure message
        """

        print("upsert_document is deprecated, please use upsert instead.")
        return ""

    def deleteDocument(self, document_id):
        """Function summary

        Args:
                arg1 (str): Document ID

        Returns:
                str: Success/Failure message
        """

        url = document_by_id_url.format(quote(document_id))
        params = {
            "apiKey": self.__api_key,
            "bucket": self.__bucket_name,
            "databaseId": self.__database_id,
        }

        if debug_mode:
            print("url:", url)
            print("params:", params)

        try:
            response = requests.delete(url, params=params)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            jsonRes = response.text
            if debug_mode:
                print("Delete document result ", jsonRes)
            return jsonRes
        except Exception as e:
            print("Failed to delete document by id {}, reason : {}".format(document_id, str(e)))
            return ""

    def transcribe(self, video_url: str):
        url = transcription_url

        body = {
            "url": video_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Transcription result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get transcription for the url {video_url}, reason : {str(e)}")
            return ""

    def transcribeYT(self, video_url: str):

        url = transcription_yt_url

        body = {
            "url": video_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Youtube transcription result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get transcription for the youtube url {video_url}, reason : {str(e)}")
            return ""

    def caption(self, image_url: str):
        url = caption_url

        body = {
            "url": image_url,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.text
            if debug_mode:
                print("Caption result: ", res)
            return res
        except Exception as e:
            print(f"Failed to get caption for the url {image_url}, reason : {str(e)}")
            return ""

    def embed(
        self,
        open_ai_api_key,
        embedding_function=None,
        limit=None,
        tokens_per_minute=None,
        model=None,
        system_prompt=None,
        compute_locally=False,
    ):
        """Function summary

        Args:
                arg1 (str): OpenAI API key to embed the database

        Returns:
                str: Success/error message of embedding the database
        """

        if compute_locally is True:
            from embeddings.embeddings import Embeddings

            embeddings = Embeddings(
                self.__database_id,
                self.__database_name,
                self.__bucket_name,
                self.__api_key,
                open_ai_api_key,
                limit,
                embedding_function,
                tokens_per_minute,
                model,
                system_prompt,
            )
            return embeddings.embedDb(compute_locally)

        url = embed_database_url

        body = {
            "database": self.__database_name,
            "apiKey": self.__api_key,
            "openAIApiKey": open_ai_api_key,
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Embed result: ", res)
            return res
        except Exception as e:
            errMsg = "Failed to embed the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            return

    def chat(
        self,
        open_ai_api_key,
        question,
        k=None,
        temperature=None,
        model=None,
        system_prompt=None,
        session_id=None,
        compute_locally=False,
    ):
        """Function summary

        Args:
                arg1 (str): OpenAI API key to embed the database
                arg2 (str): Query/Question to for your database
                arg3 (str): K value (optional)
                arg4 (str): Temperature for the LLM (optional)
                arg5 (str): Model Name (optional)
                arg6 (str): System prompt (optional)
                arg7 (bool): Chat with DB locally (optional)

        Returns:
                str: Answer/error to the query
        """

        from embeddings.embeddings import Embeddings

        if compute_locally is True:
            embeddings = Embeddings(
                self.__database_id,
                self.__database_name,
                self.__bucket_name,
                self.__api_key,
                open_ai_api_key,
                None,
                None,
                None,
                model,
                system_prompt,
                session_id,
            )
            return embeddings.ask_and_get_answers(question, k, temperature, compute_locally)

        url = chat_with_database_url

        body = {
            key: value
            for key, value in {
                "question": question,
                "k": k,
                "database": self.__database_name,
                "apiKey": self.__api_key,
                "openAIApiKey": open_ai_api_key,
                "model": model,
                "systemPrompt": system_prompt,
                "temperature": temperature,
            }.items()
            if value is not None
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Database chat result: ", res)
            return res['answer']
        except Exception as e:
            errMsg = "Failed to chat with the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            return

    def ask_and_get_answers(
        self,
        open_ai_api_key,
        question,
        k=None,
        temperature=None,
        model=None,
        system_prompt=None,
        session_id=None,
        compute_locally=False,
    ):
        """Function summary

        Args:
                arg1 (str): OpenAI API key to embed the database
                arg2 (str): Query/Question to for your database
                arg3 (str): K value (optional)
                arg4 (str): Temperature for the LLM (optional)
                arg5 (str): Model Name (optional)
                arg6 (str): System prompt (optional)
                arg7 (bool): Chat with DB locally (optional)

        Returns:
                str: Answer/error to the query
        """
        print('WARNING: This is method is deprecated. Use chat(open_ai_api_key, question) instead.')
        from embeddings.embeddings import Embeddings

        if compute_locally is True:
            embeddings = Embeddings(
                self.__database_id,
                self.__database_name,
                self.__bucket_name,
                self.__api_key,
                open_ai_api_key,
                None,
                None,
                None,
                model,
                system_prompt,
                session_id,
            )
            return embeddings.ask_and_get_answers(question, k, temperature, compute_locally)

        url = chat_with_database_url

        body = {
            key: value
            for key, value in {
                "question": question,
                "k": k,
                "database": self.__database_name,
                "apiKey": self.__api_key,
                "openAIApiKey": open_ai_api_key,
                "model": model,
                "systemPrompt": system_prompt,
                "temperature": temperature,
            }.items()
            if value is not None
        }

        payload = json.dumps(body)
        if debug_mode:
            print("url:", url)
            print("payload:", payload)
        headers = Utils.get_headers(self.__api_key)

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code != 200:
                Utils.handleApiCallFailure(response.json(), response.status_code)
            res = response.json()
            if debug_mode:
                print("Database chat result: ", res)
            return res['answer']
        except Exception as e:
            errMsg = "Failed to chat with the database. Please try again later."
            print(f"{errMsg}, reason : {str(e)}")
            return

    def ingest_pdf(self, file_list, extract_json_path=None, compute_locally=True):
        """Ingests a list of PDF files and extracts their content.

        Args:
            file_list (list[File]): List of PDF files to be processed.
            extract_json_path (str, optional): Path to save the extracted data in JSON format. Defaults to None, which saves the data under 'content'.
            compute_locally (bool, optional): If True, the processing is done locally; otherwise, it is done on BerryDB servers. Defaults to True.

        Returns:
            If compute_locally is True, returns a list of extracted documents. Otherwise, returns a success/failure message.
        """
        try:
            if type(file_list) is str:
                file_list = [file_list]
            if not file_list or not len(file_list):
                raise ValueError("At least one file must be provided")
            if len(file_list) > 5:
                raise ValueError("Exceeded maximum allowed files (5)")

            for file in file_list:
                if not file.endswith(".pdf"):
                    raise ValueError("All files must be of type PDF")

            extract_json_path = extract_json_path or "content"

            Utils.validate_json_path(extract_json_path)

            files = []
            compiled_extracted_docs = []
            for file_path in file_list:
                files.append(("files", open(file_path, "rb")))
                filename = file_path.split('/')[-1]
                if compute_locally is not True:
                    compute_locally = False

                if compute_locally:
                    print(f"Processing file: {filename}")
                    pdf_elements = partition_pdf(
                        file_path,
                        url=None,
                        strategy="hi_res",
                        infer_table_structure=True,
                    )

                    # Clean the elements
                    cleaned_elements = []
                    for el in pdf_elements:
                        if el.category != "PageBreak" or el.category != "Header" or el.category != "Footer":
                            cleaned_elements.append(el)

                    # Chunk the elements by title
                    chunks = chunk_by_title(
                        cleaned_elements,
                        max_characters=2000,
                        combine_text_under_n_chars=0,
                    )

                    # Convert the chunk into documents
                    extracted_docs = []
                    for chunk in chunks:
                        chunk_dict = chunk.to_dict()
                        content_type = chunk_dict["type"] if "type" in chunk_dict else ""
                        content_text = str(chunk_dict["text"]) if "text" in chunk_dict else ""
                        doc = {}
                        doc['type'] = content_type
                        doc['bbox'] = {}
                        doc['text'] = content_text
                        doc['source'] = filename
                        extracted_doc = Utils.create_nested_dict(extract_json_path, doc)
                        extracted_docs.append(extracted_doc)
                    if debug_mode:
                        print("Extracted Documents: ", extracted_docs)
                    print(f"Processing complete: {filename}")
                    self.upsert(extracted_docs)
                    compiled_extracted_docs += extracted_docs

                if compute_locally:
                    return compiled_extracted_docs

            url = extract_pdf_url

            params = {
                "databaseId": self.__database_id,
                "databaseName": self.__database_name,
                "apiKey": self.__api_key,
                "extractJsonPath": extract_json_path,
            }

            if debug_mode:
                print("url:", url)
                print("params:", params)

            response = requests.post(url, files=files, params=params)

            if response.status_code == 200:
                print("Success")
                response_json = response.json()
                if response_json["success"]:
                    return response_json["message"]
            else:
                print(f"Failed with ingest PDFs, status code: {response.status_code}")
        except Exception as e:
            print(f"Failed with ingest PDFs, reason: {e}")
            if debug_mode:
                raise e

    # Sematic Extraction methods
    def ner(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = NER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def medical_ner(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = MEDICAL_NER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def text_summarization(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = TEXT_SUMMARIZATION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def image_classification(self, json_path, labels, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): Labels for the classification of text
                arg3 (str): document IDs of the documents you want to extract the data of (optional)
                arg4 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = IMAGE_CLASSIFICATION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, labels, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def image_captioning(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = IMAGE_CAPTIONING_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def pneumonia_detection(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = PNEUMONIA_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def alzheimer_detection(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = ALZHEIMER_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def fashion(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = FASHION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def audio_transcription(self, json_path, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): document IDs of the documents you want to extract the data of (optional)
                arg3 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = AUDIO_TRANSCRIPTION_SE_TYPE
        try:
            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, None, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def text_classification(self, json_path, labels, document_ids=[], annotate=False):
        """Function summary

        Args:
                arg1 (str): JSON path to the object you want to extract semantic for
                arg2 (str): Labels for the classification of text
                arg3 (str): document IDs of the documents you want to extract the data of (optional)
                arg4 (str): Add sematic data to the document (optional)

        Returns:
                list | str: sematic data | hash
        """
        extraction_type = TEXT_CLASSIFICATION_SE_TYPE
        if not (labels and len(labels)):
            raise ValueError(f"Labels are required for {extraction_type} to classify the text.")
        try:

            return self.__semantic_extraction_base(extraction_type, json_path, document_ids, labels, annotate)

        except Exception as e:
            logger.exception("Failed to extract semantics for {}, reason: {}".format(extraction_type, str(e)))
            raise e

    def __semantic_extraction_base(self, extraction_type, json_path, document_ids=None, labels=None, annotate=False):

        if not json_path:
            raise ValueError("JSON path is required")
        if not annotate and not (document_ids and len(document_ids)):
            raise ValueError("Document IDs are required if you are not annotating the document")

        url = SEMANTICS_PREDICT_URL
        if annotate:
            url = SEMANTICS_ANNOTATE_URL

        params = {
            "apiKey": self.__api_key,
        }

        body = {
            "databaseId": self.__database_id,
            "documentIds": document_ids,
            "extract": extraction_type,
            "jsonPath": json_path,
        }

        if labels and len(labels):
            body["labels"] = labels

        payload = json.dumps(body)
        headers = Utils.get_headers(self.__api_key)

        logger.debug("url:", url)
        logger.debug("params:", params)
        logger.debug("payload:", payload)
        logger.debug("headers:", headers)

        response: Response = requests.post(url, params=params, data=payload, headers=headers)

        if response.status_code == 200:
            return response.json()

        logger.error("response status code: ", response.status_code)
        logger.error("response body: ", response.json())
