# CINEMA CHATBOT - ARCHITECTURE ET FONCTIONNEMENT
## Système GraphRAG pour Base de Données Cinéma

---

## 🎬 VUE D'ENSEMBLE

Le Cinema Chatbot est un système **GraphRAG (Graph-based Retrieval Augmented Generation)** qui permet de poser des questions en langage naturel sur une base de données de films français.

### Principe de Fonctionnement

```
Question (français naturel)
        ↓
    LLM génère SPARQL
        ↓
    Exécution sur GraphDB
        ↓
    Formatage des résultats
        ↓
    LLM génère réponse (français naturel)
```

**Avantage clé:** Pas de règles hardcodées - le LLM génère dynamiquement les requêtes SPARQL!

---

## 📁 ARCHITECTURE DES FICHIERS

### Vue d'ensemble

```
cinema-chatbot/
├── .env                           # Configuration environnement
├── config_cinema.py               # Chargeur de configuration
├── llm_client.py                  # Communication avec LLM
├── graphdb_client.py              # Communication avec GraphDB
├── context_builder.py             # Formatage des résultats
├── cinema_sparql_generator.py     # Génération SPARQL (CERVEAU)
└── cinema_chatbot.py              # Orchestrateur principal
```

---

## 🔧 FICHIER PAR FICHIER

### 1. `.env` - Variables d'Environnement

**Rôle:** Stocke tous les paramètres de configuration

**Contenu:**
```bash
# LLM Configuration
LOCAL_LLM_MODEL=Meta-Llama-3.1-8B-Instruct-GGUF
LOCAL_LLM_ENDPOINT=http://localhost:1234/v1

# GraphDB Configuration
GRAPHDB_ENDPOINT=http://localhost:7200/repositories/movie-test

# Ontology
ONTOLOGY_NAMESPACE=http://exemple.org/cinema#
```

**Pourquoi ce fichier existe:**
- ✅ Sépare configuration et code
- ✅ Facile à modifier sans toucher au code
- ✅ Différentes configs pour dev/test/prod

**Quand le modifier:**
- Changer de modèle LLM
- Changer d'endpoint GraphDB
- Changer de repository

---

### 2. `config_cinema.py` - Gestionnaire de Configuration

**Rôle:** Charge les variables d'.env et les fournit aux autres modules

**Code clé:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Charge depuis .env
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "default-value")
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT", "default-endpoint")

def validate_config():
    """Vérifie que tout est configuré correctement"""
    # Vérifie endpoints, variables, etc.
```

**Ce qu'il fait:**
1. Lit le fichier `.env`
2. Charge les variables en Python
3. Fournit des valeurs par défaut si manquantes
4. Valide la configuration au démarrage

**Utilisé par:** TOUS les autres fichiers importent depuis ici

**Exemple d'utilisation:**
```python
# Dans cinema_chatbot.py
from config_cinema import GRAPHDB_ENDPOINT, LOCAL_LLM_MODEL

client = GraphDBClient(GRAPHDB_ENDPOINT)
```

**Tester:**
```bash
python config_cinema.py
# Affiche toute la configuration
```

---

### 3. `llm_client.py` - Client LLM

**Rôle:** Gère TOUTE la communication avec le LLM (LM Studio)

**Architecture:**
```python
class LLMClient:
    """Client de base pour n'importe quel LLM"""
    
    def generate(prompt, system_prompt):
        """Envoie prompt → Reçoit réponse"""
        # 1. Construit messages
        # 2. Envoie HTTP POST à LM Studio
        # 3. Parse la réponse JSON
        # 4. Retourne le texte généré

class FrenchLLMClient(LLMClient):
    """Version optimisée pour français"""
    # Ajoute contexte système en français
