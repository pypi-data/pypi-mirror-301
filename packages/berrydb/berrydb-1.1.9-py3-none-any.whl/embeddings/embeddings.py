import os
import tiktoken
import faiss
import time
import numpy as np
from langchain.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.docstore.in_memory import InMemoryDocstore
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain.memory import ConversationBufferMemory

from database.database import Database
from constants.constants import (
    debug_mode,
    DEFAULT_TOKENS_PER_MINUTE,
    OPEN_AI_EMBEDDINGS_COST_PER_THOUSAND_TOKENS,
    DEFAULT_OPEN_AI_TEMPERATURE,
)
from constants.constants import (
    DEFAULT_OPEN_AI_MODEL,
    OPEN_AI_MODEL_TYPE_NAME,
    HUGGING_FACE_MIXTRAL_MODEL,
    HUGGING_FACE_LLAMA_MODEL,
)
from constants.constants import (
    HUGGING_FACE_MIXTRAL_MODEL_ID,
    HUGGING_FACE_LLAMA_MODEL,
    HUGGING_FACE_LLAMA_MODEL_ID,
)
from constants.constants import (
    HUGGING_FACE_FALCON_MODEL,
    HUGGING_FACE_FALCON_MODEL_ID,
    HUGGING_FACE_TEXT_EMBEDDING_MODEL_NAME,
)
from utils.utils import Utils
from loaders.berrydb_json_loader import BerryDBJSONLoader


