import logging

debug_mode = False
LOGGING_LEVEL = logging.DEBUG

# BerryDB Base URLs
BASE_URL = "https://api.berrydb.io"
ML_BACKEND_BASE_URL = "http://gpt.berrydb.io"
BERRY_GPT_BASE_URL = "https://gpt.berrydb.io"
LABEL_STUDIO_BASE_URL = "https://api.berrydb.io/annotations"

# Profile service endpoints
get_schema_id_url = BASE_URL + "/profile/schema"
get_database_id_url = BASE_URL + "/profile/database"
create_database_url = BASE_URL + "/profile/database"
delete_database_url = BASE_URL + "/profile/database"
create_schema_url = BASE_URL + "/profile/schema"
get_database_list_by_api_key_url = BASE_URL + "/profile/database/list-by-api-key"

# Label Studio endpoints
create_label_studio_project_url = LABEL_STUDIO_BASE_URL + "/api/projects"
setup_label_config_url = LABEL_STUDIO_BASE_URL + "/api/projects/{}"
import_label_studio_project_url = (
    LABEL_STUDIO_BASE_URL + "/api/projects/{}/import?commit_to_project=false"
)
reimport_label_studio_project_url = LABEL_STUDIO_BASE_URL + "/api/projects/{}/reimport"
connect_project_to_ml_url = LABEL_STUDIO_BASE_URL + "/api/ml"
couchbase_config = "cluster_ip=13.126.134.203;cluster_username=Admin;cluster_password=123456;bucket=BerryDb;scope={};collection=bObject"
create_annotations_url = LABEL_STUDIO_BASE_URL + "/api/tasks/{}/annotations?project={}"
create_predictions_url = LABEL_STUDIO_BASE_URL + "/api/predictions"

# Berrydb service endpoints
documents_url = BASE_URL + "/berrydb/documents"
query_url = BASE_URL + "/berrydb/query"
document_by_id_url = BASE_URL + "/berrydb/documents/{}"
bulk_upsert_documents_url = BASE_URL + "/berrydb/documents/bulk"

# ML backend endpoint
transcription_url = ML_BACKEND_BASE_URL + "/transcription"
transcription_yt_url = ML_BACKEND_BASE_URL + "/transcription-yt"
caption_url = ML_BACKEND_BASE_URL + "/caption"

# Berry GPT backend endpoint
extract_pdf_url = BERRY_GPT_BASE_URL + "/extract-pdf"
embed_database_url = BERRY_GPT_BASE_URL + "/chat/embed"
chat_with_database_url = BERRY_GPT_BASE_URL + "/chat"

# Semantic extraction API endpoints
SEMANTICS_PREDICT_URL = BASE_URL + "/profile/semantics/predictions"
SEMANTICS_ANNOTATE_URL = BASE_URL + "/profile/semantics/annotations"

# Semantic extraction types
NER_SE_TYPE = "NER"
MEDICAL_NER_SE_TYPE = "Medical NER"
TEXT_CLASSIFICATION_SE_TYPE = "Text Classification"
TEXT_SUMMARIZATION_SE_TYPE = "Text Summarization"
IMAGE_CLASSIFICATION_SE_TYPE = "Image Classification"
IMAGE_CAPTIONING_SE_TYPE = "Image Captioning"
PNEUMONIA_SE_TYPE = "Pneumonia"
ALZHEIMER_SE_TYPE = "Alzheimer"
FASHION_SE_TYPE = "Fashion"
AUDIO_TRANSCRIPTION_SE_TYPE = "Audio Transcription"
TEXT_CLASSIFICATION_SE_TYPE = "Text Classification"

generic_error_message = "Oops! something went wrong. Please try again later."

# Default variables
DEFAULT_BUCKET = "BerryDb"
DEFAULT_TOKENS_PER_MINUTE = 150000
OPEN_AI_EMBEDDINGS_COST_PER_THOUSAND_TOKENS = 0.0001

# LLM related variables
DEFAULT_OPEN_AI_MODEL = "gpt-3.5-turbo"
DEFAULT_OPEN_AI_TEMPERATURE = 0.5
OPEN_AI_MODEL_TYPE_NAME = "OpenAI"
HUGGING_FACE_MIXTRAL_MODEL = "Mixtral 7B Instruct v0.2"
HUGGING_FACE_MIXTRAL_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"
HUGGING_FACE_LLAMA_MODEL = "LLama 2 7b chat"
HUGGING_FACE_LLAMA_MODEL_ID = "meta-llama/Llama-2-7b-chat"
HUGGING_FACE_FALCON_MODEL = "Falcon 40b"
HUGGING_FACE_FALCON_MODEL_ID = "tiiuae/falcon-40b"
HUGGING_FACE_TEXT_EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