```

**Comment ça marche:**
```python
# Utilisation simple
llm = FrenchLLMClient()
response = llm.generate(
    prompt="Génère une requête SPARQL...",
    system_prompt="Tu es un expert SPARQL..."
)
# response = "PREFIX cinema: <...> SELECT ..."
```

**Fonctionnalités:**
- ✅ Gère connexion à LM Studio (port 1234)
- ✅ Retry automatique si échec
- ✅ Timeout après X secondes
- ✅ Messages d'erreur en français
- ✅ Optimisé pour réponses françaises

**Utilisé par:**
- `cinema_sparql_generator.py` (génération SPARQL)
- `cinema_chatbot.py` (génération réponse finale)

**Tester:**
```bash
python llm_client.py
# Test de connexion au LLM
```

---

### 4. `graphdb_client.py` - Client GraphDB

**Rôle:** Exécute les requêtes SPARQL sur GraphDB

**Architecture:**
```python
class GraphDBClient:
    def __init__(endpoint):
        """Se connecte à GraphDB"""
        self.endpoint = endpoint
    
    def query(sparql_query):
        """Exécute une requête SPARQL"""
        # 1. Envoie HTTP POST à GraphDB
        # 2. Reçoit JSON results
        # 3. Retourne les bindings
```

**Comment ça marche:**
```python
# Utilisation
client = GraphDBClient("http://localhost:7200/repositories/movie-test")

sparql = """
    PREFIX cinema: <http://exemple.org/cinema#>
    SELECT ?film ?titre
    WHERE {
        ?film rdf:type cinema:Film .
        ?film cinema:titre ?titre .
    }
"""

results = client.query(sparql)
# results = {
#   "results": {
#     "bindings": [
#       {"film": {"value": "..."}, "titre": {"value": "Amélie"}}
#     ]
#   }
# }
```

**Format de retour:**
```json
{
  "results": {
    "bindings": [
      {
        "film": {"value": "http://exemple.org/cinema#LesFabuleux"},
        "titre": {"value": "Le Fabuleux Destin d'Amélie Poulain"},
        "annee": {"value": "2001", "datatype": "xsd:gYear"}
      }
    ]
  }
}
```

**Fonctionnalités:**
- ✅ Envoie requête SPARQL à GraphDB
- ✅ Parse réponse JSON
- ✅ Gère erreurs de connexion
- ✅ Gère timeout
- ✅ Test de connexion intégré

**Utilisé par:** `cinema_chatbot.py` (pour exécuter les requêtes)

**Tester:**
```bash
python graphdb_client.py
# Test de connexion et compte les triplets
```

---

### 5. `context_builder.py` - Formateur de Résultats

**Rôle:** Transforme les résultats SPARQL bruts en texte lisible pour le LLM

**Transformation:**

**ENTRÉE (GraphDB):**
```json
{
  "bindings": [
    {"acteur": {"value": "http://exemple.org/cinema#AudreyTautou"}},
    {"acteur": {"value": "http://exemple.org/cinema#OmarSy"}}
  ]
}
```

**SORTIE (Texte formaté):**
```
Données trouvées (2 résultats):

Résultat 1:
  - acteur: AudreyTautou

Résultat 2:
  - acteur: OmarSy
```

**Architecture:**
```python
class ContextBuilder:
    def format_results(bindings, explanation):
        """Formate les résultats SPARQL"""
        # 1. Parcourt chaque résultat
        # 2. Extrait les valeurs
        # 3. Nettoie les URIs (garde juste l'ID)
        # 4. Formate en texte lisible
        # 5. Retourne string
```

**Pourquoi ce fichier existe:**
- Le LLM ne peut pas lire du JSON brut efficacement
- Les URIs complètes sont trop longues
- Format texte = plus facile à comprendre pour le LLM

**Utilisé par:** `cinema_chatbot.py` (entre GraphDB et génération réponse)

---

### 6. `cinema_sparql_generator.py` - Le Cerveau 🧠

**Rôle:** Génère dynamiquement des requêtes SPARQL à partir de questions en français

**C'EST LE COMPOSANT LE PLUS IMPORTANT!**

**Architecture:**
```python
class CinemaSPARQLGenerator:
    def __init__(llm_client):
        self.llm = llm_client
        self.ontology_summary = """
            # Description de l'ontologie cinéma
            Classes: Film, Acteur, Réalisateur, Genre
            Propriétés: titre, annéeSortie, note, nom
            Relations: réaliséPar, avecActeur, genre
        """
    
    def generate_sparql(question):
        """Question FR → SPARQL query"""
        # 1. Construit prompt avec ontologie + exemples
        # 2. Envoie au LLM
        # 3. Parse réponse JSON
        # 4. Retourne {sparql, entités, relations, explication}