class Embeddings:
    __berry_db_api_key: str
    __open_ai_api_key: str
    __bucket_name: str
    __database_id: str
    __database_name: str
    __embedding_function: str
    __limit: str
    __tokens_per_minute: int
    __model: str
    __system_prompt: str

    session_models: dict = {}
    session_chains: dict = {}

    def __init__(
        self,
        database_id: int,
        database_name: str,
        bucket_name: str,
        berry_db_api_key: str,
        open_ai_api_key: str,
        limit: int = None,
        embedding_function=None,
        tokens_per_minute: int = None,
        model: str = None,
        system_prompt: str = None,
        session_id: str = None,
    ):
        if not database_id:
            Utils.print_error_and_exit("Database cannot be None")
        if not database_name:
            Utils.print_error_and_exit("Database name cannot be None")
        if not bucket_name:
            Utils.print_error_and_exit("Bucket name cannot be None")
        if not berry_db_api_key:
            Utils.print_error_and_exit("API Key cannot be None")
        if not open_ai_api_key:
            Utils.print_error_and_exit("OpenAI API Key cannot be None")
        if limit and not (isinstance(limit, int) and int(limit) > 0):
            Utils.print_error_and_exit("Limit should be empty or a positive integer")
        if tokens_per_minute and isinstance(tokens_per_minute, int):
            tokens_per_minute = int(tokens_per_minute)
            if not tokens_per_minute > 0:
                Utils.print_error_and_exit(
                    "Tokens per minute should be empty or a positive integer"
                )
            if tokens_per_minute < DEFAULT_TOKENS_PER_MINUTE:
                Utils.print_error_and_exit(
                    f"Tokens per minute cannot be less than {DEFAULT_TOKENS_PER_MINUTE}"
                )

        self.__berry_db_api_key = berry_db_api_key
        self.__open_ai_api_key = open_ai_api_key
        self.__bucket_name = bucket_name
        self.__database_id = database_id
        self.__database_name = database_name
        self.__embedding_function = embedding_function
        self.__limit = int(limit) if limit else None
        self.__tokens_per_minute = (
            tokens_per_minute if tokens_per_minute else DEFAULT_TOKENS_PER_MINUTE
        )
        self.__model = model
        self.__system_prompt = system_prompt
        self.__session_id = session_id

    def embedDb(self):
        if debug_mode:
            print("self.__database_id: ", self.__database_id)
            print("self.__database_name: ", self.__database_name)
            print("self.__bucket_name: ", self.__bucket_name)
            print("self.__tokens_per_minute: ", self.__tokens_per_minute)
            print("self.__model: ", self.__model)
            print("self.__system_prompt: ", self.__system_prompt)
            # print(f"Checking if you have access to {self.__database_name}")

        documents = []
        records = self.__get_all_records_for_database()
        records = [item["BerryDb"] for item in records]
        if self.__limit:
            records = records[: self.__limit]
        if debug_mode:
            print(f"Fetched {len(records)} records")
        if len(records) <= 0:
            Utils.print_error_and_exit("Database does not have any records")

        documents = self.__load_JSON(records)

        tokens, embedding_cost = self.__calculate_embedding_cost(documents)
        if debug_mode:
            print(f"Embedding Cost: ${embedding_cost:.4f}")
            print(f"Number of chunks: {len(documents)}")

        return self.__embed_docs(documents, True, self.__embedding_function)

    def __get_chat_model(self, temperature):
        try:
            memory = None
            if self.__session_id:
                print(
                    "*************************Finding llm_model for session with id: ",
                    self.__session_id,
                )
                """ llm_model = (
                    Embeddings.session_models[self.__session_id]
                    if self.__session_id in Embeddings.session_models
                    else None
                ) """
                memory = (
                    Embeddings.session_models[self.__session_id]
                    if self.__session_id in Embeddings.session_models
                    else None
                )
                if memory:
                    print(
                        "*************************Found memory for: ",
                        self.__session_id,
                        " memory: ",
                        memory,
                    )
                """ if llm_model:
                    print(
                        "*************************Found llm_model for: ",
                        self.__session_id,
                    )
                    return llm_model """
            """ print(
                "*************************Couldn't find llm_model for: ",
                self.__session_id,
            ) """
            if self.__model == HUGGING_FACE_MIXTRAL_MODEL_ID:
                # max_length=128,
                llm_model = HuggingFaceEndpoint(
                    repo_id=HUGGING_FACE_MIXTRAL_MODEL_ID,
                    temperature=temperature,
                    model_kwargs={"trust_remote_code": True},
                    huggingfacehub_api_token=self.__open_ai_api_key,
                )
                # return HuggingFaceHub(HUGGING_FACE_MIXTRAL_MODEL_ID)
            elif self.__model == HUGGING_FACE_LLAMA_MODEL_ID:
                llm_model = HuggingFaceEndpoint(
                    repo_id=HUGGING_FACE_LLAMA_MODEL_ID,
                    temperature=temperature,
                    model_kwargs={"trust_remote_code": True},
                    huggingfacehub_api_token=self.__open_ai_api_key,
                )
                # return HuggingFaceHub(HUGGING_FACE_LLAMA_MODEL_ID)
            elif self.__model == HUGGING_FACE_FALCON_MODEL_ID:
                llm_model = HuggingFaceEndpoint(
                    repo_id=HUGGING_FACE_FALCON_MODEL_ID,
                    temperature=temperature,
                    model_kwargs={"trust_remote_code": True},
                    huggingfacehub_api_token=self.__open_ai_api_key,
                )
                # return HuggingFaceHub(HUGGING_FACE_LLAMA_MODEL_ID)
            else:
                self.__model = self.__model or DEFAULT_OPEN_AI_MODEL
                llm_model = ChatOpenAI(
                    model=self.__model,
                    temperature=temperature or DEFAULT_OPEN_AI_TEMPERATURE,
                    openai_api_key=self.__open_ai_api_key,
                )
            """ if self.__session_id:
                Embeddings.session_models[self.__session_id] = llm_model """
            if self.__session_id:
                if not memory:
                    memory = ConversationBufferMemory(
                        memory_key="history", input_key="question", return_messages=True
                    )
                    Embeddings.session_models[self.__session_id] = memory
            return llm_model
            # else:
            #     Utils.print_error_and_exit(f"Model named {self.__model} not found")
        except Exception as e:
            raise e
            # Utils.print_error_and_exit(
            #     f"Unable to find model named {self.__model}, reason: {e['error']['message'] if (('error' in e) and ('message' in e['error'])) else e}"
            # )

    def ask_and_get_answers(
        self,
        q,
        k=None,
        temperature=None,
    ):
        """llm = ChatOpenAI(
            model="gpt-3.5-turbo", temperature=temperature, openai_api_key=self.__open_ai_api_key
        )"""
        chain = None
        prompt_template = (
            "System: " + self.__system_prompt if self.__system_prompt else ""
        )
        llm = self.__get_chat_model(temperature)
        v_store = self.__get_vector_store()
        retriever = v_store.as_retriever(search_kwargs={"k": k or 3})

        if self.__session_id:
            chain = (
                Embeddings.session_chains[self.__session_id]
                if self.__session_id in Embeddings.session_chains
                else None
            )
            """prompt_template +=

            {context}

            Question: {question}
            """
            # if memory:
            prompt_template += """
            Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question:
            ------
            <ctx>
            {context}
            </ctx>
            ------
            <hs>
            {history}
            </hs>
            ------
            {question}
            Answer:
            """
            # else:
            #     prompt_template += """
            #     Use the following context (delimited by <ctx></ctx>) to answer the question:
            #     ------
            #     <ctx>
            #     {context}
            #     </ctx>
            #     ------
            #     {question}
            #     Answer:
            #     """
            prompt_with_question = PromptTemplate(
                template=prompt_template,
                input_variables=(["history", "context", "question"]),
            )
            chain_type_kwargs = {
                "prompt": prompt_with_question,
                "verbose": True,
            }
            # if memory:
            #     chain_type_kwargs["memory"] = memory
            # chain_type_kwargs = {"prompt": final_prompt}
        if not chain:
            prompt_template += """
                Use the following context (delimited by <ctx></ctx>) to answer the question:
                ------
                <ctx>
                {context}
                </ctx>
                ------
                {question}
                Answer:
                """
            prompt_with_question = PromptTemplate(
                template=prompt_template,
                input_variables=(["context", "question"]),
            )
            chain_type_kwargs = {
                "prompt": prompt_with_question,
                "verbose": True,
            }
            chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs=chain_type_kwargs,
            )
            if self.__session_id:
                Embeddings.session_chains[self.__session_id] = chain
        answer = chain.run(q)
        if debug_mode:
            print("answer: ", answer)
        return answer

    def __get_embeddings_from_docs(self, open_ai_api_key):
        if (
            self.__model == HUGGING_FACE_MIXTRAL_MODEL_ID
            or self.__model == HUGGING_FACE_LLAMA_MODEL_ID
            or self.__model == HUGGING_FACE_FALCON_MODEL_ID
        ):
            return HuggingFaceHubEmbeddings(
                model=HUGGING_FACE_TEXT_EMBEDDING_MODEL_NAME,
                task="feature-extraction",
                huggingfacehub_api_token=open_ai_api_key,
            )
        return OpenAIEmbeddings(openai_api_key=open_ai_api_key)

    def __get_vector_store(self):
        if not self.is_embedded():
            Utils.print_error_and_exit(
                f"Database with name {self.__database_name} is not embedded. Please embed the database and try again."
            )
        records = self.__get_all_records_for_database()
        records = [item["BerryDb"] for item in records]
        docs = self.__load_JSON(records)
        vector_store = self.__embed_docs(docs)
        return vector_store

    def __embed_docs(
        self,
        documents,
        generate_embeddings=False,
        embedding_function=None,
    ):
        if embedding_function and not callable(embedding_function):
            Utils.print_error_and_exit("Embedding Function must be a function or None")

        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]

        if embedding_function:
            return embedding_function(documents)

        embedding = self.__get_embeddings_from_docs(self.__open_ai_api_key)

        if generate_embeddings:
            # self.get_embeddings_from_docs(generate_embeddings, embedding_function)

            # embeddings = embedding.embed_documents(texts)
            embeddings = self.__embed_texts_with_rate_limit(
                embedding, texts, self.__tokens_per_minute
            )
            index = faiss.IndexFlatIP(len(embeddings[0]))
            vector = np.array(embeddings, dtype=np.float32)
            index.add(vector)
        else:
            try:
                embeddings_file_path = self.__get_embeddings_path(
                    self.__database_id, self.__database_name
                )
                if debug_mode:
                    print("embeddings_file_path: ", embeddings_file_path)
                vector = np.load(embeddings_file_path)
                index = faiss.IndexFlatIP(len(vector[0]))
                index.add(vector)
            except Exception as e:
                # raise e
                Utils.print_error_and_exit(
                    f"Database with name {self.__database_name} is not embedded. Please embed the database and try again."
                )

        documents = []

        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            documents.append(Document(page_content=text, metadata=metadata))
        index_to_docstore_id = {
            i: doc.metadata["objectId"] for i, doc in enumerate(documents)
        }
        if debug_mode:
            print("index to doctore map")
            # print(index_to_docstore_id)
        docstore = InMemoryDocstore(
            {index_to_docstore_id[i]: doc for i, doc in enumerate(documents)}
        )

        faiss_vector_store = FAISS(
            embedding.embed_query, index, docstore, index_to_docstore_id
        )

        if generate_embeddings:
            file_path = self.__get_embeddings_path(
                self.__database_id, self.__database_name
            )
            doc_store_id_to_index = {
                index_to_docstore_id[i]: i for i in range(len(index_to_docstore_id))
            }
            """ if debug_mode:
                print(doc_store_id_to_index) """
            self.__persist_embeddings(file_path, vector)
            self.__store_embedding_data(file_path, doc_store_id_to_index)

        return faiss_vector_store

    def __embed_texts_with_rate_limit(self, embedding, texts, tokens_per_minute):
        time_limit_in_seconds = 70
        chunked_texts = []
        total_tokens = 0
        timer_start = time.time()
        enc = tiktoken.encoding_for_model("text-embedding-ada-002")

        text_embeddings = []
        print(f"A total of {len(texts)} texts received for embedding\n\n")
        for text in texts:
            # print(f"text: {text}")
            # tokens = enc.count_tokens(text)
            # tokens = len(enc.encode(text))
            tokens = sum([len(enc.encode(words)) for words in text])
            # print(f"tokens: {tokens}")
            if (
                total_tokens + tokens > tokens_per_minute
                and time.time() - timer_start < time_limit_in_seconds
            ):
                remaining_time = max(
                    0, time_limit_in_seconds - (time.time() - timer_start)
                )
                if debug_mode:
                    print(f"total_tokens: {total_tokens}")
                    print(f"tokens: {tokens}")
                    print(f"remaining_time: {remaining_time}")
                    print(f"Embedding {total_tokens} tokens\n")

                text_embeddings.extend(embedding.embed_documents(chunked_texts))
                print(
                    f"Embedded a total of {len(text_embeddings)} of {len(texts)}: ({int(len(text_embeddings) / len(texts) * 100)}%)\n"
                )
                # print(f"Total embeddings length: {len(text_embeddings)}\n")
                chunked_texts = []

                if debug_mode:
                    print(f"Sleeping for {remaining_time} seconds\n")
                time.sleep(remaining_time)
                timer_start = time.time()
                total_tokens = 0

            chunked_texts.append(text)
            total_tokens += tokens

        if chunked_texts:
            print(f"Embedding {len(chunked_texts)} remaining tokens\n")
            text_embeddings.extend(embedding.embed_documents(chunked_texts))
            print(
                f"Embedded a total of {len(text_embeddings)} of {len(texts)}: ({int(len(text_embeddings) / len(texts)) * 100}%)\n"
            )

        print(f"Embedded a total of {len(chunked_texts)} tokens\n\n\n")
        return text_embeddings

    def __get_embeddings_path(self, database_id, database_name):
        embeddings_file_path_prefix = os.environ.get(
            "EMBEDDINGS_FILE_PATH_PREFIX", "embeddings/"
        )
        if debug_mode:
            print("embeddings_file_path_prefix: ", embeddings_file_path_prefix)
        if embeddings_file_path_prefix and not os.path.exists(
            embeddings_file_path_prefix
        ):
            os.makedirs(embeddings_file_path_prefix)
        return f"{embeddings_file_path_prefix if embeddings_file_path_prefix else ''}{str(database_id)}_{database_name}_embeddings.npy"

    def __persist_embeddings(self, file_path, embeddings):
        # Convert embeddings to a NumPy array and persist to file system
        embeddings_array = np.array(embeddings)
        np.save(file_path, embeddings_array)

    def __store_embedding_data(self, file_path, mappings):
        data = {
            "databaseId": self.__database_id,
            "path": file_path,
            "mappings": mappings,
        }
        doc = {"id": str(self.__database_id) + "_" + self.__database_name, "data": data}

        self.__upsert_file_path_data_into_vector_bucket(doc)

    def __calculate_embedding_cost(self, texts):
        enc = tiktoken.encoding_for_model("text-embedding-ada-002")
        total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
        return (
            total_tokens,
            total_tokens / 1000 * OPEN_AI_EMBEDDINGS_COST_PER_THOUSAND_TOKENS,
        )
        # return len(texts), 0

    def __get_all_records_for_database(self):
        db = Database(
            self.__berry_db_api_key,
            self.__bucket_name,
            self.__database_id,
            self.__database_name,
        )
        records = db.get_all_documents()
        if debug_mode:
            print(f"A total of {len(records)} fetched")
            # print(records)
        return records

    def __load_JSON(self, records):
        # loader = BerryDBJSONCSVLoader(json_data=records, text_content=False)
        loader = BerryDBJSONLoader(
            json_data=records, jq_schema=".[]", text_content=False
        )
        return loader.load()

    def __upsert_file_path_data_into_vector_bucket(self, data):
        berryDb_vectors_bkt = Database(
            self.__berry_db_api_key,
            "Vectors",
            self.__database_id,
            self.__database_name,
        )
        berryDb_vectors_bkt.upsert(data)

    def is_embedded(self):
        berryDb_vectors = Database(
            self.__berry_db_api_key, "Vectors", self.__database_id, self.__database_name
        )
        # query = f'Select * from Vectors where databaseId = {db_id}'
        query = f"SELECT COUNT(*) AS count FROM `Vectors` WHERE databaseId = '{self.__database_id}'"
        result = berryDb_vectors.query(query)
        # if debug_mode:
        # print("result: ", result)
        try:
            count = result[0]["count"]
        except:
            count = 0
        return bool(count)

    def delete_embeddings(self):
        if debug_mode:
            print("self.__database_id: ", self.__database_id)
            print("self.__database_name: ", self.__database_name)
            print("self.__database_name: ", self.__berry_db_api_key)

        self.__delete_embeddings_file()

    def __delete_embeddings_file(self):
        file_path = self.__get_embeddings_path(self.__database_id, self.__database_name)
        try:
            os.remove(file_path)
        except OSError as e:
            print(
                "Error: Failed to delete embeddings file. Database may not have been embedded."
            )