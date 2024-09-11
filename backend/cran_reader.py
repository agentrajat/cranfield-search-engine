from typing import Dict
import xml.etree.ElementTree as ET

"""
This file contains classes to read the Cranfield dataset files.
"""

def read_file(file_path) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print("Error occurred: ", e)
        return ""
    
def read_by_line(file_path) -> list:
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except Exception as e:
        print("Error occurred: ", e)
        return []


class Document:
    def read_from_xml(self, xml_element: ET.Element):
        self.docno = xml_element.find("docno").text
        self.docno = int(self.docno.strip())

        self.title = xml_element.find("title").text
        self.author = xml_element.find("author").text
        self.bib = xml_element.find("bib").text
        self.text = xml_element.find("text").text

        return self

    def __str__(self):
        return f"DocNo: {self.docno}\nTitle: {self.title}\nAuthor: {self.author}\nBibliography: {self.bib}\nText: {self.text}"

    def to_dict(self):
        return {
            "docno": self.docno,
            "title": self.title,
            "author": self.author,
            "bib": self.bib,
            "text": self.text
        }

class CranDocuments:
    def __init__(self):
        self.documents: Dict[Document] = {}

    def read_from_file(self, file_path):
        element = ET.fromstring("<root>" + read_file(file_path) + "</root>")

        doc_list = element.findall("doc")
        print(f"Found {len(doc_list)} documents from file.")

        for doc in doc_list:
            document = Document().read_from_xml(doc)
            self.documents[document.docno] = document
        

class Query:
    def read_from_xml(self, xml_element: ET.Element):
        self.num = xml_element.find("num").text
        self.num = int(self.num.strip())

        self.title = xml_element.find("title").text

        return self

    def __str__(self):
        return f"Number: {self.num}\nTitle: {self.title}"
    
    def to_dict(self):
        return {
            "num": self.num,
            "title": self.title
        }
    

class CranQueries:
    def __init__(self):
        self.queries: Dict[Query] = {}

    def read_from_file(self, file_path):
        root = ET.parse(file_path).getroot()

        query_list = root.findall("top")
        print(f"Found {len(query_list)} queries from file.")

        for query in query_list:
            q = Query().read_from_xml(query)
            self.queries[q.num] = q

"""
class RelevancePerQuery:
    def __init__(self):
        self.relevance = {}

    def read_from_file(self, file_path):
        lines = read_by_line(file_path)
        lines = [line.strip() for line in lines]
        self.relevance = {}
        for line in lines:
            items = line.split()
            items = [item.strip() for item in items]
            items = [item for item in items if item != ""]
            query_id = int(items[0])
            document_no = int(items[2])
            if int(items[3]) > 0:
                if query_id in self.relevance:
                    self.relevance[query_id].append(document_no)
                else:
                    self.relevance[query_id] = [document_no]
"""