```

**Comment ça marche - DÉTAILS:**

**ÉTAPE 1: Construire le prompt**
```python
prompt = f"""
Tu es expert en SPARQL pour base de données cinéma.

ONTOLOGIE:
{self.ontology_summary}  # Structure des données

EXEMPLES (Few-Shot Learning):
Question: "Qui a réalisé Amélie?"
SPARQL: PREFIX cinema: <...>
        SELECT ?realisateur
        WHERE {{ ?film cinema:titre "Amélie" .
                 ?film cinema:réaliséPar ?realisateur }}

Question: "Films sortis après 2010"
SPARQL: PREFIX cinema: <...>
        SELECT ?film ?titre
        WHERE {{ ?film cinema:titre ?titre .
                 ?film cinema:annéeSortie ?annee .
                 FILTER(?annee > "2010"^^xsd:gYear) }}

MAINTENANT génère SPARQL pour: "{question}"

Réponds en JSON:
{{
  "sparql_query": "...",
  "entities_used": ["Film", "Acteur"],
  "relations_used": ["titre", "annéeSortie"],
  "explanation": "Description en français"
}}
"""
```

**ÉTAPE 2: LLM génère la requête**
```python
llm_response = self.llm.generate(prompt)
# LLM pense: "Pour trouver acteurs nés après 1975..."
# LLM génère JSON avec SPARQL
```

**ÉTAPE 3: Parser la réponse**
```python
result = json.loads(llm_response)
# result = {
#   "sparql_query": "PREFIX cinema: ...",
#   "entities_used": ["Acteur"],
#   "relations_used": ["annéeNaissance"],
#   "explanation": "Récupère acteurs nés après 1975"
# }
```

**Fonctionnalités:**
- ✅ **Few-Shot Learning**: Apprend par exemples
- ✅ **Ontology-Aware**: Connaît la structure des données
- ✅ **Dynamic**: Génère requête différente pour chaque question
- ✅ **Explainable**: Retourne entités et relations utilisées

**Utilisé par:** `cinema_chatbot.py` (première étape du pipeline)

---

### 7. `cinema_chatbot.py` - L'Orchestrateur

**Rôle:** Coordonne TOUS les composants pour répondre aux questions

**Architecture:**
```python
class CinemaChatbot:
    def __init__():
        # Initialise tous les composants
        self.graphdb = GraphDBClient()
        self.llm = FrenchLLMClient()
        self.sparql_generator = CinemaSPARQLGenerator(self.llm)
        self.context_builder = ContextBuilder()
    
    def answer_question(question):
        """Orchestration complète"""
        # ÉTAPE 1: Génère SPARQL
        # ÉTAPE 2: Exécute sur GraphDB
        # ÉTAPE 3: Formate résultats
        # ÉTAPE 4: Génère réponse
        # ÉTAPE 5: Affiche tout
```

**Pipeline complet - DÉTAILLÉ:**

```python
def answer_question(self, question):
    """
    ÉTAPE 1: Génération SPARQL
    """
    query_result = self.sparql_generator.generate_sparql(question)
    # query_result = {
    #   "sparql_query": "PREFIX cinema: ...",
    #   "entities_used": ["Acteur"],
    #   "relations_used": ["annéeNaissance"],
    #   "explanation": "..."
    # }
    
    sparql_query = query_result["sparql_query"]
    
    """
    ÉTAPE 2: Exécution GraphDB
    """
    results = self.graphdb.query(sparql_query)
    # results = {
    #   "results": {
    #     "bindings": [
    #       {"acteur": {"value": "..."}, "nom": {"value": "Audrey Tautou"}}
    #     ]
    #   }
    # }
    
    bindings = results['results']['bindings']
    
    """
    ÉTAPE 3: Construction contexte
    """
    context = self.context_builder.format_results(bindings)
    # context = "Données trouvées (4 résultats):\n  - acteur: AudreyTautou\n..."
    
    """
    ÉTAPE 4: Génération réponse
    """
    system_prompt = "Tu es expert en cinéma français..."
    user_prompt = f"Question: {question}\n\nContexte: {context}"
    
    answer = self.llm.generate(user_prompt, system_prompt)
    # answer = "Les acteurs nés après 1975 sont: Audrey Tautou..."
    
    """
    ÉTAPE 5: Affichage
    """
    print(f"QUESTION: {question}")
    print(f"SPARQL: {sparql_query}")
    print(f"RÉSULTATS: {len(bindings)}")
    print(f"RÉPONSE: {answer}")
    
    return {
        "success": True,
        "question": question,
        "sparql_query": sparql_query,
        "results_count": len(bindings),
        "answer": answer
    }
