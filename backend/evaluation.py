from cran_reader import Query
# from cran_reader import RelevancePerQuery
from retrieval_models import BaseModel
from typing import List
import os, subprocess

class Metric:
    def __init__(self, query_id, doc_id, rank, similarity, run_id):
        self.query_id = query_id
        self.doc_id = doc_id
        self.rank = rank
        self.similarity = similarity
        self.run_id = run_id

    def __str__(self):
        return f"{self.query_id} iter {self.doc_id} {self.rank} {self.similarity} {self.run_id}"


class Evaluation:
    def __init__(self, output_dir = './output/'):
        self.output_dir = output_dir
        # For windows
        self.trec_eval_path = "./trec_eval-9.0.8-built-windows/trec_eval.exe"
        # For linux
        # self.trec_eval_path = "./trec_eval/trec_eval"
        self.test_file_path = "./cranfield-trec-dataset/cranqrel.trec.txt"
        self.output_file_path = None
        self.model_name = None
        self.metrics = None
        self.ndcg_per_query = None

    def parse_trec_eval(self, trec_output):
        dict = {}
        for line in trec_output.split("\n"):
            if line.strip() == "":
                continue
            param, _, value = line.split("\t")
            dict[param.strip()] = float(value.strip())
        return dict
    

    def trec_eval(self):
        if self.output_file_path is None:
            print("Please run evaluate_model first")
            return
        
        print(f"Executing trec_eval for {self.model_name}...")
        p = subprocess.Popen([self.trec_eval_path, self.test_file_path, self.output_file_path, "-m", "map", "-m", "P.5", "-m", "ndcg"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return self.parse_trec_eval(out.decode("utf-8"))
    
    # def calculate_ndcg(self, relevant_docs, retrieved_docs):
    #     # Calculating DCG
    #     dcg = 1 if retrieved_docs[0] in relevant_docs else 0
    #     for i in range(1, len(retrieved_docs)):
    #         if retrieved_docs[i] in relevant_docs:
    #             dcg += 1 / math.log2(i + 1)

    #     # Calculating IDCG
    #     idcg = 1
    #     for i in range(1, len(relevant_docs)):
    #         idcg += 1 / math.log2(i + 1)

    #     return dcg / idcg
    
    
    def generate_output_file(self):
        print(f"\nCreating output file...")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = self.output_dir + self.model_name + ".txt"
        with open(file_path, 'w') as file:
            for metric in self.metrics:
                file.write(str(metric) + "\n")

        self.output_file_path = file_path
        print(f"Output file created at {file_path}")
        return file_path


    def evaluate_model(self, model: BaseModel, queries: List[Query], run_id = "1", select_top = -1):
        self.model_name = model.__class__.__name__
        self.ndcg_per_query = []
        metrics = []

        # relevance_per_query = RelevancePerQuery()
        # relevance_per_query.read_from_file(self.test_file_path)

        for index, query in enumerate(queries):
            query_ref_id = index + 1
            print(f"Running queries... ({index + 1} / {len(queries)})", end='\r')
            similarities: dict = model.query_on_index(query.title)
            similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
            
            if select_top > 0:
                similarities = similarities[:select_top]

            rank = 1
            for (doc_id, similarity) in similarities:
                # metric = Metric(query.num, doc_id, rank, similarity, run_id)
                metric = Metric(query_ref_id, doc_id, rank, similarity, run_id)
                metrics.append(metric)
                rank += 1

            # Calculating NDCG
            # relevant_docs = relevance_per_query.relevance.get(query_ref_id, [])
            # if len(relevant_docs) == 0:
            #     raise Exception(f"Query {query.num} with index {index} has no relevant docs")
            
            # retrieved_docs = [doc_id for (doc_id, _) in similarities[:len(relevant_docs)]]
            # ndcg = self.calculate_ndcg(relevant_docs, retrieved_docs)
            # self.ndcg_per_query.append(ndcg)

        self.metrics = metrics
        self.generate_output_file()

        return self


    
