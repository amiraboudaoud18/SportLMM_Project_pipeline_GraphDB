# cinema_chatbot.py
"""
Cinema Chatbot - French Movies Database
No classifier - LLM generates SPARQL dynamically
Local LLM only (LM Studio)
"""


from graphdb_client import GraphDBClient
from cinema_sparql_generator import CinemaSPARQLGenerator
from llm_client import FrenchLLMClient


class CinemaChatbot:
    """
    Intelligent cinema chatbot - French movies
    Generates SPARQL queries dynamically using local LLM
    """
    
    def __init__(
        self,
        graphdb_endpoint: str = "http://localhost:7200/repositories/movie-test"
    ):
        """
        Initialize the cinema chatbot
        
        Args:
            graphdb_endpoint: GraphDB SPARQL endpoint
        """
        print(" Initialisation du Chatbot Cinéma...")
        print("   Base de données: Films français")
        print("   LLM: Local (LM Studio)")
        
        # Initialize components
        self.graphdb = GraphDBClient(graphdb_endpoint)
        self.llm = FrenchLLMClient(use_local=True)
        self.sparql_generator = CinemaSPARQLGenerator(self.llm)
        
        print("Chatbot cinéma initialisé!\n")
    
    def answer_question(self, question: str, verbose: bool = True) -> dict:
        """
        Answer a question about movies
        
        Args:
            question: User's question in French
            verbose: If True, print detailed steps
            
        Returns:
            Dictionary with answer and all intermediate steps
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"QUESTION: {question}")
            print(f"{'='*80}\n")
        
        # STEP 1: Generate SPARQL query using LLM
        if verbose:
            print("ÉTAPE 1: Génération de la requête SPARQL...")
        
        try:
            query_result = self.sparql_generator.generate_sparql(question, "fr")
            sparql_query = query_result["sparql_query"]
            entities_used = query_result["entities_used"]
            relations_used = query_result["relations_used"]
            explanation = query_result["explanation"]
            
            if verbose:
                print(" Requête générée!\n")
                print(f" Entités utilisées: {', '.join(entities_used) if entities_used else 'N/A'}")
                print(f" Relations utilisées: {', '.join(relations_used) if relations_used else 'N/A'}")
                print(f" Explication: {explanation}\n")
                print(" Requête SPARQL:")
                print("-" * 80)
                # Pretty print SPARQL
                for line in sparql_query.split('\n'):
                    print(f"  {line}")
                print("-" * 80)
                print()
        
        except Exception as e:
            error_msg = f"Erreur lors de la génération de la requête: {str(e)}"
            print(f" {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "question": question
            }
        
        # STEP 2: Execute SPARQL query on GraphDB
        if verbose:
            print(" ÉTAPE 2: Exécution de la requête sur GraphDB...")
        
        try:
            results = self.graphdb.query(sparql_query)
            
            if not results or 'results' not in results:
                if verbose:
                    print("Aucun résultat retourné par GraphDB\n")
                return {
                    "success": False,
                    "error": "Pas de résultats",
                    "question": question,
                    "sparql_query": sparql_query,
                    "entities_used": entities_used,
                    "relations_used": relations_used
                }
            
            bindings = results['results']['bindings']
            results_count = len(bindings)
            
            if verbose:
                print(f" {results_count} résultat(s) trouvé(s)!\n")
        
        except Exception as e:
            error_msg = f"Erreur lors de l'exécution de la requête: {str(e)}"
            print(f" {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "question": question,
                "sparql_query": sparql_query
            }
        
        # STEP 3: Build context from results
        if verbose:
            print(" ÉTAPE 3: Construction du contexte...")
        
        try:
            context = self._format_results_as_context(bindings, explanation)
            
            if verbose:
                print(f"Contexte créé ({len(context)} caractères)\n")
                print(" Aperçu du contexte:")
                print("-" * 80)
                print(context[:500] + "..." if len(context) > 500 else context)
                print("-" * 80)
                print()
        
        except Exception as e:
            error_msg = f"Erreur lors de la construction du contexte: {str(e)}"
            print(f"{error_msg}")
            context = str(bindings)
        
        # STEP 4: Generate natural language answer using LLM
        if verbose:
            print(" ÉTAPE 4: Génération de la réponse en langage naturel...")
        
        try:
            answer = self._generate_answer(question, context, results_count)
            
            if verbose:
                print(" Réponse générée!\n")
        
        except Exception as e:
            error_msg = f"Erreur lors de la génération de la réponse: {str(e)}"
            print(f" {error_msg}")
            answer = f"Erreur: {error_msg}"
        
        # STEP 5: Display final answer
        if verbose:
            print(" RÉPONSE FINALE:")
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
    
    def _format_results_as_context(self, bindings: list, explanation: str) -> str:
        """Format SPARQL results as readable context"""
        
        if not bindings:
            return "Aucune donnée trouvée dans la base de données cinéma."
        
        context = f"Contexte de la requête: {explanation}\n\n"
        context += f"Données trouvées ({len(bindings)} résultats):\n\n"
        
        for i, binding in enumerate(bindings, 1):
            context += f"Résultat {i}:\n"
            for key, value in binding.items():
                if 'value' in value:
                    display_value = value['value']
                    # Shorten URIs
                    if display_value.startswith('http://'):
                        display_value = display_value.split('#')[-1]
                    context += f"  - {key}: {display_value}\n"
            context += "\n"
        
        return context
    
    def _generate_answer(self, question: str, context: str, results_count: int) -> str:
        """Generate natural language answer using LLM"""
        
        system_prompt = """Tu es un assistant expert en cinéma français.
Tu réponds aux questions en te basant UNIQUEMENT sur le contexte fourni de la base de données.
Tu réponds en français, de manière claire, naturelle et engageante.
Si l'information n'est pas dans le contexte, tu le dis clairement.
Tu peux mentionner des détails intéressants comme les notes, années, réalisateurs, etc."""
        
        user_prompt = f"""Question: {question}

Contexte de la base de données cinéma ({results_count} résultats):
{context}

Réponds à la question en te basant uniquement sur ce contexte.
Sois précis, informatif et naturel. Mentionne les détails pertinents."""
        
        # Generate answer
        answer = self.llm.generate(user_prompt, system_prompt)
        
        return answer
    
    def chat(self):
        """Interactive chat mode"""
        
        print("\n Chatbot Cinéma - Mode Interactif")
        print("=" * 80)
        print("Posez vos questions sur les films français!")
        print("Exemples:")
        print("  - Quels sont tous les films?")
        print("  - Qui a réalisé Amélie Poulain?")
        print("  - Films avec Omar Sy")
        print("  - Films de comédie")
        print("  - Films sortis après 2010")
        print("  - Quel est le meilleur film noté?")
        print("\nTapez 'quit', 'exit' ou 'quitter' pour terminer.")
        print("=" * 80)
        
        while True:
            question = input("\n Votre question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'quitter', 'bye']:
                print("\n Au revoir! Bon cinéma!")
                break
            
            self.answer_question(question, verbose=True)


# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Cinema Chatbot - French Movies')
    parser.add_argument('--question', type=str, help='Ask a single question')
    
    args = parser.parse_args()
    
    # Create chatbot
    chatbot = CinemaChatbot()
    
    # Single question or interactive mode
    if args.question:
        chatbot.answer_question(args.question, verbose=True)
    else:
        chatbot.chat()