```

**Modes d'utilisation:**

**Mode 1: Question unique**
```bash
python cinema_chatbot.py --question "Qui a réalisé Intouchables?"
```

**Mode 2: Mode interactif**
```bash
python cinema_chatbot.py
# Démarre une boucle de conversation
```

**Utilisé par:** L'utilisateur final (vous!)

---

## 🎯 EXEMPLE COMPLET - FLUX DE DONNÉES

Prenons votre exemple: **"Quels acteurs sont nés après 1975 ?"**

### ÉTAPE 1: Question → SPARQL

**Input:**
```
Question: "Quels acteurs sont nés après 1975 ?"
```

**Dans cinema_sparql_generator.py:**
```python
# Construction du prompt avec:
# - Structure ontologie (Film, Acteur, propriétés...)
# - Exemples de questions/réponses
# - Question actuelle

prompt = """
Tu es expert SPARQL...
ONTOLOGIE: Acteur (nom, annéeNaissance...)
EXEMPLES: [3-4 exemples]
QUESTION: Quels acteurs sont nés après 1975?
Génère JSON avec SPARQL
"""

# LLM génère
llm_response = self.llm.generate(prompt)
```

**Output ÉTAPE 1:**
```json
{
  "sparql_query": "PREFIX cinema: <http://exemple.org/cinema#>\nPREFIX rdf: ...\nSELECT ?acteur ?nom\nWHERE {\n  ?acteur rdf:type cinema:Acteur .\n  ?acteur cinema:annéeNaissance ?anneeNaissance .\n  FILTER(?anneeNaissance > \"1975\"^^xsd:gYear)\n}",
  "entities_used": ["Acteur"],
  "relations_used": ["annéeNaissance"],
  "explanation": "Récupère les acteurs nés après 1975"
}
```

**Affichage console:**
```
📊 Entités utilisées: Acteur
🔗 Relations utilisées: annéeNaissance
💡 Explication: Récupère les acteurs nés après 1975

📝 Requête SPARQL:
PREFIX cinema: <http://exemple.org/cinema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?acteur ?nom
WHERE {
  ?acteur rdf:type cinema:Acteur .
  ?acteur cinema:annéeNaissance ?anneeNaissance .
  FILTER(?anneeNaissance > "1975"^^xsd:gYear)
}
```

---

### ÉTAPE 2: SPARQL → GraphDB

**Dans graphdb_client.py:**
```python
# Envoie requête à GraphDB
results = requests.post(
    "http://localhost:7200/repositories/movie-test",
    data=sparql_query,
    headers={"Accept": "application/sparql-results+json"}
)

# Parse réponse
json_results = results.json()
```

**Output ÉTAPE 2 (Brut):**
```json
{
  "results": {
    "bindings": [
      {
        "acteur": {"value": "http://exemple.org/cinema#AudreyTautou"},
        "nom": {"value": "Audrey Tautou"}
      },
      {
        "acteur": {"value": "http://exemple.org/cinema#OmarSy"},
        "nom": {"value": "Omar Sy"}
      },
      {
        "acteur": {"value": "http://exemple.org/cinema#LéaSeydoux"},
        "nom": {"value": "Léa Seydoux"}
      },
      {
        "acteur": {"value": "http://exemple.org/cinema#AdèleExarchopoulos"},
        "nom": {"value": "Adèle Exarchopoulos"}
      }
    ]
  }
}
```

**Affichage console:**
```
✅ 4 résultat(s) trouvé(s)!
```

---

### ÉTAPE 3: Résultats bruts → Contexte formaté

**Dans context_builder.py:**
```python
context = ""
for i, binding in enumerate(bindings, 1):
    context += f"Résultat {i}:\n"
    for key, value in binding.items():
        display_value = value['value']
        # Nettoie URI: http://...#AudreyTautou → AudreyTautou
        if display_value.startswith('http://'):
            display_value = display_value.split('#')[-1]
        context += f"  - {key}: {display_value}\n"
