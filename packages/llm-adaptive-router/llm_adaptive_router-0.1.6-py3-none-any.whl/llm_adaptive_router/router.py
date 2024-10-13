from typing import Dict
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .models import RouteMetadata, QueryResult


class AdaptiveRouter:
    def __init__(
        self,
        vectorstore: VectorStore,
        llm: BaseLanguageModel,
        embeddings: Embeddings,
        routes: Dict[str, RouteMetadata],
        complexity_threshold: float = 0.7,
        update_frequency: int = 100
    ):
        self.vectorstore = vectorstore
        self.llm = llm
        self.embeddings = embeddings
        self.routes = routes
        self.complexity_threshold = complexity_threshold
        self.update_frequency = update_frequency
        self.query_count = 0
        self.feedback_data = []

        self._initialize_vectorstore()
        self._setup_llm_chain()

    def _initialize_vectorstore(self):
        for route, metadata in self.routes.items():
            
            # Convert metadata to a dictionary
            metadata_dict = metadata.dict()
            
            # Remove non-serializable entries
            if 'invoker' in metadata_dict:
                del metadata_dict['invoker']
            
            # Sanitize metadata: Convert any remaining complex types to strings
            sanitized_metadata = {}
            for key, value in metadata_dict.items():
                if isinstance(value, list) or isinstance(value, dict):
                    # Convert lists and dicts to strings
                    sanitized_metadata[key] = ', '.join(str(item) for item in value) if isinstance(value, list) else str(value)
                else:
                    sanitized_metadata[key] = value
            
            # Prepare texts: include route name, example sentences, capabilities, and any other lists
            texts = [route]  # Start with the route name

            # Include example sentences
            texts.extend(metadata.example_sentences)

            # Include capabilities and any other list fields you want to add as texts
            # Let's assume you have a list of fields you want to include
            list_fields_to_include = ['capabilities']  # Add other fields if needed
            for field_name in list_fields_to_include:
                field_values = getattr(metadata, field_name, [])
                if isinstance(field_values, list):
                    texts.extend(field_values)
            
            # Compute embeddings for all texts
            embeddings = self.embeddings.embed_documents(texts)
            
            # Prepare metadatas: replicate sanitized metadata for each text
            metadatas = [sanitized_metadata] * len(texts)
            
            # Add texts, metadatas, and embeddings to the vector store
            self.vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                embeddings=embeddings
            )

    def _setup_llm_chain(self):
        prompt = ChatPromptTemplate.from_template(
            "Given the following query and candidate models, select the most appropriate model:\n"
            "Query: {query}\n"
            "Candidate Models:\n{candidates}\n"
            "Provide your selection as a single model name."
        )
        parser = JsonOutputParser()
        self.llm_chain = prompt | self.llm | parser

    def route(self, query: str) -> RouteMetadata:
        self.query_count += 1
        
        results = self.vectorstore.similarity_search_with_score(query, k=3)
        
        if self._is_complex_query(results):
            selected_model = self._llm_selection(query, results)
        else:
            selected_model = results[0][0].metadata['model']
        
        if self.query_count % self.update_frequency == 0:
            self._update_routes()
        
        return self.routes[selected_model]

    def _is_complex_query(self, results: list[QueryResult]) -> bool:
        return results[0][1] < self.complexity_threshold

    def _llm_selection(self, query: str, candidates: list[QueryResult]) -> str:
        candidate_str = "\n".join([f"- {c[0].metadata['model']}: {c[0].metadata['capabilities']}" for c in candidates])
        response = self.llm_chain.invoke({"query": query, "candidates": candidate_str})
        return response.get("model")

    def add_feedback(self, query: str, selected_model: str, performance_score: float):
        self.feedback_data.append({
            "query": query,
            "selected_model": selected_model,
            "performance_score": performance_score
        })

    def _update_routes(self):
        # Implement logic to update routes based on feedback data
        pass

    def add_route(self, route: str, metadata: RouteMetadata):
        self.routes[route] = metadata
        self._initialize_vectorstore()

    def remove_route(self, route: str):
        if route in self.routes:
            del self.routes[route]
            # Rebuild vectorstore
            self.vectorstore.delete(where={"model": route})

    def get_routes(self) -> Dict[str, RouteMetadata]:
        return self.routes

    def set_complexity_threshold(self, threshold: float):
        self.complexity_threshold = threshold

    def set_update_frequency(self, frequency: int):
        self.update_frequency = frequency