# Configuration GraphDB - Ontologie + Knowledge Graph

## ✅ Méthode CORRECTE

### 1. Créer un Repository dans GraphDB

**Interface GraphDB** : http://localhost:7200

```
Setup → Repositories → Create new repository
├── Repository ID: horse-knowledge-graph
├── Repository type: GraphDB Repository
├── Ruleset: OWL-Horst (Optimized)
└── Enable context index: ✓
```

**Pourquoi OWL-Horst ?**
- Support inférence OWL
- Performance équilibrée
- Parfait pour ontologie + instances

---

### 2. Import de l'Ontologie (ontology.owl)

**Méthode A : Interface Web** (Recommandée pour début)

```
Import → RDF → Server files
├── Upload: ontology.owl
├── Named graph: http://example.org/ontology
├── Base URI: http://example.org/horse-ontology#
└── Import
```

**Méthode B : SPARQL UPDATE**

```sparql
# Charger l'ontologie avec contexte spécifique
LOAD <file:///path/to/ontology.owl> 
INTO GRAPH <http://example.org/ontology>
```

---

### 3. Import du Knowledge Graph (HorseKnowledgeGraphBis.rdf)

**Interface Web :**

```
Import → RDF → Server files
├── Upload: HorseKnowledgeGraphBis.rdf
├── Named graph: http://example.org/instances
├── Base URI: http://example.org/horse-data#
└── Import
```

**Important** : Utiliser un **named graph différent** pour séparer logiquement :
- Ontologie (schéma) → `<http://example.org/ontology>`
- Données (instances) → `<http://example.org/instances>`

---

### 4. Vérification de l'import

**Requête 1 : Compter les triplets**

```sparql
SELECT (COUNT(*) AS ?count) WHERE {
  GRAPH ?g { ?s ?p ?o }
}
GROUP BY ?g
```

**Résultat attendu :**
```
| Graph                           | Count |
|---------------------------------|-------|
| http://example.org/ontology     | 150   |
| http://example.org/instances    | 450   |
```

**Requête 2 : Lister les classes de l'ontologie**

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?class ?label WHERE {
  GRAPH <http://example.org/ontology> {
    ?class a owl:Class .
    OPTIONAL { ?class rdfs:label ?label }
  }
}
```

**Requête 3 : Vérifier les instances**

```sparql
PREFIX : <http://example.org/horse-ontology#>

SELECT ?horse ?session WHERE {
  GRAPH <http://example.org/instances> {
    ?horse a :Horse .
    ?horse :hasParticipated ?session .
  }
} LIMIT 10
```

---

## ⚠️ Problèmes courants et solutions

### Problème 1 : "Pas de résultats" ou "Réponses vides"

**Causes possibles :**

1. **Namespace mismatch**
   ```sparql
   # ❌ Mauvais
   SELECT ?s WHERE { ?s a Horse }
   
   # ✅ Correct
   PREFIX : <http://example.org/horse-ontology#>
   SELECT ?s WHERE { ?s a :Horse }
   ```

2. **Named graph non spécifié**
   ```sparql
   # ❌ Cherche dans le graphe par défaut
   SELECT ?s WHERE { ?s a :Horse }
   
   # ✅ Spécifier le graphe
   SELECT ?s WHERE {
     GRAPH <http://example.org/instances> {
       ?s a :Horse
     }
   }
   
   # OU recherche dans tous les graphes
   SELECT ?s WHERE {
     GRAPH ?g { ?s a :Horse }
   }
   ```

3. **Ontologie en anglais, KG en français**
   ```turtle
   # Dans l'ontologie (ontology.owl)
   :Horse a owl:Class ;
     rdfs:label "Cheval"@fr ;
     rdfs:label "Horse"@en .
   
   # Dans le KG (instances)
   :horse123 a :Horse ;
     :hasRace "Pur-sang"@fr .
   ```

---

## 🔧 Configuration optimale GraphDB

### Fichier de configuration recommandé

**Repository config (horse-kg-config.ttl)**

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rep: <http://www.openrdf.org/config/repository#> .
@prefix sr: <http://www.openrdf.org/config/repository/sail#> .
@prefix sail: <http://www.openrdf.org/config/sail#> .
@prefix owlim: <http://www.ontotext.com/trree/owlim#> .

[] a rep:Repository ;
    rep:repositoryID "horse-knowledge-graph" ;
    rdfs:label "Horse Knowledge Graph" ;
    rep:repositoryImpl [
        rep:repositoryType "openrdf:SailRepository" ;
        sr:sailImpl [
            sail:sailType "GraphDB:Sail" ;
            
            # Ruleset pour inférence
            owlim:ruleset "owl-horst-optimized" ;
            
            # Activation des indexes
            owlim:enable-context-index "true" ;
            owlim:enablePredicateList "true" ;
            
            # Performance tuning
            owlim:cache-memory "2g" ;
            owlim:tuple-index-memory "1g" ;
            
            # Support multilingue
            owlim:enable-literal-index "true" ;
        ]
    ] .
```

---

## 📋 Checklist avant de générer des requêtes

- [ ] Ontologie importée dans un named graph dédié
- [ ] KG importé dans un named graph dédié
- [ ] Les prefixes/namespaces sont cohérents
- [ ] Test de requête basique fonctionne
- [ ] Les labels rdfs:label sont en français (si nécessaire)
- [ ] L'inférence OWL est activée
- [ ] Les indexes sont créés

---

## 🎯 Requête universelle pour exploration

**Utiliser cette requête pour comprendre votre graphe :**

```sparql
# Explorer tout le graphe
SELECT DISTINCT ?type (COUNT(?instance) AS ?count) WHERE {
  ?instance a ?type .
} 
GROUP BY ?type
ORDER BY DESC(?count)
```

Cela vous montre :
- Quelles classes existent
- Combien d'instances par classe
- Si vos données sont bien chargées

---

## 💡 Recommandation finale

**Structure idéale :**

```
GraphDB Repository: horse-knowledge-graph
├── Named Graph: <http://example.org/ontology>
│   └── ontology.owl (Classes, Propriétés, Règles)
│
└── Named Graph: <http://example.org/instances>
    └── HorseKnowledgeGraphBis.rdf (Instances, Données)
```

**Avantages :**
- ✅ Séparation claire schéma/données
- ✅ Facile de recharger l'ontologie sans perdre les données
- ✅ Queries plus explicites
- ✅ Meilleure maintenance