```

**Output ÉTAPE 3:**
```
Contexte de la requête: Récupère les acteurs nés après 1975

Données trouvées (4 résultats):

Résultat 1:
  - acteur: AudreyTautou

Résultat 2:
  - acteur: OmarSy

Résultat 3:
  - acteur: LéaSeydoux

Résultat 4:
  - acteur: AdèleExarchopoulos
```

**Affichage console:**
```
✅ Contexte créé (244 caractères)

📊 Aperçu du contexte:
Contexte de la requête: Récupère les acteurs nés après 1975
Données trouvées (4 résultats):
Résultat 1:
  - acteur: AudreyTautou
...
```

---

### ÉTAPE 4: Contexte → Réponse naturelle

**Dans cinema_chatbot.py:**
```python
# Construire prompt pour génération réponse
system_prompt = """
Tu es un assistant expert en cinéma français.
Tu réponds aux questions en te basant UNIQUEMENT sur le contexte fourni.
Tu réponds en français, de manière claire et naturelle.
"""

user_prompt = f"""
Question: Quels acteurs sont nés après 1975?

Contexte du graphe de connaissances (4 résultats):
{context}

Réponds à la question en te basant uniquement sur ce contexte.
Sois précis, informatif et naturel.
"""

# LLM génère réponse en français naturel
answer = self.llm.generate(user_prompt, system_prompt)
```

**Output ÉTAPE 4:**
```
Les acteurs nés après 1975 que j'ai trouvés dans notre base de données sont :
- Audrey Tautou (née le 9 août 1976)
- Omar Sy (né le 20 janvier 1978)
- Léa Seydoux (née le 1er juillet 1985)
- Adèle Exarchopoulos (née le 22 novembre 1993)

Ces acteurs ont tous fait carrière dans le cinéma français, et certains d'entre eux ont même remporté des prix prestigieux pour leurs performances.
```

**Affichage console:**
```
✅ Réponse générée!

💬 RÉPONSE FINALE:
================================================================================
Les acteurs nés après 1975 que j'ai trouvés dans notre base de données sont :
- Audrey Tautou (née le 9 août 1976)
- Omar Sy (né le 20 janvier 1978)
- Léa Seydoux (née le 1er juillet 1985)
- Adèle Exarchopoulos (née le 22 novembre 1993)

Ces acteurs ont tous fait carrière dans le cinéma français, et certains d'entre eux ont même remporté des prix prestigieux pour leurs performances.
================================================================================
```

---

## 📊 DIAGRAMME DE FLUX COMPLET

```
┌─────────────────────────────────────────┐
│  USER: "Quels acteurs nés après 1975?"  │
└───────────────┬─────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_chatbot.py                                │
│  answer_question(question)                        │
└───────────────┬───────────────────────────────────┘
                │
                │ ÉTAPE 1: Génère SPARQL
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_sparql_generator.py                       │
│  generate_sparql(question)                        │
│    │                                              │
│    ├─→ Lit ontology_summary                       │
│    ├─→ Construit prompt avec exemples             │
│    ├─→ Appelle llm_client.generate()              │
│    └─→ Parse JSON response                        │
└───────────────┬───────────────────────────────────┘
                │
                │ {"sparql_query": "SELECT ...",
                │  "entities_used": ["Acteur"],
                │  "relations_used": ["annéeNaissance"]}
                ▼
┌───────────────────────────────────────────────────┐
│  llm_client.py                                    │
│  FrenchLLMClient.generate(prompt)                 │
│    │                                              │
│    ├─→ POST http://localhost:1234/v1/chat/...    │
│    ├─→ LM Studio (Llama-3.1-8B)                   │
│    └─→ Retourne texte généré                      │
└───────────────┬───────────────────────────────────┘
                │
                │ SPARQL Query (text)
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_chatbot.py                                │
│  (reçoit le SPARQL)                               │
└───────────────┬───────────────────────────────────┘
                │
                │ ÉTAPE 2: Execute SPARQL
                ▼
