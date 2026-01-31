# cinema_sparql_generator.py
"""
Intelligent SPARQL Query Generator for Cinema Knowledge Graph
Generates queries dynamically using LLM
"""

import json
from typing import Dict, Any

class CinemaSPARQLGenerator:
    """Generate SPARQL queries for cinema knowledge graph using LLM"""
    
    def __init__(self, llm_client):
        """
        Initialize with LLM client
        
        Args:
            llm_client: LLM interface (local)
        """
        self.llm = llm_client
        self.namespace = "http://exemple.org/cinema#"
        
        # Load ontology structure
        self.ontology_summary = self._create_ontology_summary()
    
    def _create_ontology_summary(self):
        """
        Create a summary of the cinema ontology for the LLM
        """
        return """
# ONTOLOGIE CINÉMA - STRUCTURE

## Classes Principales:

### Film
- Description: Une œuvre cinématographique
- Propriétés:
  * titre (string): Le titre du film
  * annéeSortie (gYear): L'année de sortie (ex: 2001, 2011)
  * note (float): La note du film (ex: 8.3, 7.5)
  * durée (integer): Durée en minutes
  * synopsis (string): Description de l'intrigue

### Acteur
- Description: Une personne qui joue dans des films
- Propriétés:
  * nom (string): Le nom de l'acteur
  * annéeNaissance (gYear): Année de naissance
  * nationalité (string): Nationalité
  * récompenses (string): Récompenses remportées

### Actrice
- Description: Une actrice de cinéma
- Sous-classe de: Acteur

### Réalisateur
- Description: Une personne qui réalise des films
- Propriétés:
  * nom (string): Le nom du réalisateur
  * annéeNaissance (gYear): Année de naissance
  * nationalité (string): Nationalité
  * récompenses (string): Récompenses remportées

### RéalisateurActeur
- Description: Une personne qui est à la fois réalisateur et acteur
- Sous-classe de: Réalisateur ET Acteur
- Exemple: Mathieu Kassovitz

### Genre
- Description: Une catégorie de film
- Propriétés:
  * nom (string): Le nom du genre
  * description (string): Description du genre
- Exemples: Comédie, Drame, Romance, Action, Thriller

## Relations Principales:

### réaliséPar
- Domaine: Film
- Range: Réalisateur
- Description: Relie un film à son réalisateur
- Exemple: "Amélie Poulain" réaliséPar "Jean-Pierre Jeunet"

### avecActeur
- Domaine: Film
- Range: Acteur
- Description: Relie un film aux acteurs qui y jouent
- Exemple: "Intouchables" avecActeur "Omar Sy"

### genre
- Domaine: Film
- Range: Genre
- Description: Relie un film à son/ses genre(s)
- Exemple: "La Haine" genre "Drame"
- Note: Un film peut avoir plusieurs genres

## Exemples de Films dans le Graphe:
- "Le Fabuleux Destin d'Amélie Poulain" (2001) - Comédie, Romance
- "Intouchables" (2011) - Comédie, Drame
- "La Haine" (1995) - Drame
- "Les Petits Mouchoirs" (2010) - Comédie, Drame
- "La Vie d'Adèle" (2013) - Drame, Romance

## Exemples d'Acteurs:
- Audrey Tautou, Omar Sy, François Cluzet, Marion Cotillard, Vincent Cassel

## Exemples de Réalisateurs:
- Jean-Pierre Jeunet, Mathieu Kassovitz, Guillaume Canet

## Namespace:
PREFIX cinema: <http://exemple.org/cinema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

## NOTES IMPORTANTES:
1. Les années utilisent le type gYear (ex: "2001"^^xsd:gYear)
2. Un film peut avoir plusieurs réalisateurs (ex: Intouchables)
3. Un film peut avoir plusieurs genres
4. Les noms de propriétés sont en français (réaliséPar, avecActeur)
5. Mathieu Kassovitz est à la fois réalisateur ET acteur
"""
    
    def generate_sparql(self, question: str, language: str = "fr") -> Dict[str, Any]:
        """
        Generate SPARQL query from natural language question using LLM
        
        Args:
            question: User's question in natural language
            language: Language of the question (fr/en)
            
        Returns:
            Dictionary with:
                - sparql_query: Generated SPARQL query
                - entities_used: List of classes/entities used
                - relations_used: List of relations used
                - explanation: Explanation of the query
        """
        
        prompt = self._build_generation_prompt(question, language)
        
        # Get LLM response
        llm_response = self.llm.generate(prompt)
        
        # Parse the response
        result = self._parse_llm_response(llm_response)
        
        return result
    
    def _build_generation_prompt(self, question: str, language: str) -> str:
        """Build the prompt for LLM to generate SPARQL"""
        
        prompt = f"""Tu es un expert en génération de requêtes SPARQL pour une base de données cinéma.

{self.ontology_summary}

QUESTION DE L'UTILISATEUR: {question}

TÂCHE: Génère une requête SPARQL pour répondre à cette question.

INSTRUCTIONS:
1. Analyse la question pour identifier:
   - Quelles classes sont impliquées (Film, Acteur, Réalisateur, Genre)
   - Quelles propriétés sont nécessaires (titre, note, annéeSortie, nom, etc.)
   - Quelles relations sont utilisées (réaliséPar, avecActeur, genre)

2. Génère une requête SPARQL valide qui:
   - Utilise le préfixe cinema: <http://exemple.org/cinema#>
   - Sélectionne les bonnes variables
   - Inclut les filtres appropriés (ex: FILTER pour notes > X)
   - Est optimisée et claire
   - Utilise OPTIONAL pour propriétés facultatives

3. Réponds UNIQUEMENT avec un objet JSON valide dans ce format exact:
{{
  "sparql_query": "la requête SPARQL complète ici",
  "entities_used": ["liste des classes utilisées"],
  "relations_used": ["liste des relations utilisées"],
  "explanation": "explication brève de la requête en français"
}}

EXEMPLES DE REQUÊTES:

Exemple 1 - "Quels sont tous les films?"
{{
  "sparql_query": "PREFIX cinema: <http://exemple.org/cinema#>\\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\\n\\nSELECT ?film ?titre ?annee\\nWHERE {{\\n  ?film rdf:type cinema:Film .\\n  ?film cinema:titre ?titre .\\n  OPTIONAL {{ ?film cinema:annéeSortie ?annee . }}\\n}}",
  "entities_used": ["Film"],
  "relations_used": ["titre", "annéeSortie"],
  "explanation": "Récupère tous les films avec leur titre et année de sortie"
}}

Exemple 2 - "Qui a réalisé Amélie Poulain?"
{{
  "sparql_query": "PREFIX cinema: <http://exemple.org/cinema#>\\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\\n\\nSELECT ?realisateur ?nom\\nWHERE {{\\n  ?film rdf:type cinema:Film .\\n  ?film cinema:titre ?titre .\\n  FILTER(CONTAINS(LCASE(?titre), 'amélie'))\\n  ?film cinema:réaliséPar ?realisateur .\\n  ?realisateur cinema:nom ?nom .\\n}}",
  "entities_used": ["Film", "Réalisateur"],
  "relations_used": ["réaliséPar", "titre", "nom"],
  "explanation": "Trouve le réalisateur du film dont le titre contient 'amélie'"
}}

Exemple 3 - "Films avec Omar Sy"
{{
  "sparql_query": "PREFIX cinema: <http://exemple.org/cinema#>\\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\\n\\nSELECT ?film ?titre ?annee\\nWHERE {{\\n  ?acteur rdf:type cinema:Acteur .\\n  ?acteur cinema:nom ?nomActeur .\\n  FILTER(CONTAINS(LCASE(?nomActeur), 'omar sy'))\\n  ?film cinema:avecActeur ?acteur .\\n  ?film cinema:titre ?titre .\\n  OPTIONAL {{ ?film cinema:annéeSortie ?annee . }}\\n}}",
  "entities_used": ["Film", "Acteur"],
  "relations_used": ["avecActeur", "titre", "nom"],
  "explanation": "Trouve les films dans lesquels joue l'acteur Omar Sy"
}}

IMPORTANT: 
- Ne génère QUE le JSON, rien d'autre
- Pas de texte avant ou après le JSON
- Pas de markdown, pas de ```json```
- Utilise OPTIONAL pour les propriétés qui peuvent ne pas exister
- Utilise FILTER avec CONTAINS et LCASE pour recherche de texte
- Limite avec LIMIT si nécessaire
"""
        
        return prompt
    
    def _parse_llm_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM response to extract SPARQL query and metadata"""
        try:
            # Clean up response
            cleaned = llm_response.strip()
            
            # Remove markdown code blocks if present
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            result = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ["sparql_query", "entities_used", "relations_used", "explanation"]
            for field in required_fields:
                if field not in result:
                    result[field] = ""
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Raw response: {llm_response[:500]}")
            
            # Fallback: extract SPARQL manually
            return {
                "sparql_query": self._extract_sparql_fallback(llm_response),
                "entities_used": [],
                "relations_used": [],
                "explanation": "Query extracted from unstructured response"
            }
    
    def _extract_sparql_fallback(self, text: str) -> str:
        """Fallback method to extract SPARQL if JSON parsing fails"""
        import re
        
        # Try to find SPARQL query in the text
        patterns = [
            r'(PREFIX.*?SELECT.*?WHERE\s*\{.*?\})',
            r'(SELECT.*?WHERE\s*\{.*?\})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no pattern found, return basic query
        return """
        PREFIX cinema: <http://exemple.org/cinema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        
        SELECT ?subject ?predicate ?object
        WHERE {
          ?subject ?predicate ?object .
          FILTER(STRSTARTS(STR(?subject), "http://exemple.org/cinema#"))
        }
        LIMIT 10
        """


# Test
if __name__ == "__main__":
    print("Cinema SPARQL Generator loaded")
    print("Configured for French cinema database")
