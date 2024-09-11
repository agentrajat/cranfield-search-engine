from cran_reader import CranQueries, CranDocuments, Document
from indexing import Indexing
from retrieval_models import BaseModel, VectorSpaceModel, BM25Model, QueryLikelyhoodDPSModel
from evaluation import Evaluation
from typing import List

document_path = "./cranfield-trec-dataset/cran.all.1400.xml"
query_path = "./cranfield-trec-dataset/cran.qry.xml"

class IRSystem:
    def __init__(self, 
                 initialize_vsm = True, 
                 vsm_args: dict = {},
                 initialize_bm25 = True,
                 bm25_args: dict = {},
                 initialize_qldps = True, 
                 qldps_args: dict = {}
                 ):
        print("Initializing IR System")
        
        print("Reading documents and queries")
        document_reader = CranDocuments()
        document_reader.read_from_file(document_path)
        self.documents = document_reader.documents
        
        query_reader = CranQueries()
        query_reader.read_from_file(query_path)
        self.queries = query_reader.queries

        print("Building index")
        self.index = Indexing()
        self.index.build_index(self.documents.values())

        print("Initializing retrieval models")
        self.models = {}

        if initialize_vsm:
            self.models["vsm"] = VectorSpaceModel(self.index, **vsm_args)

        if initialize_bm25:
            self.models["bm25"] = BM25Model(self.index, **bm25_args)

        if initialize_qldps:
            self.models["qldps"] = QueryLikelyhoodDPSModel(self.index, **qldps_args)

        print("IR System initialized")

    def get_model(self, model: str) -> BaseModel:
        return self.models[model]

    def search(self, query: str, model: str) -> List[dict]:
        print(f"Searching for '{query}' using {model}")
        results = self.get_model(model).query_on_index(query)
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        tokens = self.index.process_text(query)
        return {
            "tokens": tokens,
            "results": [{"docno": docno, "score": score} for docno, score in results]
        }
    
    def get_documents(self, docnos: list) -> List[dict]:
        return [self.documents[int(docno)].to_dict() for docno in docnos]
    
    def evaluate_model(self, model: BaseModel) -> dict:
        evaluator = Evaluation()
        evaluator.evaluate_model(model, self.queries.values())
        return evaluator
    
    def evaluate_model(self, model: BaseModel) -> dict:
        evaluator = Evaluation()
        evaluator.evaluate_model(model, self.queries.values())
        return evaluator
    
    def get_metrics(self, evaluator: Evaluation) -> dict:
        result = evaluator.trec_eval()
        # result["mean_ndcg"] = round(sum(evaluator.ndcg_per_query) / len(evaluator.ndcg_per_query), 4)
        return result