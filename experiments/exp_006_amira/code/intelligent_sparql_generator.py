# intelligent_sparql_generator.py
"""
Intelligent SPARQL Generator - Equestrian Knowledge Graph
"""


import json
import re
from typing import Dict, Any
from config import ONTOLOGY_NAMESPACE, get_sparql_prefixes

class IntelligentSPARQLGenerator:
    """Generates SPARQL queries using LLM intelligence and ontology awareness"""
    
    def __init__(self, llm_client):
        """
        Initialize SPARQL generator
        
        Args:
            llm_client: LLM client for generating queries
        """
        self.llm = llm_client
        self.namespace = ONTOLOGY_NAMESPACE
        
        # Create detailed ontology summary
        self.ontology_summary = self._create_ontology_summary()
    
    def _create_ontology_summary(self):
        """
        Create comprehensive ontology summary for LLM
        V2.0: Added correct relationship directions and sensor position handling
        """
        return f"""
# ONTOLOGIE ÉQUESTRE - STRUCTURE COMPLÈTE V2.0

## NAMESPACE:
{self.namespace}

## RÈGLES CRITIQUES - DIRECTIONS DES RELATIONS:

### 1. Riders → Horses (PAS l'inverse!)
```sparql
# CORRECT:
?rider rdf:type horses:Rider .
?rider horses:AssociatedWith ?horse .

# FAUX:
?horse horses:AssociatedWith ?rider
```

### 2. Sensors → Horses (PAS l'inverse!)
```sparql
# CORRECT:
?sensor horses:isAttachedTo ?horse .

# FAUX:
?horse horses:isAttachedTo ?sensor
```

### 3. Training → Actors (relation spéciale!)
```sparql
# CORRECT (actors impliqués dans training):
?training horses:involvesActor ?actor .
?actor rdf:type horses:Rider .  # ou Veterinarian, Caretaker

# FAUX:
?horse horses:hasVeterinarian ?vet  # Cette propriété n'existe pas!
```

### 4. Positions de capteurs = TYPES (pas propriétés!)
```sparql
# CORRECT:
?sensor rdf:type horses:Withers .  # ou CanonOfForelimb, Sternum, etc.

# FAUX:
?sensor horses:hasPosition horses:Withers
?sensor horses:hasSensorID ?position  # hasSensorID donne l'ID, pas la position!
```

### 5. Fréquence d'échantillonnage des capteurs
```sparql
# ORRECT:
?sensor horses:hasSensorTime ?frequency .  # Returns "200Hz", "250Hz"

# FAUX:
?sensor horses:Frequency ?frequency  # Frequency est pour Training, pas Sensors!
```

## CLASSES PRINCIPALES:

### 1. Horse (Cheval)
Propriétés:
  - hasName (string) : Nom du cheval (ex: "Dakota", "Naya")
  - hasRace (string) : Race du cheval (ex: "Selle Français", "Anglo-Arabe")
  - hasPuce (integer) : Numéro de puce électronique
  - hasRobe (string) : Couleur de la robe
  - hasHeight (float) : Taille du cheval

Relations SORTANTES (Horse est le sujet):
  - CompetesIn → SportingEvent
  - TrainsIn → Training

Relations ENTRANTES (Horse est l'objet):
  - Rider AssociatedWith → Horse
  - Sensor isAttachedTo → Horse

### 2. Rider (Cavalier)
IMPORTANT: Les riders n'ont souvent PAS de propriété hasName!
L'identifiant est dans l'URI: Rider_Emma, Rider_Leo, Rider_Manon

Relations:
  - Rider AssociatedWith → Horse (Rider est le sujet!)
  - Training involvesActor → Rider

### 3. Human (Acteurs humains)
Sous-classes:
  - Rider : Cavaliers
  - Veterinarian : Vétérinaires (ex: Vet_DrMartin)
  - Caretaker : Soigneurs (ex: Caretaker_Sophie)

IMPORTANT - Acteurs SANS hasName:
- Riders: PAS de hasName property!
- Veterinarian: PAS de hasName property!
- Caretaker: PAS de hasName property!

Solution: Sélectionner l'URI directement (?rider, ?actor)
Le nom est dans l'URI: Rider_Emma → "Emma", Vet_DrMartin → "Dr Martin"

Relations:
  - Training involvesActor → Human (de tous types)

### 4. Training (Entraînement)
Sous-classes:
  - PreparationStage : Préparation
  - PreCompetitionStage : Pré-compétition
  - CompetitionStage : Compétition
  - TransitionStage : Transition

Propriétés:
  - Frequency (integer) : Fréquence (ex: 4)
  - Intensity (string) : "Moderate", "High", "Peak", "Low", "Modérée", "Élevée"
  - Volume (string) : Durée (ex: "45min", "60min")

Relations:
  - dependsOn → SportingEvent
  - involvesActor → Human (Rider, Veterinarian, Caretaker)

### 5. SportingEvent (Événement sportif)
Sous-classes:
  - ShowJumping (Saut d'obstacles)
  - Dressage (Dressage)
  - Cross (Cross-country)

Propriétés:
  - eventDate (date) : Date de l'événement
  - eventLocation (string) : Lieu
  - category (string) : Catégorie (ex: "Amateur 1", "Club Elite")

Relations:
  - inSeason → CompetitiveSeason
  - hasParticipation → EventParticipation

### 6. CompetitiveSeason (Saison)
Exemple: Season_2026

Propriétés:
  - seasonName (string) : "Saison 2026"
  - seasonStart (date) : Date de début
  - seasonEnd (date) : Date de fin

### 7. EventParticipation (Participation à un événement)
Propriétés:
  - rank (integer) : Classement

Relations:
  - hasHorse → Horse
  - hasRider → Rider

### 8. InertialSensors (Capteurs inertiels)
IMPORTANT: Chaque capteur a DEUX types:
1. horses:InertialSensors (classe de base)
2. Position anatomique (Withers, CanonOfForelimb, CanonOfHindlimb, Sternum)

Propriétés:
  - hasSensorID (string) : ID du capteur (ex: "IMU-W-001")
  - hasSensorTime (string) : Fréquence d'échantillonnage (ex: "200Hz", "250Hz")
  - hasFormat (string) : Format (ex: "CSV")
  - hasFileSize (integer) : Taille du fichier
  - hasSensorOffset (string) : Offset

Relations:
  - isAttachedTo → Horse
  - isUsedFor → ExperimentalObjective

Positions anatomiques (ce sont des TYPES):
  - Withers (garrot)
  - CanonOfForelimb (canon antérieur)
  - CanonOfHindlimb (canon postérieur)
  - Sternum (sternum)

### 9. ExperimentalObjective (Objectifs expérimentaux)
Exemples:
  - GaitClassification (Classification de la démarche)
  - FatigueDetection (Détection de fatigue)
  - LamenessDetection (Détection de boiterie)

## EXEMPLES DE DONNÉES RÉELLES:

Chevaux:
  - Horse1: Dakota (Selle Français)
  - Horse2: Naya (Anglo-Arabe)

Cavaliers:
  - Rider_Emma AssociatedWith Horse1
  - Rider_Manon AssociatedWith Horse1
  - Rider_Leo AssociatedWith Horse2

Acteurs:
  - Vet_DrMartin (Vétérinaire)
  - Caretaker_Sophie (Soigneuse)

Entraînements:
  - Training_Prepa_SJ_01: Frequency=4, Intensity="Modérée", Volume="45min"
    → dependsOn Event_SJ_01
    → involvesActor Rider_Emma, Vet_DrMartin, Caretaker_Sophie
  
  - Training_PreComp_SJ_01: Frequency=3, Intensity="Élevée", Volume="60min"
    → dependsOn Event_SJ_01
    → involvesActor Rider_Manon, Caretaker_Sophie

Événements:
  - Event_SJ_01: type ShowJumping, date "2026-04-12", location "Saumur", category "Amateur 1"
    → inSeason Season_2026
  
  - Event_Dressage_01: type Dressage, date "2026-05-03", location "Angers", category "Club Elite"
    → inSeason Season_2026

Saison:
  - Season_2026: seasonStart "2026-03-01", seasonEnd "2026-10-31"

Capteurs (tous attachés à Horse1/Dakota):
  - IMU_Withers_01: hasSensorID "IMU-W-001", hasSensorTime "200Hz"
    → types: InertialSensors ET Withers
    → isUsedFor GaitClassif_01
  
  - IMU_CanonFore_01: hasSensorID "IMU-CF-002", hasSensorTime "250Hz"
    → types: InertialSensors ET CanonOfForelimb
    → isUsedFor FatigueDetection
  
  - IMU_CanonHind_01: hasSensorID "IMU-CH-003", hasSensorTime "250Hz"
    → types: InertialSensors ET CanonOfHindlimb
  
  - IMU_Sternum_01: hasSensorID "IMU-ST-004", hasSensorTime "200Hz"
    → types: InertialSensors ET Sternum

Participation:
  - Participation_SJ01_H1_Emma:
    → hasHorse Horse1
    → hasRider Rider_Emma
    → rank 2

## RÈGLES POUR GÉNÉRER DES REQUÊTES:

1. **Direction des relations** (TRÈS IMPORTANT!):
   - Rider → Horse (pas Horse → Rider)
   - Sensor → Horse (pas Horse → Sensor)
   - Training → Actor (pas Horse → Actor)

2. **Positions de capteurs**:
   - Utiliser rdf:type pour les positions
   - Filtrer la classe de base: FILTER(?position != horses:InertialSensors)

3. **Noms des acteurs**:
   - Extraire du nom de l'URI: Rider_Emma → "Emma"
   - Vet_DrMartin → "Dr Martin"
   - Caretaker_Sophie → "Sophie"

4. **Propriétés optionnelles**:
   - Toujours utiliser OPTIONAL pour propriétés qui peuvent manquer
   - Exemple: OPTIONAL {{ ?horse horses:hasRace ?race }}

5. **Pas de GRAPH**:
   - Ne jamais utiliser de clause GRAPH
   - Toutes les données sont dans le graphe par défaut

6. **Comptages**:
   - Utiliser COUNT(?variable) pour compter
   - Grouper avec GROUP BY si nécessaire

7. **Événements spécifiques**:
   - Pour un événement nommé (ex: Event_SJ_01), utiliser l'URI directement
   - horses:Event_SJ_01 horses:eventDate ?date
   - NE PAS chercher par hasName pour les événements!

8. **Catégorie d'événement**:
   - horses:category = niveau de compétition ("Amateur 1", "Club Elite")
   - Ce N'EST PAS le type d'événement (ShowJumping, Dressage)!

9. **Classements**:
   - Les classements sont sur EventParticipation, pas sur Horse
   - Utiliser hasParticipation, hasHorse, rank

10. **Capteurs spécifiques**:
    - Pour un capteur nommé (ex: IMU_Withers_01), utiliser l'URI directement
    - horses:IMU_Withers_01 horses:isUsedFor ?objective
    
11. **Acteurs sans hasName**:
   - Riders, Veterinarian, Caretaker n'ont PAS de hasName
   - Sélectionner ?rider (pas ?riderName), ?actor (pas ?actorName)
   - Le nom est dans l'URI et sera extrait automatiquement

"""
    
    def generate_sparql(self, question: str, language: str = "fr", debug: bool = False) -> Dict[str, Any]:
        """
        Generate SPARQL query from natural language question
        
        Args:
            question: User's question in natural language
            language: Language (fr/en)
            debug: If True, print raw LLM response
            
        Returns:
            Dict with sparql_query, entities_used, relations_used, explanation
        """
        # Build prompt with few-shot examples
        prompt = self._build_fewshot_prompt(question)
        
        # Get LLM response
        llm_response = self.llm.generate(prompt)
        
        if debug:
            print("="*80)
            print("RAW LLM RESPONSE:")
            print("="*80)
            print(llm_response)
            print("="*80)
        
        # Parse response
        result = self._parse_llm_response(llm_response)
        
        # Auto-correct V2 mistakes
        result = self._auto_correct_v2_queries(result)
        
        return result
    
    def _build_fewshot_prompt(self, question: str) -> str:
        """Build prompt with ontology summary and few-shot examples"""
        
        prompt = f"""{self.ontology_summary}

═══════════════════════════════════════════════════════════════
EXEMPLES DE REQUÊTES SPARQL
═══════════════════════════════════════════════════════════════

EXEMPLE 1 - Noms des chevaux:
Question: "Quels sont les noms des chevaux?"

Analyse:
- Classe: Horse
- Propriété: hasName

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?horseName
WHERE {{
  ?horse rdf:type horses:Horse .
  OPTIONAL {{ ?horse horses:hasName ?horseName . }}
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 2 - Cavaliers associés à un cheval (NO hasName!):
Question: "Quels cavaliers sont associés à Dakota?"

Analyse:
- Classes: Horse, Rider
- Relation: Rider AssociatedWith Horse (DIRECTION!)
- IMPORTANT: Riders N'ONT PAS de hasName property!
- Solution: Sélectionner ?rider directement (pas ?riderName)

SPARQL:
PREFIX horses: <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?rider
WHERE {{
  ?horse horses:hasName "Dakota" .
  ?rider rdf:type horses:Rider .
  ?rider horses:AssociatedWith ?horse .
}}

Résultat attendu: ?rider = Rider_Emma, Rider_Manon (extraire "Emma", "Manon" du nom)

═══════════════════════════════════════════════════════════════

EXEMPLE 3 - Date d'un événement (V2 PROPERTY!):
Question: "Quelle est la date de l'événement Event_SJ_01?"

Analyse:
- Classe: SportingEvent (ShowJumping)
- Propriété: eventDate (PAS hasDate!)
- IMPORTANT: Utiliser l'URI directement pour l'événement spécifique

SPARQL:
PREFIX horses: <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?date
WHERE {{
  horses:Event_SJ_01 horses:eventDate ?date .
}}


═══════════════════════════════════════════════════════════════

EXEMPLE 5 - Catégorie d'un événement (NIVEAU DE COMPÉTITION!):
Question: "Quelle est la catégorie de l'événement Event_SJ_01?"

Analyse:
- Classe: SportingEvent
- Propriété: category (niveau: "Amateur 1", "Club Elite", etc.)
- IMPORTANT: category = niveau de compétition, PAS le type d'événement!

SPARQL:
PREFIX horses: <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?category
WHERE {{
  horses:Event_SJ_01 horses:category ?category .
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 6 - Classement dans un événement (EVENTPARTICIPATION!):
Question: "Quel classement Dakota et Emma ont-ils obtenu à Event_SJ_01?"

Analyse:
- Classes: EventParticipation, Horse, Rider
- Relations: Event hasParticipation Participation
- Propriété: rank sur EventParticipation
- IMPORTANT: Le classement est sur EventParticipation, PAS sur Horse!

SPARQL:
PREFIX horses: <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?rank
WHERE {{
  horses:Event_SJ_01 horses:hasParticipation ?participation .
  ?participation horses:hasHorse ?horse .
  ?horse horses:hasName "Dakota" .
  ?participation horses:rank ?rank .
}}


═══════════════════════════════════════════════════════════════

EXEMPLE 3 - Vétérinaire et soigneurs:
Question: "Qui est le vétérinaire? Qui est le soigneur?"

Analyse:
- Classes: Veterinarian, Caretaker
- Relation: Training involvesActor → Human
- IMPORTANT: Pas de propriété hasVeterinarian! Utiliser involvesActor

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?actor ?actorType
WHERE {{
  ?training horses:involvesActor ?actor .
  ?actor rdf:type ?actorType .
  FILTER(?actorType = horses:Veterinarian || ?actorType = horses:Caretaker)
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 4 - Acteurs dans une phase d'entraînement:
Question: "Qui participe à la phase de préparation?"

Analyse:
- Classes: PreparationStage, Human
- Relation: Training involvesActor → Human

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?actor
WHERE {{
  ?training rdf:type horses:PreparationStage .
  ?training horses:involvesActor ?actor .
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 5 - Positions anatomiques des capteurs:
Question: "À quelles positions sont placés les capteurs IMU?"

Analyse:
- Classe: InertialSensors
- IMPORTANT: La position est un TYPE, pas une propriété!
- Chaque capteur a 2 types: InertialSensors ET sa position

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?sensor ?sensorID ?position
WHERE {{
  ?sensor rdf:type horses:InertialSensors .
  ?sensor horses:hasSensorID ?sensorID .
  ?sensor rdf:type ?position .
  FILTER(?position != horses:InertialSensors)
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 6 - Capteur à une position spécifique:
Question: "Quel est l'identifiant du capteur au garrot?"

Analyse:
- Type: Withers (garrot)
- Propriété: hasSensorID

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?sensorID
WHERE {{
  ?sensor rdf:type horses:Withers .
  ?sensor horses:hasSensorID ?sensorID .
}}

═══════════════════════════════════════════════════════════════

EXEMPLE 7 - Fréquence d'échantillonnage d'un capteur:
Question: "Quelle est la fréquence d'échantillonnage du capteur au sternum?"

Analyse:
- Type: Sternum
- Propriété: hasSensorTime (PAS Frequency!)

SPARQL:
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?frequency
WHERE {{
  ?sensor rdf:type horses:Sternum .
  ?sensor horses:hasSensorTime ?frequency .
}}



═══════════════════════════════════════════════════════════════

MAINTENANT, génère une requête SPARQL pour: "{question}"

ANALYSE:
- Quelles classes sont nécessaires?
- Quelles propriétés?
- Quelles relations? (ATTENTION AUX DIRECTIONS!)
- Quels filtres?

RAPPELS CRITIQUES:
1. Rider AssociatedWith Horse (pas l'inverse!)
2. Sensor isAttachedTo Horse (pas l'inverse!)
3. Training involvesActor Actor (pas Horse!)
4. Position de capteur = rdf:type (pas propriété!)
5. Fréquence de capteur = hasSensorTime (pas Frequency!)

Réponds UNIQUEMENT avec un objet JSON valide (PAS de texte avant ou après, PAS de ```json):

{{
  "sparql_query": "PREFIX horses: <{self.namespace}>\\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\\n\\nSELECT ?variable\\nWHERE {{\\n  ?variable rdf:type horses:ClassName .\\n}}",
  "entities_used": ["Horse", "Training"],
  "relations_used": ["TrainsIn", "hasName"],
  "explanation": "Explication courte en français de ce que fait la requête"
}}

RÈGLES JSON:
- NE génère QUE le JSON, rien d'autre
- Utilise \\n pour les retours à ligne
- Utilise {{{{ et }}}} pour les accolades dans SPARQL
- Le JSON doit être parsable directement
- RAPPEL: PAS de clause GRAPH dans la requête!
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
            
            # Unescape newlines and tabs
            if "sparql_query" in result and isinstance(result["sparql_query"], str):
                result["sparql_query"] = result["sparql_query"].replace("\\n", "\n")
                result["sparql_query"] = result["sparql_query"].replace("\\t", "\t")
            
            # Validate required fields
            if "sparql_query" not in result or not result["sparql_query"].strip():
                print("Pas de requête SPARQL dans JSON, extraction manuelle...")
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
            return {
                "sparql_query": self._extract_sparql_fallback(llm_response),
                "entities_used": [],
                "relations_used": [],
                "explanation": "Requête extraite (JSON invalide)"
            }
    
    
    def _auto_correct_v2_queries(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Auto-correct common V2 property mistakes
        This prevents queries from using old property names
        """
        sparql_query = result.get('sparql_query', '')
        
        # V2 Event property corrections
        corrections = [
            ('horses:hasDate', 'horses:eventDate'),
            ('horses:hasLocation', 'horses:eventLocation'),
            ('?horse horses:AssociatedWith ?rider', '?rider horses:AssociatedWith ?horse'),
            ('?horse horses:isAttachedTo ?sensor', '?sensor horses:isAttachedTo ?horse'),
            ('horses:hasRanking', 'horses:rank'),
        ]
        
        corrected = False
        for old, new in corrections:
            if old in sparql_query:
                sparql_query = sparql_query.replace(old, new)
                corrected = True
        
        if corrected:
            result['sparql_query'] = sparql_query
            result['auto_corrected'] = True
        
        return result


    def _extract_sparql_fallback(self, text: str) -> str:
        """Extract SPARQL from unstructured text as fallback"""
        # Try to find SPARQL pattern
        patterns = [
            r'(PREFIX.*?SELECT.*?WHERE\s*\{.*?\})',
            r'(SELECT.*?WHERE\s*\{.*?\})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                query = match.group(1).strip()
                # Unescape if needed
                query = query.replace("\\n", "\n").replace("\\t", "\t")
                return query
        
        # Return basic fallback query
        return f"""
PREFIX horses: <{self.namespace}>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?subject ?predicate ?object
WHERE {{
  ?subject ?predicate ?object .
}}
LIMIT 10
"""


if __name__ == "__main__":
    print("Intelligent SPARQL Generator V2.0 loaded")
    print(f"   Namespace: {ONTOLOGY_NAMESPACE}")
    print("   Features: Dynamic relationship learning, 10 examples, No overfitting")
    print("   Improvements: Correct relationship directions, sensor positions as types")