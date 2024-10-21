import sys,json
from elasticsearch import Elasticsearch

def create_index(es: Elasticsearch, index_name="java_collections_benchmarks"):
    es.indices.create(index=index_name, ignore=400)

def delete_index(es: Elasticsearch, index_name="java_collections_benchmarks"):
    es.indices.delete(index=index_name, ignore=[400, 404])

def upload_doc(es: Elasticsearch, doc: dict, index_name="java_collections_benchmarks"):
    es.index(index=index_name, body=doc)

def dict_keep(d: dict, *keys):
    return {k: d[k] for k in keys if k in d}

def doc_iterator(file_path: str):
    with open(file_path, 'r') as file:
        docs = json.load(file) # list of dictionaries
    if not isinstance(docs, list):
        raise ValueError("Expected a list of objects")
    
    for doc in docs:
        yield dict_keep(doc, "benchmark", "forks", "warmupIterations", "measurementIterations", "mode", "measurementTime", "params", "primaryMetric")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 upload.py <file_path> | python3 upload.py delete")
        sys.exit(1)
    
    es = Elasticsearch(
        "http://localhost:9200"
    )

    if sys.argv[1] == "delete":
        delete_index(es)
        print("Index deleted")
        sys.exit(0)
    
    file_path = sys.argv[1]
    create_index(es)
    for doc in doc_iterator(file_path):
        upload_doc(es, doc)
    print("Upload successful")