┌───────────────────────────────────────────────────┐
│  graphdb_client.py                                │
│  query(sparql_query)                              │
│    │                                              │
│    ├─→ POST http://localhost:7200/repositories/  │
│    ├─→ GraphDB exécute requête                    │
│    └─→ Retourne JSON results                      │
└───────────────┬───────────────────────────────────┘
                │
                │ {"results": {"bindings": [...]}}
                │ (4 acteurs trouvés)
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_chatbot.py                                │
│  (reçoit résultats bruts)                         │
└───────────────┬───────────────────────────────────┘
                │
                │ ÉTAPE 3: Formate contexte
                ▼
┌───────────────────────────────────────────────────┐
│  context_builder.py                               │
│  format_results(bindings, explanation)            │
│    │                                              │
│    ├─→ Parcourt chaque résultat                   │
│    ├─→ Nettoie URIs                               │
│    └─→ Formate en texte lisible                   │
└───────────────┬───────────────────────────────────┘
                │
                │ "Données trouvées (4 résultats):
                │  Résultat 1: - acteur: AudreyTautou..."
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_chatbot.py                                │
│  (reçoit contexte formaté)                        │
└───────────────┬───────────────────────────────────┘
                │
                │ ÉTAPE 4: Génère réponse
                ▼
┌───────────────────────────────────────────────────┐
│  llm_client.py                                    │
│  FrenchLLMClient.generate(question + context)     │
│    │                                              │
│    ├─→ POST à LM Studio                           │
│    ├─→ LLM lit contexte                           │
│    └─→ Génère réponse naturelle en français       │
└───────────────┬───────────────────────────────────┘
                │
                │ "Les acteurs nés après 1975 sont:
                │  - Audrey Tautou (1976)..."
                ▼
┌───────────────────────────────────────────────────┐
│  cinema_chatbot.py                                │
│  (reçoit réponse finale)                          │
│                                                   │
│  ÉTAPE 5: Affiche tout                            │
│    - Question                                     │
│    - SPARQL généré                                │
│    - Entités/Relations utilisées                  │
│    - Nombre de résultats                          │
│    - Contexte                                     │
│    - Réponse finale                               │
└───────────────┬───────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────┐
│  CONSOLE: Affichage formaté pour l'utilisateur  │
│                                                 │
│  =====================================          │
│  ❓ QUESTION: Quels acteurs nés après 1975?    │
│  =====================================          │
│  🔧 ÉTAPE 1: Génération SPARQL... ✅            │
│  🔍 ÉTAPE 2: Exécution GraphDB... ✅ 4 résults  │
│  📋 ÉTAPE 3: Construction contexte... ✅         │
│  🤖 ÉTAPE 4: Génération réponse... ✅           │
│  💬 RÉPONSE FINALE:                             │
│  Les acteurs nés après 1975 sont:              │
│  - Audrey Tautou (1976)                        │
│  - Omar Sy (1978)                              │
│  - Léa Seydoux (1985)                          │
│  - Adèle Exarchopoulos (1993)                  │
│  =====================================          │
└─────────────────────────────────────────────────┘
```

---

## 🔑 CONCEPTS CLÉS

### 1. **Few-Shot Learning**

Le système **apprend par exemples** au lieu de règles hardcodées.

**Dans cinema_sparql_generator.py:**
```python
EXEMPLES:
Question: "Qui a réalisé Amélie?"
SPARQL: SELECT ?realisateur WHERE {?film titre "Amélie" ...}

Question: "Films sortis après 2010"
SPARQL: SELECT ?film WHERE {?film annéeSortie ?a . FILTER(?a > 2010)}

