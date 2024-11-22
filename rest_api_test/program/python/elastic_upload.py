from elasticsearch import Elasticsearch as ES
import sys,json

mapping = {
    "properties": {
        "round": {"type": "keyword"},
        "idTS": {"type": "keyword"},
        "nameTS": {"type": "keyword"},
        "idTC": {"type": "keyword"},
        "nameTC": {"type": "keyword"},
        "status": {"type": "keyword"},
        "timestamp": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
        "totalTime": {"type": "double"},
        "httpMethod": {"type": "keyword"},
        "message": {"type": "text"},
    }
}

def create_index(es: ES, index_name="rest_api_test"):
    es.options(ignore_status=400).indices.create(index=index_name, mappings=mapping)

def delete_index(es: ES, index_name="rest_api_test"):
    es.options(ignore_status=400).indices.delete(index=index_name)

def clear_index(es: ES, index_name="rest_api_test"):
    es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})

def upload_doc(es: ES, doc: dict, index_name="rest_api_test"):
    es.index(index=index_name, body=doc, id=f"{doc['round']}#{doc['idTC']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 upload.py <file_path> | python3 upload.py delete")
        sys.exit(1)
    
    es = ES(
        "http://localhost:9200"
    )

    if sys.argv[1] == "delete":
        delete_index(es)
        print("Index deleted")
        sys.exit(0)

    if sys.argv[1] == "clear":
        clear_index(es)
        print("Index cleared")
        sys.exit(0)
    
    file_path = sys.argv[1]
    create_index(es)

    with open(file_path, 'r') as file:
        docs = json.load(file)
    if not isinstance(docs, list):
        raise ValueError("Expected a list of objects")
    
    for doc in docs:
        upload_doc(es, doc)
        print(f"Uploaded: {doc['round']}#{doc['idTC']}")