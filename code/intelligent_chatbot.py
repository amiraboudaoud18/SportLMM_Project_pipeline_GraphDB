# intelligent_chatbot.py
"""
Intelligent Equestrian Chatbot - Main Orchestrator
Updated to use specialized LLMs for different tasks
"""

import sys
from graphdb_client import GraphDBClient
from intelligent_sparql_generator import IntelligentSPARQLGenerator
from llm_client import get_sparql_llm, get_answer_llm
from context_builder import ContextBuilder
from config import GRAPHDB_ENDPOINT, VERBOSE, SHOW_SPARQL, SHOW_CONTEXT, get_active_models


class IntelligentEquestrianChatbot:
    """
    Main chatbot orchestrating the complete GraphRAG pipeline
    Uses specialized LLMs for SPARQL generation and answer generation
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
        print(f"   Repository: {graphdb_endpoint.split('/')[-1]}")
        print(f"   Langue: {language.upper()}")
        
        # Show model configuration
        models = get_active_models()
        if models['using_specialized']:
            print("\nConfiguration: Modèles spécialisés")
            print(f"   SPARQL: {models['sparql_model']}")
            print(f"   Answer: {models['answer_model']}")
        else:
            print("\n  Configuration: Modèle unique")
            print(f"   Model: {models['sparql_model']}")
        
        self.language = language
        
        # Initialize all components with specialized LLMs
        try:
            self.graphdb = GraphDBClient(graphdb_endpoint)
            
            # Get specialized LLMs
            self.sparql_llm = get_sparql_llm()  # Code-specialized (Qwen2.5-Coder)
            self.answer_llm = get_answer_llm()  # Language model (Mistral/Vigogne)
            
            # Initialize components with appropriate LLMs
            self.sparql_generator = IntelligentSPARQLGenerator(self.sparql_llm)
            self.context_builder = ContextBuilder()
            
            print("\nChatbot initialisé!\n")
        except Exception as e:
            print(f"\nErreur lors de l'initialisation: {e}")
            raise
    
    def answer_question(self, question: str, verbose: bool = VERBOSE) -> dict:
        """
        Answer a question about horses using specialized LLMs
        
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
        
        # ====================================================================
        # STEP 1: Generate SPARQL query using CODE-SPECIALIZED LLM
        # ====================================================================
        if verbose:
            print("ÉTAPE 1: Génération de la requête SPARQL (modèle code-spécialisé)...")
        
        try:
            query_result = self.sparql_generator.generate_sparql(question, self.language)
            sparql_query = query_result["sparql_query"]
            entities_used = query_result["entities_used"]
            relations_used = query_result["relations_used"]
            explanation = query_result["explanation"]
            
            if verbose:
                print(" Requête générée!\n")
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
        
        # ====================================================================
        # STEP 2: Execute SPARQL on GraphDB
        # ====================================================================
        if verbose:
            print("ÉTAPE 2: Exécution de la requête sur GraphDB...")
        
        try:
            results = self.graphdb.query(sparql_query)
            
            if not results or 'results' not in results:
                if verbose:
                    print("Aucun résultat retourné par GraphDB\n")
                return {
                    "success": False,
                    "error": "Pas de résultats de GraphDB",
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
            
            if "400" in str(e) or "Bad Request" in str(e):
                print("\n Suggestions:")
                print("   - Vérifiez que la requête SPARQL est syntaxiquement correcte")
                print("   - Vérifiez que le namespace correspond à celui de GraphDB")
                print("   - Testez la requête manuellement dans GraphDB web interface")
            
            return {
                "success": False,
                "error": error_msg,
                "question": question,
                "sparql_query": sparql_query
            }
        
        # ====================================================================
        # STEP 3: Build context from results
        # ====================================================================
        if verbose:
            print("ÉTAPE 3: Construction du contexte...")
        
        try:
            context = self.context_builder.format_results(bindings, explanation)
            
            if verbose:
                print(f"Contexte créé ({len(context)} caractères)\n")
                
                if SHOW_CONTEXT and results_count > 0:
                    print("Aperçu du contexte:")
                    print("-" * 80)
                    preview = context[:500]
                    print(preview)
                    if len(context) > 500:
                        print("...")
                    print("-" * 80)
                    print()
        
        except Exception as e:
            error_msg = f"Erreur construction contexte: {str(e)}"
            print(f"{error_msg}")
            context = str(bindings)
        
        # ====================================================================
        # STEP 4: Generate natural language answer using LANGUAGE LLM
        # ====================================================================
        if verbose:
            print("ÉTAPE 4: Génération de la réponse (modèle langage)...")
        
        try:
            answer = self._generate_answer(question, context, results_count, bindings)
            
            if verbose:
                print("Réponse générée!\n")
        
        except Exception as e:
            error_msg = f"Erreur génération réponse: {str(e)}"
            print(f"{error_msg}")
            if results_count > 0:
                answer = f"J'ai trouvé {results_count} résultat(s), mais je n'ai pas pu générer une réponse naturelle. Voici les données brutes: {context[:200]}..."
            else:
                answer = "Je n'ai pas trouvé de résultats pour cette question."
        
        # ====================================================================
        # STEP 5: Display final answer
        # ====================================================================
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
    
    def _generate_answer(self, question: str, context: str, results_count: int, bindings: list) -> str:
        """
        Generate natural language answer using LANGUAGE-SPECIALIZED LLM
        
        Args:
            question: Original question
            context: Formatted context from SPARQL results
            results_count: Number of results found
            bindings: Raw SPARQL bindings
            
        Returns:
            Natural language answer in French
        """
        
        # Enhanced system prompt for French answer generation
        system_prompt = """Tu es un assistant expert en données équestres.
Tu réponds aux questions en te basant UNIQUEMENT sur le contexte fourni par le graphe de connaissances.
Tu réponds en français, de manière claire, précise et naturelle.

RÈGLES IMPORTANTES:
1. Utilise les informations de TYPE pour donner des réponses plus compréhensibles
   - Si tu vois "ShowJumping", dis "saut d'obstacles" ou "CSO"
   - Si tu vois "Dressage", dis "dressage"
   - Si tu vois "Cross", dis "cross-country" ou "CCE"
   - Si tu vois "PreCompetitionStage", dis "phase de pré-compétition"

2. Privilégie les noms FRANÇAIS et LISIBLES plutôt que les URIs
   - Mauvais: "Dakota participe à Event_SJ_2026_01"
   - Bon: "Dakota participe à l'événement de saut d'obstacles (Event_SJ_2026_01)"

3. Structure tes réponses de façon claire avec:
   - Une phrase introductive
   - Une liste numérotée ou à puces si plusieurs éléments
   - Des détails pertinents entre parenthèses

4. Si l'information n'est pas dans le contexte, dis-le clairement
5. Ne jamais inventer d'informations"""
        
        # Build user prompt
        if results_count == 0:
            user_prompt = f"""Question: {question}

Contexte: Aucune donnée trouvée dans le graphe de connaissances.

Réponds poliment que tu n'as pas trouvé d'informations pour répondre à cette question.
Suggère que les données recherchées n'existent peut-être pas encore dans la base."""
        else:
            user_prompt = f"""Question: {question}

Contexte du graphe de connaissances ({results_count} résultats trouvés):
{context}

Réponds à la question en te basant uniquement sur ce contexte.
Sois précis, informatif et naturel. Structure ta réponse de manière claire."""
        
        # Generate answer using the LANGUAGE-SPECIALIZED LLM
        answer = self.answer_llm.generate(user_prompt, system_prompt)
        
        return answer
    
    def chat(self):
        """Interactive chat mode"""
        
        print("\n" + "="*80)
        print(" CHATBOT ÉQUESTRE INTELLIGENT - MODE INTERACTIF")
        print("="*80)
        print("\nPosez vos questions sur:")
        print("  • Les chevaux (Dakota)")
        print("  • Les entraînements et leur intensité")
        print("  • Les événements sportifs (ShowJumping, Dressage, Cross)")
        print("  • Les relations entre chevaux, entraînements et compétitions")
        print("\nExemples de questions:")
        print("  - Quels sont tous les chevaux?")
        print("  - Quel cheval participe à quels entraînements?")
        print("  - Quels entraînements ont une haute intensité?")
        print("  - Quelle est la fréquence d'entraînement?")
        print("  - Quels événements sont prévus?")
        print("\nCommandes:")
        print("  • 'quit', 'exit', 'quitter' pour terminer")
        print("  • 'help' pour voir les exemples")
        print("="*80)
        
        while True:
            try:
                question = input("\n Votre question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'quitter', 'bye', 'au revoir']:
                    print("\n Au revoir!")
                    break
                
                if question.lower() in ['help', 'aide', '?']:
                    print("\n Exemples de questions:")
                    print("  1. Quels sont tous les chevaux?")
                    print("  2. Quel cheval participe à quels entraînements?")
                    print("  3. Quels entraînements ont une intensité élevée?")
                    print("  4. Quelle est la fréquence des entraînements?")
                    print("  5. Quels événements sportifs existent?")
                    print("  6. Quels entraînements dépendent de quel événement?")
                    continue
                
                # Answer the question
                self.answer_question(question, verbose=True)
                
            except KeyboardInterrupt:
                print("\n\n Au revoir!")
                break
            except Exception as e:
                print(f"\n Erreur: {e}")
                import traceback
                traceback.print_exc()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Chatbot Équestre Intelligent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python intelligent_chatbot.py
      → Mode interactif
  
  python intelligent_chatbot.py --question "Quels sont tous les chevaux?"
      → Question unique avec affichage détaillé
  
  python intelligent_chatbot.py --question "Quelle est la fréquence?" --quiet
      → Question unique en mode silencieux
        """
    )
    
    parser.add_argument(
        '--question',
        type=str,
        help='Poser une seule question (au lieu du mode interactif)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Mode silencieux (pas de détails, juste la réponse)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Mode debug (affiche la réponse brute du LLM)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create chatbot
        chatbot = IntelligentEquestrianChatbot()
        
        # Single question or interactive mode
        if args.question:
            verbose = not args.quiet
            result = chatbot.answer_question(args.question, verbose=verbose)
            
            # In quiet mode, just print the answer
            if args.quiet and result.get('success'):
                print(result['answer'])
            elif not result.get('success'):
                print(f" Erreur: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        else:
            # Interactive chat mode
            chatbot.chat()
    
    except KeyboardInterrupt:
        print("\n\n Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
