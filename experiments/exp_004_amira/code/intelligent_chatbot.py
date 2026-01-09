# intelligent_chatbot.py
"""
Intelligent Equestrian Chatbot - Main Orchestrator
Coordinates all components to answer questions about horses
"""

from graphdb_client import GraphDBClient
from intelligent_sparql_generator import IntelligentSPARQLGenerator
from llm_client import FrenchLLMClient
from context_builder import ContextBuilder
from config import GRAPHDB_ENDPOINT, VERBOSE, SHOW_SPARQL


class IntelligentEquestrianChatbot:
    """
    Main chatbot that orchestrates the entire GraphRAG pipeline
    """
    
    def __init__(
        self,
        graphdb_endpoint: str = GRAPHDB_ENDPOINT,
        language: str = "fr"
    ):
        """
        Initialize the chatbot
        
        Args:
            graphdb_endpoint: GraphDB SPARQL endpoint
            language: Response language (fr/en)
        """
        print(" Initialisation du Chatbot Équestre Intelligent...")
        print(f"   Langue: {language.upper()}")
        print("   LLM: Local (LM Studio)")
        
        self.language = language
        
        # Initialize all components
        self.graphdb = GraphDBClient(graphdb_endpoint)
        self.llm = FrenchLLMClient(use_local=True)
        self.sparql_generator = IntelligentSPARQLGenerator(self.llm)
        self.context_builder = ContextBuilder()
        
        print("Chatbot initialisé!\n")
    
    def answer_question(self, question: str, verbose: bool = VERBOSE) -> dict:
        """
        Answer a question about horses
        
        Args:
            question: User's question in natural language
            verbose: Show detailed steps
            
        Returns:
            Dictionary with answer and metadata
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"QUESTION: {question}")
            print(f"{'='*80}\n")
        
        # STEP 1: Generate SPARQL query
        if verbose:
            print("ÉTAPE 1: Génération de la requête SPARQL...")
        
        try:
            query_result = self.sparql_generator.generate_sparql(question, self.language)
            sparql_query = query_result["sparql_query"]
            entities_used = query_result["entities_used"]
            relations_used = query_result["relations_used"]
            explanation = query_result["explanation"]
            
            if verbose:
                print("Requête générée!\n")
                print(f"Entités utilisées: {', '.join(entities_used) if entities_used else 'N/A'}")
                print(f"Relations utilisées: {', '.join(relations_used) if relations_used else 'N/A'}")
                print(f"Explication: {explanation}\n")
                
                if SHOW_SPARQL:
                    print("Requête SPARQL:")
                    print("-" * 80)
                    for line in sparql_query.split('\n'):
                        print(f"  {line}")
                    print("-" * 80)
                    print()
        
        except Exception as e:
            error_msg = f"Erreur lors de la génération SPARQL: {str(e)}"
            print(f"{error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "question": question
            }
        
        # STEP 2: Execute SPARQL on GraphDB
        if verbose:
            print("ÉTAPE 2: Exécution de la requête sur GraphDB...")
        
        try:
            results = self.graphdb.query(sparql_query)
            
            if not results or 'results' not in results:
                if verbose:
                    print("Aucun résultat retourné\n")
                return {
                    "success": False,
                    "error": "Pas de résultats",
                    "question": question,
                    "sparql_query": sparql_query
                }
            
            bindings = results['results']['bindings']
            results_count = len(bindings)
            
            if verbose:
                print(f"{results_count} résultat(s) trouvé(s)!\n")
        
        except Exception as e:
            error_msg = f"Erreur GraphDB: {str(e)}"
            print(f" {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "question": question,
                "sparql_query": sparql_query
            }
        
        # STEP 3: Build context
        if verbose:
            print("ÉTAPE 3: Construction du contexte...")
        
        try:
            context = self.context_builder.format_results(bindings, explanation)
            
            if verbose:
                print(f"Contexte créé ({len(context)} caractères)\n")
        
        except Exception as e:
            error_msg = f"Erreur contexte: {str(e)}"
            print(f"{error_msg}")
            context = str(bindings)
        
        # STEP 4: Generate natural language answer
        if verbose:
            print(" ÉTAPE 4: Génération de la réponse...")
        
        try:
            answer = self._generate_answer(question, context, results_count)
            
            if verbose:
                print("Réponse générée!\n")
        
        except Exception as e:
            error_msg = f"Erreur génération réponse: {str(e)}"
            print(f"{error_msg}")
            answer = f"Erreur: {error_msg}"
        
        # STEP 5: Display answer
        if verbose:
            print("RÉPONSE FINALE:")
            print("=" * 80)
            print(answer)
            print("=" * 80)
            print()
        
        return {
            "success": True,
            "question": question,
            "sparql_query": sparql_query,
            "entities_used": entities_used,
            "relations_used": relations_used,
            "explanation": explanation,
            "results_count": results_count,
            "context": context,
            "answer": answer,
            "raw_results": results
        }
    
    def _generate_answer(self, question: str, context: str, results_count: int) -> str:
        """Generate natural language answer"""
        
        system_prompt = """Tu es un assistant expert en données équestres.
Tu réponds aux questions en te basant UNIQUEMENT sur le contexte fourni.
Tu réponds en français, de manière claire, concise et naturelle.
Si l'information n'est pas dans le contexte, tu le dis clairement."""
        
        user_prompt = f"""Question: {question}

Contexte du graphe de connaissances ({results_count} résultats):
{context}

Réponds à la question en te basant uniquement sur ce contexte.
Sois précis, concis et naturel."""
        
        answer = self.llm.generate(user_prompt, system_prompt)
        return answer
    
    def chat(self):
        """Interactive chat mode"""
        
        print("\n🐴 Chatbot Équestre - Mode Interactif")
        print("=" * 80)
        print("Posez vos questions sur les chevaux, cavaliers, entraînements, etc.")
        print("\nExemples de questions:")
        print("  - Quels sont tous les chevaux?")
        print("  - Quel cheval a participé à quelle séance d'entraînement?")
        print("  - Quels sont les différents couplages cheval/cavalier?")
        print("  - Quel est la race du cheval?")
        print("\nTapez 'quit', 'exit' ou 'quitter' pour terminer.")
        print("=" * 80)
        
        while True:
            try:
                question = input("\n🐴 Votre question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'quitter', 'bye']:
                    print("\nAu revoir!")
                    break
                
                self.answer_question(question, verbose=True)
                
            except KeyboardInterrupt:
                print("\n\n Au revoir!")
                break
            except Exception as e:
                print(f"\n Erreur: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Chatbot Équestre Intelligent')
    parser.add_argument('--question', type=str, help='Poser une seule question')
    parser.add_argument('--quiet', action='store_true', help='Mode silencieux')
    
    args = parser.parse_args()
    
    # Create chatbot
    chatbot = IntelligentEquestrianChatbot()
    
    # Single question or interactive mode
    if args.question:
        verbose = not args.quiet
        chatbot.answer_question(args.question, verbose=verbose)
    else:
        chatbot.chat()
