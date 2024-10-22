import sys,json
from elasticsearch import Elasticsearch

def create_index(es: Elasticsearch, index_name="java_collections_benchmarks"):
    es.options(ignore_status=400).indices.create(index=index_name)

def delete_index(es: Elasticsearch, index_name="java_collections_benchmarks"):
    es.options(ignore_status=404).indices.delete(index=index_name)

def clear_index(es: Elasticsearch, index_name="java_collections_benchmarks"):
    es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})

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
        doc["params"]["size"] = int(doc["params"]["size"])
        if "progress" in doc["params"]:
            doc["params"]["progress"] = int(doc["params"]["progress"])
        doc["benchmark"] = doc["benchmark"].split(".")[-1]
        
        doc = dict_keep(doc, "benchmark", "forks", "warmupIterations", "measurementIterations", "mode", "measurementTime", "params", "primaryMetric")
        doc["primaryMetric"] = dict_keep(doc["primaryMetric"], "score", "scoreError", "scoreConfidence", "scorePercentiles", "scoreUnit")
        yield doc

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

    if sys.argv[1] == "clear":
        clear_index(es)
        print("Index cleared")
        sys.exit(0)
    
    file_path = sys.argv[1]
    create_index(es)
    for doc in doc_iterator(file_path):
        upload_doc(es, doc)
        print(f"Uploaded: {doc['benchmark']}/{'/'.join(str(v) for v in doc['params'].values())}")
    print("Upload successful")