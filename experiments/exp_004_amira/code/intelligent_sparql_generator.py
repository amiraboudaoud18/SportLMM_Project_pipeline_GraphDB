# intelligent_sparql_generator.py
"""
Intelligent SPARQL Generator - Uses LLM to generate SPARQL queries
"""

import json
import re
from typing import Dict, Any
from config import ONTOLOGY_NAMESPACE, INSTANCES_GRAPH, get_sparql_prefixes


class IntelligentSPARQLGenerator:
    """Generates SPARQL queries using LLM intelligence"""
    
    def __init__(self, llm_client):
        """
        Initialize SPARQL generator
        
        Args:
            llm_client: LLM client for generating queries
        """
        self.llm = llm_client
        self.namespace = ONTOLOGY_NAMESPACE
        self.instances_graph = INSTANCES_GRAPH
        
        # Create ontology summary
        self.ontology_summary = self._create_ontology_summary()
    
    def _create_ontology_summary(self):
        """Create ontology summary for LLM"""
        return f"""
# ONTOLOGIE ÉQUESTRE - STRUCTURE

## Classes Principales:

### Horse (Cheval)
- Propriétés: hasName, hasRace, hasHeight, hasWeight, hasPuce, hasSire, hasRobe
- Description: Représente un cheval dans le système

### Rider (Cavalier)
- Propriétés: hasName
- Description: Représente un cavalier

### Training (Entraînement)
- Sous-classes: PreparationStage, CompetitionStage, PreCompetitionStage, TransitionStage
- Propriétés: hasDate, hasLocation, Frequency, Intensity
- Description: Séances d'entraînement

### ExperimentalDevices (Dispositifs expérimentaux)
- Sous-classes: InertialSensors, Camera, Video, Images
- Propriétés: hasSensorID, hasSensorTime, hasVideofile
- Description: Capteurs et dispositifs de mesure

### SportingEvent (Événement sportif)
- Sous-classes: ShowJumping (CSO), Cross (CCO), Dressage
- Propriétés: hasDate, hasLocation, hasName
- Description: Compétitions et événements

### Studies (Études)
- Sous-classes: BienetreSaumur, HappyAthlete, CognitionEquine, etc.
- Description: Projets de recherche

### IndicateurPerformance
- Sous-classes: FacteurPhysique, FacteurMental, FacteurTechnique
- Description: Indicateurs de performance

### IndicateurBienetre
- Sous-classes: Alimentation, Comportement, Hebergement, HealthStatus
- Description: Indicateurs de bien-être

## Relations Principales:

### hasParticipatedTo
- Domaine: Horse
- Range: Training/Study/SportingEvent
- Description: Cheval participe à un entraînement/étude/événement
- Exemple: Thunder hasParticipatedTo DressageTraining

### AssociatedWith
- Domaine: Horse ↔ Rider
- Description: Couplage cheval-cavalier
- Exemple: Thunder AssociatedWith JohnSmith

### isAttachedTo
- Domaine: Horse → Sensor
- Description: Capteur attaché au cheval
- Exemple: Thunder isAttachedTo Sensor123

### isUsedFor
- Domaine: Device → Project
- Description: Dispositif utilisé pour un projet
- Exemple: Camera123 isUsedFor BienetreSaumur

### CompetesIn
- Domaine: Horse → SportingEvent
- Description: Cheval participe à un événement sportif

### TrainsIn
- Domaine: Horse → Training
- Description: Cheval s'entraîne

## IMPORTANT:
- Namespace: {self.namespace}
- Les données sont dans le named graph: {self.instances_graph}
- TOUJOURS utiliser: GRAPH <{self.instances_graph}> {{ ... }}
"""
    
    def generate_sparql(self, question: str, language: str = "fr", debug: bool = False) -> Dict[str, Any]:
        """
        Generate SPARQL query from natural language question
        
        Args:
            question: User's question
            language: Language (fr/en)
            debug: If True, print raw LLM response
            
        Returns:
            Dictionary with sparql_query, entities_used, relations_used, explanation
        """
        prompt = self._build_generation_prompt(question, language)
        llm_response = self.llm.generate(prompt)
        
        # Debug: show raw response
        if debug:
            print("\n🔍 DEBUG - Réponse brute du LLM:")
            print("=" * 80)
            print(llm_response[:500])
            print("=" * 80)
        
        result = self._parse_llm_response(llm_response)
        
        return result
    
    def _build_generation_prompt(self, question: str, language: str) -> str:
        """Build prompt for LLM to generate SPARQL"""
        
        prefixes = get_sparql_prefixes()
        
        prompt = f"""Tu es un expert en génération de requêtes SPARQL pour une ontologie équestre.

{self.ontology_summary}

QUESTION DE L'UTILISATEUR: {question}

TÂCHE: Génère une requête SPARQL pour répondre à cette question.

INSTRUCTIONS CRITIQUES:
1. TOUJOURS utiliser: GRAPH <{self.instances_graph}> {{ ... }}
2. Utiliser les préfixes:{prefixes}
3. Utiliser OPTIONAL pour les propriétés qui peuvent ne pas exister
4. Utiliser FILTER pour les conditions (ex: intensité > X)

EXEMPLES FEW-SHOT (Apprends de ces exemples):

EXEMPLE 1:
Question: "Quel cheval a participé à quelle séance d'entraînement?"
SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?horse ?horseName ?training
WHERE {{
    GRAPH <{self.instances_graph}> {{
        ?horse rdf:type horses:Horse .
        ?horse horses:hasParticipatedTo ?training .
        ?training rdf:type horses:Training .
        OPTIONAL {{ ?horse horses:hasName ?horseName . }}
    }}
}}

EXEMPLE 2:
Question: "Quelles séances d'entraînement ont inclus des exercices de haute intensité?"
SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?training ?intensity
WHERE {{
    GRAPH <{self.instances_graph}> {{
        ?training rdf:type horses:Training .
        ?training horses:Intensity ?intensity .
        FILTER(?intensity > 7)
    }}
}}

EXEMPLE 3:
Question: "Quels sont les différents couplages cheval/cavalier?"
SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?horse ?horseName ?rider ?riderName
WHERE {{
    GRAPH <{self.instances_graph}> {{
        ?horse rdf:type horses:Horse .
        ?rider rdf:type horses:Rider .
        ?horse horses:AssociatedWith ?rider .
        OPTIONAL {{ ?horse horses:hasName ?horseName . }}
        OPTIONAL {{ ?rider horses:hasName ?riderName . }}
    }}
}}

EXEMPLE 4:
Question: "Quel est la race du cheval?"
SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?horse ?horseName ?race
WHERE {{
    GRAPH <{self.instances_graph}> {{
        ?horse rdf:type horses:Horse .
        OPTIONAL {{ ?horse horses:hasName ?horseName . }}
        OPTIONAL {{ ?horse horses:hasRace ?race . }}
    }}
}}

MAINTENANT, génère une requête SPARQL pour: "{question}"

Réponds UNIQUEMENT avec un objet JSON valide dans ce format EXACT (pas de texte avant ou après):

{{
  "sparql_query": "PREFIX horses: <{self.namespace}>\\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\\n\\nSELECT ?horse ?name\\nWHERE {{\\n  GRAPH <{self.instances_graph}> {{\\n    ?horse rdf:type horses:Horse .\\n  }}\\n}}",
  "entities_used": ["Horse"],
  "relations_used": ["hasName"],
  "explanation": "Description en français"
}}

RÈGLES CRITIQUES:
- NE génère QUE le JSON, absolument rien d'autre
- PAS de texte avant le JSON (pas de "Voici la requête...")
- PAS de texte après le JSON
- PAS de balises markdown (pas de ```json ou ```)
- Utilise \\n pour les retours à ligne dans la requête SPARQL
- Échappe les accolades dans WHERE avec {{
- Le JSON doit être parsable directement
"""
        
        return prompt
    
    def _parse_llm_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM response to extract SPARQL"""
        try:
            # Clean response
            cleaned = llm_response.strip()
            
            # Remove markdown if present
            if "```json" in cleaned:
                cleaned = cleaned.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            result = json.loads(cleaned)
            
            # IMPORTANT: Unescape the SPARQL query
            # The LLM might return \n as literal string instead of newlines
            if "sparql_query" in result and isinstance(result["sparql_query"], str):
                # Replace escaped newlines with actual newlines
                result["sparql_query"] = result["sparql_query"].replace("\\n", "\n")
                result["sparql_query"] = result["sparql_query"].replace("\\t", "\t")
            
            # Validate
            if "sparql_query" not in result or not result["sparql_query"].strip():
                print(" Pas de requête SPARQL dans la réponse JSON, extraction manuelle...")
                result["sparql_query"] = self._extract_sparql_fallback(llm_response)
            
            if "entities_used" not in result:
                result["entities_used"] = []
            
            if "relations_used" not in result:
                result["relations_used"] = []
    
            if "explanation" not in result:
                result["explanation"] = "Requête générée"
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Erreur parsing JSON: {e}")
            print("Extraction manuelle de la requête SPARQL...")
            # Fallback: try to extract SPARQL manually
            return {
                "sparql_query": self._extract_sparql_fallback(llm_response),
                "entities_used": [],
                "relations_used": [],
                "explanation": "Requête extraite"
            }
    
    def _extract_sparql_fallback(self, text: str) -> str:
        """Extract SPARQL from unstructured text"""
        # Try to find SPARQL pattern
        patterns = [
            r'(PREFIX.*?SELECT.*?WHERE\s*\{.*?\})',
            r'(SELECT.*?WHERE\s*\{.*?\})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Return basic query
        return f"""
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?subject ?predicate ?object
WHERE {{
    GRAPH <{self.instances_graph}> {{
        ?subject ?predicate ?object .
    }}
}}
LIMIT 10
"""


if __name__ == "__main__":
    print(" Intelligent SPARQL Generator loaded")