Maintenant: "Quels acteurs nés après 1975?"
LLM génère: SELECT ?acteur WHERE {?acteur annéeNaissance ?y . FILTER(?y > 1975)}
```

Le LLM comprend le pattern et l'applique!

### 2. **Ontology-Aware**

Le LLM connaît la structure de vos données.

```python
ontology_summary = """
Classes: Film, Acteur, Réalisateur, Genre
Propriétés Film: titre, annéeSortie, note, durée
Propriétés Acteur: nom, annéeNaissance, nationalité
Relations: réaliséPar (Film→Réalisateur), avecActeur (Film→Acteur)
"""
```

Quand on demande "acteurs nés après 1975", le LLM sait:
- Utiliser classe `Acteur`
- Utiliser propriété `annéeNaissance`
- Appliquer FILTER pour "après 1975"

### 3. **Pipeline GraphRAG**

**RAG traditionnel:** Documents → Chunks → Embeddings → Vector search → LLM

**GraphRAG (notre cas):** Question → SPARQL → KG Query → Structured data → LLM

**Avantages:**
- ✅ Pas d'hallucinations (données viennent du KG)
- ✅ Précis (requêtes structurées)
- ✅ Explainable (on voit le SPARQL)
- ✅ Flexible (génération dynamique)

### 4. **Separation of Concerns**

Chaque fichier a UN rôle précis:
- `config_cinema.py`: Configuration
- `llm_client.py`: Communication LLM
- `graphdb_client.py`: Communication GraphDB
- `context_builder.py`: Formatage
- `cinema_sparql_generator.py`: Logique SPARQL
- `cinema_chatbot.py`: Orchestration

**Avantage:** Facile à modifier, tester, debugger chaque partie indépendamment.

---

## 🎯 POINTS D'AMÉLIORATION

### Pour améliorer les résultats:

**1. Ajouter plus d'exemples (Few-Shot)**

Dans `cinema_sparql_generator.py`, section exemples:
```python
# Actuellement: 3-4 exemples
# Amélioration: Ajouter 10-15 exemples variés

EXEMPLE 5:
Question: "Films avec note > 8"
SPARQL: ... FILTER(?note > 8)

EXEMPLE 6:
Question: "Acteurs français"
SPARQL: ... ?acteur nationalité "Français"

etc.
```

**2. Affiner l'ontology_summary**

Plus de détails = meilleures requêtes:
```python
ontology_summary = """
Acteur:
  - nom (string)
  - annéeNaissance (gYear) ← Utiliser FILTER avec xsd:gYear
  - nationalité (string)
  - récompenses (string, optionnel)

Exemples de filtres:
  - Année: FILTER(?annee > "1975"^^xsd:gYear)
  - Note: FILTER(?note > 8.0)
  - Texte: FILTER(CONTAINS(?titre, "vie"))
"""
```

**3. Gérer les erreurs mieux**

Ajouter validation dans `cinema_sparql_generator.py`:
```python
if "SELECT" not in sparql_query:
    # Réessayer ou utiliser fallback query
```

---

## 🐛 DEBUGGING

### Si 0 résultats trouvés:

**1. Vérifier données dans GraphDB:**
```sparql
SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }
```

**2. Vérifier namespace:**
```sparql
SELECT DISTINCT ?type WHERE {
  ?s a ?type
} LIMIT 10
```

**3. Tester SPARQL manuellement:**
Copier la requête générée et l'exécuter dans GraphDB web interface

**4. Activer mode debug:**
```python
# Dans cinema_chatbot.py
result = self.sparql_generator.generate_sparql(question, debug=True)
# Affiche la réponse brute du LLM
```

---

## 📚 RÉSUMÉ

**Le système fonctionne comme une chaîne:**

```
Question FR
    ↓ (cinema_chatbot.py orchestre)
[cinema_sparql_generator.py] + [llm_client.py]
    → Génère SPARQL
    ↓
[graphdb_client.py]
    → Exécute sur GraphDB
    ↓
[context_builder.py]
    → Formate résultats
    ↓
[llm_client.py]
    → Génère réponse FR
    ↓
Réponse naturelle
```

**Chaque fichier = Une responsabilité**
**Configuration centralisée dans .env et config_cinema.py**
**LLM fait le "travail intelligent" (génération SPARQL + réponse)**
**GraphDB stocke les données structurées**

---

**Le système est modulaire, testable, et améliorable! 🎬🚀**
