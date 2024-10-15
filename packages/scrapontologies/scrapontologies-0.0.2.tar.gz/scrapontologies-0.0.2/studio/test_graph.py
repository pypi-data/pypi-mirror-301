from scrapontology import PDFParser, LLMClient
import os
from dotenv import load_dotenv

def test_entities_schema_graph():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Create an LLMClient instance
    llm_client = LLMClient(api_key)

    # Create a PDFParser instance
    pdf_parser = PDFParser(llm_client)

    # Get the entities schema graph
    entities_schema_graph = pdf_parser.get_entities_schema_graph()

    # Assert that the graph is not None
    assert entities_schema_graph is not None

    return entities_schema_graph
if __name__ == "__main__":
    entities_schema_graph = test_entities_schema_graph()