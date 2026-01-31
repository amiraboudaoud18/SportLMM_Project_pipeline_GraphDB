# 🐴 Dataset Q&A pour Évaluation RAGAS - Ontologie Équine

---

## 📋 FORMAT POUR RAGAS

Chaque question inclut:
- ✅ **Question** (en français)
- ✅ **Réponse de référence** (ground truth)
- ✅ **Contexte nécessaire** (entités RDF requises)
- ✅ **Requête SPARQL** (pour validation)
- ✅ **Type de question** (pour métriques RAGAS)

---

## 🎯 CATÉGORIE 1: Questions Simples (Factual Retrieval)

### Q1: Identification du Cheval
**Question:** Quel est le nom du cheval dans le système ?

**Réponse de référence:** Le cheval s'appelle Dakota.

**Contexte requis (Entités RDF):**
```turtle
:Horse1 rdf:type :Horse ;
        :hasName "Dakota"^^xsd:string .
```

**Entités nécessaires:**
- `Horse1` (instance)
- Propriété: `hasName`
- Valeur: "Dakota"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?name WHERE {
  ?horse rdf:type :Horse ;
         :hasName ?name .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

### Q2: Identification du Capteur
**Question:** Quel est l'identifiant du capteur inertiel ?

**Réponse de référence:** L'identifiant du capteur est SI-001523.

**Contexte requis:**
```turtle
:Sensor1 rdf:type :InertialSensors ;
         :hasSensorID "SI-001523" .
```

**Entités nécessaires:**
- `Sensor1` (instance)
- Propriété: `hasSensorID`
- Valeur: "SI-001523"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensorID WHERE {
  ?sensor rdf:type :InertialSensors ;
          :hasSensorID ?sensorID .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

## 🎯 CATÉGORIE 2: Questions de Relation (Single-hop)

### Q3: Événements de Dakota
**Question:** Dans quels événements sportifs Dakota participe-t-il ?

**Réponse de référence:** Dakota participe à trois événements sportifs : le saut d'obstacles (Event_SJ_2026_01), le dressage (Event_Dressage_2026_01) et le cross-country (Event_Cross_2026_01).

**Contexte requis:**
```turtle
:Horse1 rdf:type :Horse ;
        :hasName "Dakota" ;
        :CompetesIn :Event_SJ_2026_01 ,
                    :Event_Dressage_2026_01 ,
                    :Event_Cross_2026_01 .

:Event_SJ_2026_01 rdf:type :ShowJumping .
:Event_Dressage_2026_01 rdf:type :Dressage .
:Event_Cross_2026_01 rdf:type :Cross .
```

**Entités nécessaires:**
- `Horse1` (instance)
- `Event_SJ_2026_01`, `Event_Dressage_2026_01`, `Event_Cross_2026_01` (instances)
- Relation: `CompetesIn`
- Classes: `ShowJumping`, `Dressage`, `Cross`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?event ?eventType WHERE {
  :Horse1 :CompetesIn ?event .
  ?event rdf:type ?eventType .
  FILTER(?eventType IN (:ShowJumping, :Dressage, :Cross))
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

### Q4: Étapes d'Entraînement
**Question:** Quelles étapes d'entraînement Dakota suit-il ?

**Réponse de référence:** Dakota suit quatre étapes d'entraînement : la préparation (Training_Preparation_SJ_01), la pré-compétition (Training_PreCompetition_SJ_01), la compétition (Training_Competition_SJ_01) et la transition (Training_Transition_SJ_01).

**Contexte requis:**
```turtle
:Horse1 :TrainsIn :Training_Preparation_SJ_01 ,
                  :Training_PreCompetition_SJ_01 ,
                  :Training_Competition_SJ_01 ,
                  :Training_Transition_SJ_01 .

:Training_Preparation_SJ_01 rdf:type :PreparationStage .
:Training_PreCompetition_SJ_01 rdf:type :PreCompetitionStage .
:Training_Competition_SJ_01 rdf:type :CompetitionStage .
:Training_Transition_SJ_01 rdf:type :TransitionStage .
```

**Entités nécessaires:**
- `Horse1`
- `Training_Preparation_SJ_01`, `Training_PreCompetition_SJ_01`, `Training_Competition_SJ_01`, `Training_Transition_SJ_01`
- Relation: `TrainsIn`
- Classes: `PreparationStage`, `PreCompetitionStage`, `CompetitionStage`, `TransitionStage`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?training ?stage WHERE {
  :Horse1 :TrainsIn ?training .
  ?training rdf:type ?stage .
  FILTER(?stage IN (:PreparationStage, :PreCompetitionStage, 
                    :CompetitionStage, :TransitionStage))
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

## 🎯 CATÉGORIE 3: Questions avec Propriétés (Attribute Retrieval)

### Q5: Fréquence d'Entraînement - Préparation
**Question:** Quelle est la fréquence d'entraînement pendant la phase de préparation ?

**Réponse de référence:** Pendant la phase de préparation, la fréquence d'entraînement est de 4 séances par semaine.

**Contexte requis:**
```turtle
:Training_Preparation_SJ_01 rdf:type :PreparationStage ;
                            :Frequency 4 ;
                            :Intensity "Moderate" ;
                            :Volume "45min" .
```

**Entités nécessaires:**
- `Training_Preparation_SJ_01`
- Propriété: `Frequency`
- Valeur: 4

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?frequency WHERE {
  ?training rdf:type :PreparationStage ;
            :Frequency ?frequency .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q6: Intensité d'Entraînement - Pré-Compétition
**Question:** Quelle est l'intensité d'entraînement durant la phase pré-compétition ?

**Réponse de référence:** Durant la phase pré-compétition, l'intensité d'entraînement est élevée (High).

**Contexte requis:**
```turtle
:Training_PreCompetition_SJ_01 rdf:type :PreCompetitionStage ;
                               :Frequency 3 ;
                               :Intensity "High" ;
                               :Volume "60min" .
```

**Entités nécessaires:**
- `Training_PreCompetition_SJ_01`
- Propriété: `Intensity`
- Valeur: "High"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?intensity WHERE {
  ?training rdf:type :PreCompetitionStage ;
            :Intensity ?intensity .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q7: Volume d'Entraînement - Compétition
**Question:** Quelle est la durée des séances pendant la phase de compétition ?

**Réponse de référence:** Pendant la phase de compétition, les séances durent 30 minutes.

**Contexte requis:**
```turtle
:Training_Competition_SJ_01 rdf:type :CompetitionStage ;
                            :Frequency 1 ;
                            :Intensity "Peak" ;
                            :Volume "30min" .
```

**Entités nécessaires:**
- `Training_Competition_SJ_01`
- Propriété: `Volume`
- Valeur: "30min"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?volume WHERE {
  ?training rdf:type :CompetitionStage ;
            :Volume ?volume .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

## 🎯 CATÉGORIE 4: Questions Multi-Hop (Complex Reasoning)

### Q8: Dépendance Entraînement-Événement
**Question:** De quel événement dépendent les étapes d'entraînement de Dakota ?

**Réponse de référence:** Toutes les étapes d'entraînement de Dakota (préparation, pré-compétition, compétition et transition) dépendent de l'événement de saut d'obstacles (Event_SJ_2026_01).

**Contexte requis:**
```turtle
:Horse1 :TrainsIn :Training_Preparation_SJ_01 ,
                  :Training_PreCompetition_SJ_01 ,
                  :Training_Competition_SJ_01 ,
                  :Training_Transition_SJ_01 .

:Training_Preparation_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_PreCompetition_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_Competition_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_Transition_SJ_01 :dependsOn :Event_SJ_2026_01 .

:Event_SJ_2026_01 rdf:type :ShowJumping .
```

**Entités nécessaires:**
- `Horse1`
- Toutes les instances de `Training`
- `Event_SJ_2026_01`
- Relations: `TrainsIn`, `dependsOn`
- Classe: `ShowJumping`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT DISTINCT ?event WHERE {
  :Horse1 :TrainsIn ?training .
  ?training :dependsOn ?event .
}
```

**Type RAGAS:** `multi_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

### Q9: Thématiques des Événements
**Question:** Quelles thématiques sont associées aux événements sportifs auxquels participe Dakota ?

**Réponse de référence:** Les événements sportifs auxquels Dakota participe sont associés à deux thématiques : l'équitation (HorseRiding) et les indicateurs de performance (IndicateurPerformance).

**Contexte requis:**
```turtle
:Horse1 :CompetesIn :Event_SJ_2026_01 ,
                    :Event_Dressage_2026_01 ,
                    :Event_Cross_2026_01 .

:Event_SJ_2026_01 rdf:type :ShowJumping ;
                  :hasThematique :HorseRiding ,
                                 :IndicateurPerformance .

:Event_Dressage_2026_01 rdf:type :Dressage ;
                        :hasThematique :HorseRiding ,
                                       :IndicateurPerformance .

:Event_Cross_2026_01 rdf:type :Cross ;
                     :hasThematique :HorseRiding ,
                                    :IndicateurPerformance .
```

**Entités nécessaires:**
- `Horse1`
- Toutes les instances d'événements
- Relations: `CompetesIn`, `hasThematique`
- Classes: `HorseRiding`, `IndicateurPerformance`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT DISTINCT ?thematique WHERE {
  :Horse1 :CompetesIn ?event .
  ?event :hasThematique ?thematique .
}
```

**Type RAGAS:** `multi_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 5: Questions de Comparaison (Comparison)

### Q10: Comparaison des Intensités
**Question:** Comment l'intensité d'entraînement varie-t-elle entre la phase de préparation et la phase de compétition ?

**Réponse de référence:** L'intensité d'entraînement augmente significativement entre la phase de préparation et la phase de compétition. Durant la préparation, l'intensité est modérée (Moderate), tandis qu'elle atteint son pic maximum (Peak) pendant la compétition.

**Contexte requis:**
```turtle
:Training_Preparation_SJ_01 rdf:type :PreparationStage ;
                            :Intensity "Moderate" .

:Training_Competition_SJ_01 rdf:type :CompetitionStage ;
                            :Intensity "Peak" .
```

**Entités nécessaires:**
- `Training_Preparation_SJ_01`, `Training_Competition_SJ_01`
- Propriété: `Intensity`
- Valeurs: "Moderate", "Peak"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?stage ?intensity WHERE {
  ?training rdf:type ?stage ;
            :Intensity ?intensity .
  FILTER(?stage IN (:PreparationStage, :CompetitionStage))
}
```

**Type RAGAS:** `comparison`
**Difficulté:** ⭐⭐⭐ Difficile

---

### Q11: Comparaison des Fréquences
**Question:** Quelle est la différence de fréquence d'entraînement entre la préparation et la transition ?

**Réponse de référence:** La fréquence d'entraînement diminue de la préparation à la transition. Durant la préparation, il y a 4 séances par semaine, tandis que durant la transition, il n'y en a que 2 par semaine.

**Contexte requis:**
```turtle
:Training_Preparation_SJ_01 rdf:type :PreparationStage ;
                            :Frequency 4 .

:Training_Transition_SJ_01 rdf:type :TransitionStage ;
                           :Frequency 2 .
```

**Entités nécessaires:**
- `Training_Preparation_SJ_01`, `Training_Transition_SJ_01`
- Propriété: `Frequency`
- Valeurs: 4, 2

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?stage ?frequency WHERE {
  ?training rdf:type ?stage ;
            :Frequency ?frequency .
  FILTER(?stage IN (:PreparationStage, :TransitionStage))
}
```

**Type RAGAS:** `comparison`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 6: Questions d'Agrégation (Aggregation)

### Q12: Nombre d'Étapes d'Entraînement
**Question:** Combien d'étapes d'entraînement différentes existent dans le système ?

**Réponse de référence:** Il existe 4 étapes d'entraînement différentes dans le système : préparation, pré-compétition, compétition et transition.

**Contexte requis:**
```turtle
:Training_Preparation_SJ_01 rdf:type :PreparationStage .
:Training_PreCompetition_SJ_01 rdf:type :PreCompetitionStage .
:Training_Competition_SJ_01 rdf:type :CompetitionStage .
:Training_Transition_SJ_01 rdf:type :TransitionStage .
```

**Entités nécessaires:**
- Toutes les instances de `Training`
- Classes: `PreparationStage`, `PreCompetitionStage`, `CompetitionStage`, `TransitionStage`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT (COUNT(DISTINCT ?training) AS ?count) WHERE {
  ?training rdf:type ?stage .
  FILTER(?stage IN (:PreparationStage, :PreCompetitionStage, 
                    :CompetitionStage, :TransitionStage))
}
```

**Type RAGAS:** `aggregation`
**Difficulté:** ⭐⭐ Moyen

---

### Q13: Volume Total d'Entraînement
**Question:** Quel est le volume total d'entraînement hebdomadaire pendant la phase de préparation ?

**Réponse de référence:** Le volume total d'entraînement hebdomadaire pendant la phase de préparation est de 180 minutes (3 heures), calculé à partir de 4 séances de 45 minutes chacune.

**Contexte requis:**
```turtle
:Training_Preparation_SJ_01 rdf:type :PreparationStage ;
                            :Frequency 4 ;
                            :Volume "45min" .
```

**Entités nécessaires:**
- `Training_Preparation_SJ_01`
- Propriétés: `Frequency`, `Volume`
- Calcul: 4 × 45min = 180min

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?frequency ?volume WHERE {
  ?training rdf:type :PreparationStage ;
            :Frequency ?frequency ;
            :Volume ?volume .
}
```

**Type RAGAS:** `aggregation`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 7: Questions Hiérarchiques (Hierarchical)

### Q14: Types d'Événements Sportifs
**Question:** Quels types d'événements sportifs équestres sont définis dans l'ontologie ?

**Réponse de référence:** L'ontologie définit trois types d'événements sportifs équestres : le saut d'obstacles (ShowJumping), le dressage (Dressage) et le cross-country (Cross).

**Contexte requis:**
```turtle
:ShowJumping rdfs:subClassOf :SportingEvent .
:Dressage rdfs:subClassOf :SportingEvent .
:Cross rdfs:subClassOf :SportingEvent .
```

**Entités nécessaires:**
- Classes: `SportingEvent`, `ShowJumping`, `Dressage`, `Cross`
- Relation: `rdfs:subClassOf`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?eventType WHERE {
  ?eventType rdfs:subClassOf :SportingEvent .
  FILTER(?eventType IN (:ShowJumping, :Dressage, :Cross))
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐ Moyen

---

### Q15: Indicateurs de Bien-être
**Question:** Quels sont les indicateurs principaux pour évaluer le bien-être d'un cheval ?

**Réponse de référence:** Les quatre indicateurs principaux pour évaluer le bien-être d'un cheval sont : l'alimentation (Alimentation), l'hébergement (Heberegement), le comportement (Compertement) et l'état de santé (HealthStatus).

**Contexte requis:**
```turtle
:Alimentation rdfs:subClassOf :IndicateurBienetre .
:Heberegement rdfs:subClassOf :IndicateurBienetre .
:Compertement rdfs:subClassOf :IndicateurBienetre .
:HealthStatus rdfs:subClassOf :IndicateurBienetre .
```

**Entités nécessaires:**
- Classe parent: `IndicateurBienetre`
- Sous-classes: `Alimentation`, `Heberegement`, `Compertement`, `HealthStatus`
- Relation: `rdfs:subClassOf`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?indicator WHERE {
  ?indicator rdfs:subClassOf :IndicateurBienetre .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐ Moyen

---

### Q16: Sous-indicateurs d'Hébergement
**Question:** Quels aspects de l'hébergement sont évalués pour le bien-être du cheval ?

**Réponse de référence:** L'hébergement est évalué selon trois aspects : le confort de repos (ConfortRepos), le confort thermique (ConfortThermique) et la facilité de mouvement (FacilitéDuMouvement).

**Contexte requis:**
```turtle
:ConfortRepos rdfs:subClassOf :Heberegement .
:ConfortThermique rdfs:subClassOf :Heberegement .
:FacilitéDuMouvement rdfs:subClassOf :Heberegement .
```

**Entités nécessaires:**
- Classe parent: `Heberegement`
- Sous-classes: `ConfortRepos`, `ConfortThermique`, `FacilitéDuMouvement`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?aspect WHERE {
  ?aspect rdfs:subClassOf :Heberegement .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 8: Questions sur les Dispositifs (Device/Sensor)

### Q17: Utilisation des Capteurs Inertiels
**Question:** À quoi servent les capteurs inertiels dans l'ontologie ?

**Réponse de référence:** Les capteurs inertiels servent à la classification des allures (GaitClassification) des chevaux.

**Contexte requis:**
```turtle
:InertialSensors rdfs:subClassOf :ExperimentalDevices ;
                 :isUsedFor :GaitClassification .
```

**Entités nécessaires:**
- Classe: `InertialSensors`
- Classe: `GaitClassification`
- Relation: `isUsedFor`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?objective WHERE {
  :InertialSensors :isUsedFor ?objective .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

### Q18: Mesures des Capteurs
**Question:** Quels types de mesures peuvent fournir les capteurs inertiels ?

**Réponse de référence:** Les capteurs inertiels peuvent fournir cinq types de mesures : l'accélération (Acceleration), les données gyroscopiques (Gyroscope), l'angle de balancement (AngleSwing), l'angle de torsion (AngleTwist) et l'angle vertical (AngleVertical).

**Contexte requis:**
```turtle
:Acceleration rdfs:subClassOf :SensorMeasurements .
:Gyroscope rdfs:subClassOf :SensorMeasurements .
:AngleSwing rdfs:subClassOf :SensorMeasurements .
:AngleTwist rdfs:subClassOf :SensorMeasurements .
:AngleVertical rdfs:subClassOf :SensorMeasurements .

:SensorMeasurements rdfs:subClassOf :InertialSensors .
```

**Entités nécessaires:**
- Classe parent: `SensorMeasurements`
- Sous-classes: `Acceleration`, `Gyroscope`, `AngleSwing`, `AngleTwist`, `AngleVertical`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?measurement WHERE {
  ?measurement rdfs:subClassOf :SensorMeasurements .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐ Moyen

---

### Q19: Positionnement des Capteurs
**Question:** Où peut-on positionner des capteurs sur un cheval ?

**Réponse de référence:** Les capteurs peuvent être positionnés à sept emplacements sur un cheval : le front (Forehead), le garrot (Withers), le sternum (Sternum), le sacrum (Scarum), le bassin (Pool), le canon de l'antérieur (CanonOfForelimb) et le canon du postérieur (CanonOfHindlimb).

**Contexte requis:**
```turtle
:Forehead rdfs:subClassOf :SensorsPosition .
:Withers rdfs:subClassOf :SensorsPosition .
:Sternum rdfs:subClassOf :SensorsPosition .
:Scarum rdfs:subClassOf :SensorsPosition .
:Pool rdfs:subClassOf :SensorsPosition .
:CanonOfForelimb rdfs:subClassOf :SensorsPosition .
:CanonOfHindlimb rdfs:subClassOf :SensorsPosition .

:SensorsPosition rdfs:subClassOf :InertialSensors .
```

**Entités nécessaires:**
- Classe parent: `SensorsPosition`
- Toutes les sous-classes de positions

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?position WHERE {
  ?position rdfs:subClassOf :SensorsPosition .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐ Moyen

---

## 🎯 CATÉGORIE 9: Questions sur la Performance (Performance Indicators)

### Q20: Facteurs de Performance
**Question:** Quels sont les facteurs qui influencent la performance d'un cheval ?

**Réponse de référence:** Cinq facteurs influencent la performance d'un cheval : le facteur physique (FacteurPhysique), le facteur technique (FacteurTechnique), le facteur technico-tactique (FacteurTechnicoTactique), le facteur mental (FacteurMental) et le facteur social (FacteurSocial).

**Contexte requis:**
```turtle
:FacteurPhysique rdfs:subClassOf :IndicateurPerformance .
:FacteurTechnique rdfs:subClassOf :IndicateurPerformance .
:FacteurTechnicoTactique rdfs:subClassOf :IndicateurPerformance .
:FacteurMental rdfs:subClassOf :IndicateurPerformance .
:FacteurSocial rdfs:subClassOf :IndicateurPerformance .
```

**Entités nécessaires:**
- Classe parent: `IndicateurPerformance`
- Toutes les sous-classes de facteurs

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?factor WHERE {
  ?factor rdfs:subClassOf :IndicateurPerformance .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐ Moyen

---

### Q21: Aspects du Facteur Technique
**Question:** Quels aspects constituent le facteur technique de performance ?

**Réponse de référence:** Le facteur technique comprend cinq aspects : la qualité du geste (QualiteGeste), la qualité de déplacement (QualiteDeplacement), la variété de mouvement (VarieteMouvement), la vitesse d'exécution (VitesseExécution) et la précision technique (PresicisionTechnique).

**Contexte requis:**
```turtle
:QualiteGeste rdfs:subClassOf :FacteurTechnique .
:QualiteDeplacement rdfs:subClassOf :FacteurTechnique .
:VarieteMouvement rdfs:subClassOf :FacteurTechnique .
:VitesseExécution rdfs:subClassOf :FacteurTechnique .
:PresicisionTechnique rdfs:subClassOf :FacteurTechnique .
```

**Entités nécessaires:**
- Classe parent: `FacteurTechnique`
- Toutes les sous-classes techniques

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?aspect WHERE {
  ?aspect rdfs:subClassOf :FacteurTechnique .
}
```

**Type RAGAS:** `hierarchical`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 10: Questions Complexes Multi-Hop (Advanced Reasoning)

### Q22: Pipeline Complet Cheval-Événement-Entraînement
**Question:** Décris le cycle complet entre Dakota, ses événements et son entraînement.

**Réponse de référence:** Dakota suit un cycle complet structuré : il participe à trois événements sportifs (saut d'obstacles, dressage et cross). Pour le saut d'obstacles, qui est son événement principal, il suit quatre étapes d'entraînement spécifiques (préparation, pré-compétition, compétition et transition), et toutes ces étapes dépendent directement de cet événement cible.

**Contexte requis:**
```turtle
:Horse1 :hasName "Dakota" ;
        :CompetesIn :Event_SJ_2026_01 ,
                    :Event_Dressage_2026_01 ,
                    :Event_Cross_2026_01 ;
        :TrainsIn :Training_Preparation_SJ_01 ,
                  :Training_PreCompetition_SJ_01 ,
                  :Training_Competition_SJ_01 ,
                  :Training_Transition_SJ_01 .

:Training_Preparation_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_PreCompetition_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_Competition_SJ_01 :dependsOn :Event_SJ_2026_01 .
:Training_Transition_SJ_01 :dependsOn :Event_SJ_2026_01 .
```

**Entités nécessaires:**
- `Horse1` avec toutes ses relations
- Toutes les instances d'événements
- Toutes les instances d'entraînement
- Relations: `CompetesIn`, `TrainsIn`, `dependsOn`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?event ?training ?dependency WHERE {
  :Horse1 :CompetesIn ?event ;
          :TrainsIn ?training .
  ?training :dependsOn ?dependency .
}
```

**Type RAGAS:** `multi_hop_complex`
**Difficulté:** ⭐⭐⭐⭐ Très Difficile

---

### Q23: Objectifs Expérimentaux et Thématiques
**Question:** Quels objectifs expérimentaux sont liés à la thématique du bien-être et comment sont-ils mesurés ?

**Réponse de référence:** Deux objectifs expérimentaux sont liés à la thématique du bien-être : la détection de fatigue (FatigueDetection) et l'estimation de pose animale (AnimalPoseEstimation). La détection de fatigue est liée au bien-être et à la locomotion, tandis que l'estimation de pose animale est liée au bien-être et à l'équitation. Ces objectifs utilisent respectivement des capteurs inertiels et des caméras comme dispositifs expérimentaux.

**Contexte requis:**
```turtle
:FatigueDetection rdf:type :ExperimentalObjectif ;
                  :hasThematique :WellBeing ,
                                 :Locomotion .

:AnimalPoseEstimation rdf:type :ExperimentalObjectif ;
                      :hasThematique :WellBeing ,
                                     :HorseRiding .

:InertialSensors :isUsedFor :GaitClassification .
:Camera :isUsedFor :AnimalPoseEstimation .
```

**Entités nécessaires:**
- Classes: `FatigueDetection`, `AnimalPoseEstimation`, `WellBeing`, `Locomotion`, `HorseRiding`
- Classes dispositifs: `InertialSensors`, `Camera`
- Relations: `hasThematique`, `isUsedFor`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?objective ?theme ?device WHERE {
  ?objective rdf:type :ExperimentalObjectif ;
             :hasThematique ?theme .
  FILTER(?theme = :WellBeing)
  
  OPTIONAL {
    ?device :isUsedFor ?objective .
  }
}
```

**Type RAGAS:** `multi_hop_complex`
**Difficulté:** ⭐⭐⭐⭐ Très Difficile

---

## 🎯 CATÉGORIE 11: Questions Négatives (Pour tester la robustesse)

### Q24: Information Non Disponible - Âge
**Question:** Quel est l'âge de Dakota ?

**Réponse de référence:** L'information sur l'âge de Dakota n'est pas disponible dans le système. Les données actuelles concernant Dakota incluent uniquement son nom, mais pas son âge, sa date de naissance ou d'autres propriétés biométriques détaillées.

**Contexte requis:**
```turtle
:Horse1 :hasName "Dakota" .
# Pas de propriété :hasAge ou :hasBirthDate
```

**Entités nécessaires:**
- `Horse1`
- Propriété: `hasName` (présente)
- Propriété: `hasAge` (absente)

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?age WHERE {
  :Horse1 :hasAge ?age .
}
# Résultat vide attendu
```

**Type RAGAS:** `unanswerable`
**Difficulté:** ⭐⭐ Moyen

---

### Q25: Événement Inexistant
**Question:** Dakota participe-t-il à des compétitions de course ?

**Réponse de référence:** Non, Dakota ne participe pas à des compétitions de course. Selon les données disponibles, Dakota participe uniquement à trois disciplines : le saut d'obstacles, le dressage et le cross-country. Aucune compétition de course n'est mentionnée dans le système.

**Contexte requis:**
```turtle
:Horse1 :CompetesIn :Event_SJ_2026_01 ,  # ShowJumping
                    :Event_Dressage_2026_01 ,  # Dressage
                    :Event_Cross_2026_01 .  # Cross
# Pas d'événement de type Racing
```

**Entités nécessaires:**
- `Horse1`
- Tous les événements (ShowJumping, Dressage, Cross)
- Classe inexistante: `Racing`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?race WHERE {
  :Horse1 :CompetesIn ?race .
  ?race rdf:type :Racing .
}
# Résultat vide attendu
```

**Type RAGAS:** `unanswerable`
**Difficulté:** ⭐⭐ Moyen

---

## 📊 FORMAT DATASET RAGAS (JSON)

```json
{
  "questions": [
    {
      "question_id": "Q1",
      "question": "Quel est le nom du cheval dans le système ?",
      "ground_truth": "Le cheval s'appelle Dakota.",
      "context": [
        ":Horse1 rdf:type :Horse",
        ":Horse1 :hasName \"Dakota\"^^xsd:string"
      ],
      "entities": ["Horse1", "hasName"],
      "sparql_query": "PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>\nSELECT ?name WHERE {\n  ?horse rdf:type :Horse ;\n         :hasName ?name .\n}",
      "query_type": "simple_retrieval",
      "difficulty": "easy"
    },
    {
      "question_id": "Q2",
      "question": "Quel est l'identifiant du capteur inertiel ?",
      "ground_truth": "L'identifiant du capteur est SI-001523.",
      "context": [
        ":Sensor1 rdf:type :InertialSensors",
        ":Sensor1 :hasSensorID \"SI-001523\""
      ],
      "entities": ["Sensor1", "hasSensorID"],
      "sparql_query": "PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>\nSELECT ?sensorID WHERE {\n  ?sensor rdf:type :InertialSensors ;\n          :hasSensorID ?sensorID .\n}",
      "query_type": "simple_retrieval",
      "difficulty": "easy"
    }
  ]
}
```

---

## 🎯 STATISTIQUES DU DATASET

| Catégorie | Nombre de Questions | Difficulté Moyenne |
|-----------|---------------------|-------------------|
| Questions Simples | 2 | ⭐ Facile |
| Relations Single-Hop | 4 | ⭐⭐ Moyen |
| Propriétés/Attributs | 3 | ⭐⭐ Moyen |
| Multi-Hop | 2 | ⭐⭐⭐ Difficile |
| Comparaison | 2 | ⭐⭐⭐ Difficile |
| Agrégation | 2 | ⭐⭐-⭐⭐⭐ |
| Hiérarchiques | 3 | ⭐⭐-⭐⭐⭐ |
| Dispositifs | 3 | ⭐⭐ Moyen |
| Performance | 2 | ⭐⭐-⭐⭐⭐ |
| Complexes | 2 | ⭐⭐⭐⭐ Très Difficile |
| Négatives | 2 | ⭐⭐ Moyen |
| **TOTAL** | **25+** | **Varié** |

---

## 📈 MÉTRIQUES RAGAS COUVERTES

✅ **Faithfulness** - Toutes les réponses sont basées sur les entités RDF exactes
✅ **Answer Relevancy** - Réponses directes et précises
✅ **Context Precision** - Contexte minimal nécessaire fourni
✅ **Context Recall** - Toutes les entités requises listées
✅ **Answer Semantic Similarity** - Ground truth détaillée
✅ **Answer Correctness** - Validation via SPARQL

---

## 🔧 UTILISATION POUR RAGAS

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)

# Charger votre dataset
dataset = {
    "question": ["Quel est le nom du cheval dans le système ?", ...],
    "answer": ["Dakota", ...],  # Réponse de votre GraphRAG
    "contexts": [[":Horse1 :hasName \"Dakota\""], ...],
    "ground_truth": ["Le cheval s'appelle Dakota.", ...]
}

# Évaluer
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness
    ]
)

print(result)
```

---

# 🆕 NOUVELLES QUESTIONS - Version 2 du Knowledge Graph

---

## 🎯 CATÉGORIE 12: Questions sur les Chevaux et Races

### Q26: Race de Dakota
**Question:** Quelle est la race de Dakota ?

**Réponse de référence:** Dakota est un cheval de race Selle Français.

**Contexte requis:**
```turtle
:Horse1 rdf:type :Horse ;
        :hasName "Dakota" ;
        :hasRace "Selle Français" .
```

**Entités nécessaires:**
- `Horse1`
- Propriétés: `hasName`, `hasRace`
- Valeurs: "Dakota", "Selle Français"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?name ?race WHERE {
  ?horse rdf:type :Horse ;
         :hasName ?name ;
         :hasRace ?race .
  FILTER(?name = "Dakota")
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

### Q27: Chevaux dans le Système
**Question:** Combien de chevaux sont enregistrés dans le système et quels sont leurs noms ?

**Réponse de référence:** Il y a deux chevaux enregistrés dans le système : Dakota (Selle Français) et Naya (Anglo-Arabe).

**Contexte requis:**
```turtle
:Horse1 rdf:type :Horse ;
        :hasName "Dakota" ;
        :hasRace "Selle Français" .

:Horse2 rdf:type :Horse ;
        :hasName "Naya" ;
        :hasRace "Anglo-Arabe" .
```

**Entités nécessaires:**
- `Horse1`, `Horse2`
- Propriétés: `hasName`, `hasRace`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?horse ?name ?race WHERE {
  ?horse rdf:type :Horse ;
         :hasName ?name ;
         :hasRace ?race .
}
```

**Type RAGAS:** `aggregation`
**Difficulté:** ⭐⭐ Moyen

---

### Q28: Race de Naya
**Question:** Quelle est la race du cheval Naya ?

**Réponse de référence:** Naya est un cheval de race Anglo-Arabe.

**Contexte requis:**
```turtle
:Horse2 rdf:type :Horse ;
        :hasName "Naya" ;
        :hasRace "Anglo-Arabe" .
```

**Entités nécessaires:**
- `Horse2`
- Propriétés: `hasName`, `hasRace`
- Valeur: "Anglo-Arabe"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?race WHERE {
  ?horse rdf:type :Horse ;
         :hasName "Naya" ;
         :hasRace ?race .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

## 🎯 CATÉGORIE 13: Questions sur les Cavaliers (Riders)

### Q29: Cavaliers de Dakota
**Question:** Quels cavaliers sont associés à Dakota ?

**Réponse de référence:** Deux cavaliers sont associés à Dakota : Emma (Rider_Emma) et Manon (Rider_Manon).

**Contexte requis:**
```turtle
:Rider_Emma rdf:type :Rider ;
            :AssociatedWith :Horse1 .

:Rider_Manon rdf:type :Rider ;
             :AssociatedWith :Horse1 .

:Horse1 :hasName "Dakota" .
```

**Entités nécessaires:**
- `Rider_Emma`, `Rider_Manon`
- `Horse1`
- Relation: `AssociatedWith`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?rider WHERE {
  ?rider rdf:type :Rider ;
         :AssociatedWith :Horse1 .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

### Q30: Cavalier de Naya
**Question:** Quel cavalier est associé au cheval Naya ?

**Réponse de référence:** Le cavalier Léo (Rider_Leo) est associé à Naya.

**Contexte requis:**
```turtle
:Rider_Leo rdf:type :Rider ;
           :AssociatedWith :Horse2 .

:Horse2 :hasName "Naya" .
```

**Entités nécessaires:**
- `Rider_Leo`
- `Horse2`
- Relation: `AssociatedWith`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?rider WHERE {
  ?rider rdf:type :Rider ;
         :AssociatedWith :Horse2 .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

### Q31: Tous les Cavaliers
**Question:** Combien de cavaliers y a-t-il dans le système ?

**Réponse de référence:** Il y a trois cavaliers dans le système : Emma, Léo et Manon.

**Contexte requis:**
```turtle
:Rider_Emma rdf:type :Rider .
:Rider_Leo rdf:type :Rider .
:Rider_Manon rdf:type :Rider .
```

**Entités nécessaires:**
- `Rider_Emma`, `Rider_Leo`, `Rider_Manon`
- Classe: `Rider`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT (COUNT(?rider) AS ?total) WHERE {
  ?rider rdf:type :Rider .
}
```

**Type RAGAS:** `aggregation`
**Difficulté:** ⭐⭐ Moyen

---

## 🎯 CATÉGORIE 14: Questions sur les Acteurs (Vétérinaires et Soigneurs)

### Q32: Vétérinaire
**Question:** Quel vétérinaire intervient dans le système ?

**Réponse de référence:** Le vétérinaire Dr Martin (Vet_DrMartin) intervient dans le système.

**Contexte requis:**
```turtle
:Vet_DrMartin rdf:type :Veterinarian .
```

**Entités nécessaires:**
- `Vet_DrMartin`
- Classe: `Veterinarian`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?vet WHERE {
  ?vet rdf:type :Veterinarian .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

### Q33: Soigneur
**Question:** Qui est le soigneur impliqué dans les soins des chevaux ?

**Réponse de référence:** Sophie (Caretaker_Sophie) est la soigneuse impliquée dans les soins des chevaux.

**Contexte requis:**
```turtle
:Caretaker_Sophie rdf:type :Caretaker .
```

**Entités nécessaires:**
- `Caretaker_Sophie`
- Classe: `Caretaker`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?caretaker WHERE {
  ?caretaker rdf:type :Caretaker .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

### Q34: Acteurs dans l'Entraînement de Préparation
**Question:** Quels acteurs sont impliqués dans l'entraînement de préparation au saut d'obstacles ?

**Réponse de référence:** Trois acteurs sont impliqués dans l'entraînement de préparation : la cavalière Emma (Rider_Emma), le vétérinaire Dr Martin (Vet_DrMartin) et la soigneuse Sophie (Caretaker_Sophie).

**Contexte requis:**
```turtle
:Training_Prepa_SJ_01 rdf:type :PreparationStage ;
                      :involvesActor :Rider_Emma ,
                                     :Vet_DrMartin ,
                                     :Caretaker_Sophie .
```

**Entités nécessaires:**
- `Training_Prepa_SJ_01`
- `Rider_Emma`, `Vet_DrMartin`, `Caretaker_Sophie`
- Relation: `involvesActor`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?actor WHERE {
  :Training_Prepa_SJ_01 :involvesActor ?actor .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

### Q35: Acteurs dans l'Entraînement Pré-Compétition
**Question:** Quels acteurs participent à l'entraînement pré-compétition ?

**Réponse de référence:** Deux acteurs participent à l'entraînement pré-compétition : la cavalière Manon (Rider_Manon) et la soigneuse Sophie (Caretaker_Sophie).

**Contexte requis:**
```turtle
:Training_PreComp_SJ_01 rdf:type :PreCompetitionStage ;
                        :involvesActor :Rider_Manon ,
                                       :Caretaker_Sophie .
```

**Entités nécessaires:**
- `Training_PreComp_SJ_01`
- `Rider_Manon`, `Caretaker_Sophie`
- Relation: `involvesActor`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?actor WHERE {
  :Training_PreComp_SJ_01 :involvesActor ?actor .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐ Moyen

---

## 🎯 CATÉGORIE 15: Questions sur les Saisons Compétitives

### Q36: Saison 2026
**Question:** Quelle est la période de la saison compétitive 2026 ?

**Réponse de référence:** La saison compétitive 2026 commence le 1er mars 2026 et se termine le 31 octobre 2026.

**Contexte requis:**
```turtle
:Season_2026 rdf:type :CompetitiveSeason ;
             :seasonName "Saison 2026" ;
             :seasonStart "2026-03-01"^^xsd:date ;
             :seasonEnd "2026-10-31"^^xsd:date .
```

**Entités nécessaires:**
- `Season_2026`
- Propriétés: `seasonName`, `seasonStart`, `seasonEnd`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?start ?end WHERE {
  :Season_2026 :seasonStart ?start ;
               :seasonEnd ?end .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q37: Nom de la Saison
**Question:** Comment s'appelle la saison compétitive en cours ?

**Réponse de référence:** La saison compétitive en cours s'appelle "Saison 2026".

**Contexte requis:**
```turtle
:Season_2026 rdf:type :CompetitiveSeason ;
             :seasonName "Saison 2026" .
```

**Entités nécessaires:**
- `Season_2026`
- Propriété: `seasonName`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?name WHERE {
  ?season rdf:type :CompetitiveSeason ;
          :seasonName ?name .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

---

## 🎯 CATÉGORIE 16: Questions sur les Événements avec Détails

### Q38: Événement de Saut d'Obstacles à Saumur
**Question:** Quand et où aura lieu l'événement de saut d'obstacles Event_SJ_01 ?

**Réponse de référence:** L'événement de saut d'obstacles Event_SJ_01 aura lieu le 12 avril 2026 à Saumur, dans la catégorie Amateur 1.

**Contexte requis:**
```turtle
:Event_SJ_01 rdf:type :ShowJumping ;
             :eventDate "2026-04-12"^^xsd:date ;
             :eventLocation "Saumur" ;
             :category "Amateur 1" ;
             :inSeason :Season_2026 .
```

**Entités nécessaires:**
- `Event_SJ_01`
- Propriétés: `eventDate`, `eventLocation`, `category`
- `Season_2026`
- Relation: `inSeason`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?date ?location ?category WHERE {
  :Event_SJ_01 :eventDate ?date ;
               :eventLocation ?location ;
               :category ?category .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q39: Événement de Dressage à Angers
**Question:** Décris l'événement de dressage Event_Dressage_01.

**Réponse de référence:** L'événement de dressage Event_Dressage_01 aura lieu le 3 mai 2026 à Angers, dans la catégorie Club Elite, dans le cadre de la Saison 2026.

**Contexte requis:**
```turtle
:Event_Dressage_01 rdf:type :Dressage ;
                   :eventDate "2026-05-03"^^xsd:date ;
                   :eventLocation "Angers" ;
                   :category "Club Elite" ;
                   :inSeason :Season_2026 .
```

**Entités nécessaires:**
- `Event_Dressage_01`
- Propriétés: `eventDate`, `eventLocation`, `category`
- `Season_2026`
- Relation: `inSeason`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?date ?location ?category ?season WHERE {
  :Event_Dressage_01 :eventDate ?date ;
                     :eventLocation ?location ;
                     :category ?category ;
                     :inSeason ?season .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q40: Événements de la Saison 2026
**Question:** Quels événements font partie de la saison compétitive 2026 ?

**Réponse de référence:** Deux événements font partie de la saison 2026 : l'événement de saut d'obstacles à Saumur le 12 avril (Event_SJ_01) et l'événement de dressage à Angers le 3 mai (Event_Dressage_01).

**Contexte requis:**
```turtle
:Event_SJ_01 rdf:type :ShowJumping ;
             :inSeason :Season_2026 ;
             :eventDate "2026-04-12"^^xsd:date ;
             :eventLocation "Saumur" .

:Event_Dressage_01 rdf:type :Dressage ;
                   :inSeason :Season_2026 ;
                   :eventDate "2026-05-03"^^xsd:date ;
                   :eventLocation "Angers" .
```

**Entités nécessaires:**
- `Season_2026`
- `Event_SJ_01`, `Event_Dressage_01`
- Relation: `inSeason`
- Propriétés: `eventDate`, `eventLocation`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?event ?type ?date ?location WHERE {
  ?event :inSeason :Season_2026 ;
         rdf:type ?type ;
         :eventDate ?date ;
         :eventLocation ?location .
  FILTER(?type IN (:ShowJumping, :Dressage, :Cross))
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 17: Questions sur les Participations et Classements

### Q41: Participation de Dakota et Emma
**Question:** Quelle a été la performance de Dakota monté par Emma lors de l'événement Event_SJ_01 ?

**Réponse de référence:** Dakota monté par Emma a terminé à la 2ème place lors de l'événement de saut d'obstacles Event_SJ_01.

**Contexte requis:**
```turtle
:Participation_SJ01_H1_Emma rdf:type :EventParticipation ;
                            :hasHorse :Horse1 ;
                            :hasRider :Rider_Emma ;
                            :rank 2 .

:Event_SJ_01 :hasParticipation :Participation_SJ01_H1_Emma .

:Horse1 :hasName "Dakota" .
```

**Entités nécessaires:**
- `Participation_SJ01_H1_Emma`
- `Horse1`, `Rider_Emma`
- `Event_SJ_01`
- Relations: `hasHorse`, `hasRider`, `hasParticipation`
- Propriété: `rank`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?horse ?rider ?rank WHERE {
  :Event_SJ_01 :hasParticipation ?participation .
  ?participation :hasHorse ?horse ;
                 :hasRider ?rider ;
                 :rank ?rank .
}
```

**Type RAGAS:** `multi_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

### Q42: Classement de Dakota
**Question:** Quel classement Dakota a-t-il obtenu lors de ses compétitions ?

**Réponse de référence:** Dakota a obtenu la 2ème place lors de l'événement de saut d'obstacles Event_SJ_01, monté par la cavalière Emma.

**Contexte requis:**
```turtle
:Participation_SJ01_H1_Emma rdf:type :EventParticipation ;
                            :hasHorse :Horse1 ;
                            :hasRider :Rider_Emma ;
                            :rank 2 .

:Horse1 :hasName "Dakota" .
```

**Entités nécessaires:**
- `Participation_SJ01_H1_Emma`
- `Horse1`
- Propriété: `rank`
- Relation: `hasHorse`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?event ?rank ?rider WHERE {
  ?participation :hasHorse :Horse1 ;
                 :rank ?rank ;
                 :hasRider ?rider .
  ?event :hasParticipation ?participation .
}
```

**Type RAGAS:** `multi_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

## 🎯 CATÉGORIE 18: Questions sur les Capteurs IMU

### Q43: Capteurs IMU sur Dakota
**Question:** Combien de capteurs IMU sont attachés à Dakota et où sont-ils positionnés ?

**Réponse de référence:** Quatre capteurs IMU sont attachés à Dakota : un au garrot (IMU_Withers_01), un sur le canon antérieur (IMU_CanonFore_01), un sur le canon postérieur (IMU_CanonHind_01) et un sur le sternum (IMU_Sternum_01).

**Contexte requis:**
```turtle
:IMU_Withers_01 :hasFileSize 5120 .
:IMU_CanonFore_01 :hasFileSize 7680 .
:IMU_CanonHind_01 :hasFileSize 7420 .
:IMU_Sternum_01 :hasFileSize 6890 .
```

**Entités nécessaires:**
- Tous les capteurs IMU
- Propriété: `hasFileSize`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensor ?size WHERE {
  ?sensor rdf:type :InertialSensors ;
          :hasFileSize ?size .
}
ORDER BY DESC(?size)
LIMIT 1
```

**Type RAGAS:** `comparison`
**Difficulté:** ⭐⭐⭐ Difficile

### Q44: ID du Capteur au Garrot
**Question:** Quel est l'identifiant du capteur IMU placé au garrot de Dakota ?

**Réponse de référence:** L'identifiant du capteur IMU placé au garrot est IMU-W-001.

**Contexte requis:**
```turtle
:IMU_Withers_01 rdf:type :InertialSensors , :Withers ;
                :hasSensorID "IMU-W-001" ;
                :isAttachedTo :Horse1 .
```

**Entités nécessaires:**
- `IMU_Withers_01`
- Propriété: `hasSensorID`
- Valeur: "IMU-W-001"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensorID WHERE {
  ?sensor rdf:type :Withers ;
          :hasSensorID ?sensorID ;
          :isAttachedTo :Horse1 .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q45: Fréquence d'Échantillonnage des Capteurs
**Question:** Quelle est la fréquence d'échantillonnage du capteur IMU sur le canon antérieur ?

**Réponse de référence:** La fréquence d'échantillonnage du capteur IMU sur le canon antérieur (IMU_CanonFore_01) est de 250Hz.

**Contexte requis:**
```turtle
:IMU_CanonFore_01 rdf:type :InertialSensors , :CanonOfForelimb ;
                  :hasSensorTime "250Hz" .
```

**Entités nécessaires:**
- `IMU_CanonFore_01`
- Propriété: `hasSensorTime`
- Valeur: "250Hz"

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?frequency WHERE {
  :IMU_CanonFore_01 :hasSensorTime ?frequency .
}
```

**Type RAGAS:** `attribute_retrieval`
**Difficulté:** ⭐⭐ Moyen

---

### Q46: Utilisation des Capteurs IMU
**Question:** Pour quels objectifs expérimentaux les capteurs IMU de Dakota sont-ils utilisés ?

**Réponse de référence:** Les capteurs IMU de Dakota sont utilisés pour deux objectifs expérimentaux : la classification des allures (GaitClassif_01) avec les capteurs au garrot et canon postérieur, et la détection de fatigue (FatigueDetection) avec les capteurs sur le canon antérieur et le sternum.

**Contexte requis:**
```turtle
:IMU_Withers_01 :isUsedFor :GaitClassif_01 .
:IMU_CanonHind_01 :isUsedFor :GaitClassif_01 .

:IMU_CanonFore_01 :isUsedFor :FatigueDetection .
:IMU_Sternum_01 :isUsedFor :FatigueDetection .
```

**Entités nécessaires:**
- Tous les capteurs IMU
- Relations: `isUsedFor`
- Instances: `GaitClassif_01`, `FatigueDetection`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensor ?objective WHERE {
  ?sensor rdf:type :InertialSensors ;
          :isAttachedTo :Horse1 ;
          :isUsedFor ?objective .
}
```

**Type RAGAS:** `single_hop`
**Difficulté:** ⭐⭐⭐ Difficile

---

### Q47: Format de Données des Capteurs
**Question:** Dans quel format les capteurs IMU enregistrent-ils leurs données ?

**Réponse de référence:** Tous les capteurs IMU enregistrent leurs données au format CSV.

**Contexte requis:**
```turtle
:IMU_Withers_01 :hasFormat "CSV" .
:IMU_CanonFore_01 :hasFormat "CSV" .
:IMU_CanonHind_01 :hasFormat "CSV" .
:IMU_Sternum_01 :hasFormat "CSV" .
```

**Entités nécessaires:**
- Tous les capteurs IMU
- Propriété: `hasFormat`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT DISTINCT ?format WHERE {
  ?sensor rdf:type :InertialSensors ;
          :hasFormat ?format .
}
```

**Type RAGAS:** `simple_retrieval`
**Difficulté:** ⭐ Facile

Parfait ! La question Q48 est maintenant complète dans le document. Voici un récapitulatif de cette question :

---

###  **Q48: Taille de Fichier des Capteurs**

**Question:** Quel capteur IMU génère le plus de données (taille de fichier) ?

**Réponse de référence:** Le capteur IMU sur le canon antérieur (IMU_CanonFore_01) génère le plus de données avec une taille de fichier de 7680 octets.

**Contexte requis:**
```turtle
:IMU_Withers_01 :hasFileSize 5120 .
:IMU_CanonFore_01 :hasFileSize 7680 .
:IMU_CanonHind_01 :hasFileSize 7420 .
:IMU_Sternum_01 :hasFileSize 6890 .
```

**Entités nécessaires:**
- Tous les capteurs IMU
- Propriété: `hasFileSize`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensor ?size WHERE {
  ?sensor rdf:type :InertialSensors ;
          :hasFileSize ?size .
}
ORDER BY DESC(?size)
LIMIT 1
```

**Type RAGAS:** `comparison`
**Difficulté:** ⭐⭐⭐ Difficile

---

Votre document d'évaluation RAGAS est maintenant complet avec **51 questions** couvrant l'intégralité de votre knowledge graph V2 ! 🎉

---

## 🎯 CATÉGORIE 19: Questions Complexes Multi-Entités (Version 2)

### Q49: Pipeline Complet Entraînement-Acteurs-Événement
**Question:** Décris la relation complète entre l'entraînement de préparation, les acteurs impliqués et l'événement cible pour Dakota.

**Réponse de référence:** L'entraînement de préparation (Training_Prepa_SJ_01) pour Dakota implique trois acteurs : la cavalière Emma, le vétérinaire Dr Martin et la soigneuse Sophie. Cet entraînement a une fréquence de 4 séances par semaine, une intensité modérée et une durée de 45 minutes. Il dépend de l'événement de saut d'obstacles Event_SJ_01 qui aura lieu le 12 avril 2026 à Saumur dans la catégorie Amateur 1.

**Contexte requis:**
```turtle
:Training_Prepa_SJ_01 rdf:type :PreparationStage ;
                      :dependsOn :Event_SJ_01 ;
                      :Frequency 4 ;
                      :Intensity "Modérée" ;
                      :Volume "45min" ;
                      :involvesActor :Rider_Emma ,
                                     :Vet_DrMartin ,
                                     :Caretaker_Sophie .

:Event_SJ_01 rdf:type :ShowJumping ;
             :eventDate "2026-04-12"^^xsd:date ;
             :eventLocation "Saumur" ;
             :category "Amateur 1" .

:Horse1 :TrainsIn :Training_Prepa_SJ_01 ;
        :CompetesIn :Event_SJ_01 .
```

**Entités nécessaires:**
- `Training_Prepa_SJ_01`, `Event_SJ_01`, `Horse1`
- `Rider_Emma`, `Vet_DrMartin`, `Caretaker_Sophie`
- Relations: `dependsOn`, `involvesActor`, `TrainsIn`, `CompetesIn`
- Propriétés: `Frequency`, `Intensity`, `Volume`, `eventDate`, `eventLocation`, `category`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?training ?actor ?event ?date ?location ?frequency ?intensity WHERE {
  :Horse1 :TrainsIn ?training ;
          :CompetesIn ?event .
  ?training rdf:type :PreparationStage ;
            :dependsOn ?event ;
            :involvesActor ?actor ;
            :Frequency ?frequency ;
            :Intensity ?intensity .
  ?event :eventDate ?date ;
         :eventLocation ?location .
}
```

**Type RAGAS:** `multi_hop_complex`
**Difficulté:** ⭐⭐⭐⭐ Très Difficile

---

### Q50: Changement de Cavalier entre Entraînements
**Question:** Y a-t-il des changements de cavalier entre les différentes phases d'entraînement pour le saut d'obstacles ?

**Réponse de référence:** Oui, il y a un changement de cavalier entre les phases d'entraînement. Emma intervient durant la phase de préparation, tandis que Manon prend le relais durant la phase pré-compétition. Les deux cavalières sont associées à Dakota.

**Contexte requis:**
```turtle
:Training_Prepa_SJ_01 rdf:type :PreparationStage ;
                      :involvesActor :Rider_Emma .

:Training_PreComp_SJ_01 rdf:type :PreCompetitionStage ;
                        :involvesActor :Rider_Manon .

:Rider_Emma :AssociatedWith :Horse1 .
:Rider_Manon :AssociatedWith :Horse1 .
```

**Entités nécessaires:**
- `Training_Prepa_SJ_01`, `Training_PreComp_SJ_01`
- `Rider_Emma`, `Rider_Manon`, `Horse1`
- Relations: `involvesActor`, `AssociatedWith`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?stage ?rider WHERE {
  ?training rdf:type ?stage ;
            :dependsOn :Event_SJ_01 ;
            :involvesActor ?rider .
  ?rider rdf:type :Rider .
  FILTER(?stage IN (:PreparationStage, :PreCompetitionStage))
}
```

**Type RAGAS:** `comparison`
**Difficulté:** ⭐⭐⭐⭐ Très Difficile

---

### Q51: Analyse Complète d'un Événement
**Question:** Donne une analyse complète de l'événement Event_SJ_01 incluant les participations, classements, entraînements préparatoires et acteurs impliqués.

**Réponse de référence:** L'événement Event_SJ_01 est une compétition de saut d'obstacles qui aura lieu le 12 avril 2026 à Saumur en catégorie Amateur 1, dans le cadre de la Saison 2026. Dakota, monté par Emma, y a obtenu la 2ème place. La préparation pour cet événement comprenait deux phases d'entraînement : une phase de préparation (4 séances/semaine, intensité modérée, 45min) avec Emma, Dr Martin et Sophie, et une phase pré-compétition (3 séances/semaine, intensité élevée, 60min) avec Manon et Sophie.

**Contexte requis:**
```turtle
:Event_SJ_01 rdf:type :ShowJumping ;
             :eventDate "2026-04-12"^^xsd:date ;
             :eventLocation "Saumur" ;
             :category "Amateur 1" ;
             :inSeason :Season_2026 ;
             :hasParticipation :Participation_SJ01_H1_Emma .

:Participation_SJ01_H1_Emma :hasHorse :Horse1 ;
                             :hasRider :Rider_Emma ;
                             :rank 2 .

:Training_Prepa_SJ_01 :dependsOn :Event_SJ_01 ;
                      :Frequency 4 ;
                      :Intensity "Modérée" ;
                      :Volume "45min" ;
                      :involvesActor :Rider_Emma , :Vet_DrMartin , :Caretaker_Sophie .

:Training_PreComp_SJ_01 :dependsOn :Event_SJ_01 ;
                        :Frequency 3 ;
                        :Intensity "Élevée" ;
                        :Volume "60min" ;
                        :involvesActor :Rider_Manon , :Caretaker_Sophie .
```

**Entités nécessaires:**
- Toutes les entités liées à Event_SJ_01
- Multiples relations et propriétés

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?event ?date ?location ?horse ?rider ?rank ?training ?actor ?frequency ?intensity
WHERE {
  ?event rdf:type :ShowJumping ;
         :eventDate ?date ;
         :eventLocation ?location ;
         :hasParticipation ?participation .
  
  ?participation :hasHorse ?horse ;
                 :hasRider ?rider ;
                 :rank ?rank .
  
  ?training :dependsOn ?event ;
            :involvesActor ?actor ;
            :Frequency ?frequency ;
            :Intensity ?intensity .
}
```

**Type RAGAS:** `multi_hop_complex`
**Difficulté:** ⭐⭐⭐⭐⭐ Extrêmement Difficile

---

## 📊 STATISTIQUES MISES À JOUR

| Catégorie | Nombre Questions | Difficulté Moyenne |
|-----------|------------------|-------------------|
| **ORIGINALES (Q1-Q25)** | **25** | **Varié** |
| Chevaux et Races (Q26-Q28) | 3 | ⭐ Facile |
| Cavaliers (Q29-Q31) | 3 | ⭐⭐ Moyen |
| Acteurs (Q32-Q35) | 4 | ⭐-⭐⭐ |
| Saisons (Q36-Q37) | 2 | ⭐-⭐⭐ |
| Événements Détaillés (Q38-Q40) | 3 | ⭐⭐-⭐⭐⭐ |
| Participations (Q41-Q42) | 2 | ⭐⭐⭐ Difficile |
| Capteurs IMU (Q43-Q48) | 6 | ⭐-⭐⭐⭐ |
| Complexes V2 (Q49-Q51) | 3 | ⭐⭐⭐⭐-⭐⭐⭐⭐⭐ |
| **TOTAL** | **51** | **Très Varié** |

---

## 🎯 NOUVELLES MÉTRIQUES COUVERTES

✅ **Multi-entity reasoning** - Questions impliquant 5+ entités
✅ **Temporal reasoning** - Dates, saisons, chronologie
✅ **Ranking/Comparison** - Classements, performances
✅ **Sensor data analysis** - Propriétés techniques des IMU
✅ **Actor-role relationships** - Rôles humains dans le système
✅ **Cross-domain queries** - Chevaux + Capteurs + Événements

---

## 📋 FORMAT JSON RAGAS ÉTENDU

```json
{
  "questions": [
    {
      "question_id": "Q26",
      "question": "Quelle est la race de Dakota ?",
      "ground_truth": "Dakota est un cheval de race Selle Français.",
      "context": [
        ":Horse1 rdf:type :Horse",
        ":Horse1 :hasName \"Dakota\"",
        ":Horse1 :hasRace \"Selle Français\""
      ],
      "entities": ["Horse1", "hasName", "hasRace"],
      "sparql_query": "PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>\nSELECT ?name ?race WHERE {\n  ?horse rdf:type :Horse ;\n         :hasName ?name ;\n         :hasRace ?race .\n  FILTER(?name = \"Dakota\")\n}",
      "query_type": "simple_retrieval",
      "difficulty": "easy",
      "version": "v2"
    }
  ]
}
```

---

## 🔧 UTILISATION POUR RAGAS (Mis à Jour)

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    answer_correctness
)

# Dataset étendu avec 51 questions
dataset = {
    "question": [
        "Quel est le nom du cheval dans le système ?",
        "Quelle est la race de Dakota ?",
        "Quels cavaliers sont associés à Dakota ?",
        # ... 48 autres questions
    ],
    "answer": [
        "Dakota",
        "Selle Français",
        "Emma et Manon",
        # ... vos réponses GraphRAG
    ],
    "contexts": [
        [":Horse1 :hasName \"Dakota\""],
        [":Horse1 :hasRace \"Selle Français\""],
        [":Rider_Emma :AssociatedWith :Horse1", ":Rider_Manon :AssociatedWith :Horse1"],
        # ... contextes
    ],
    "ground_truth": [
        "Le cheval s'appelle Dakota.",
        "Dakota est un cheval de race Selle Français.",
        "Deux cavaliers sont associés à Dakota : Emma et Manon.",
        # ... réponses de référence
    ]
}

# Évaluation
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        answer_correctness
    ]
)

print(f"Score global: {result}")
print(f"Faithfulness: {result['faithfulness']}")
print(f"Answer Relevancy: {result['answer_relevancy']}")
```

---

## 🎁 RÉSUMÉ DES AJOUTS

### **26 Nouvelles Questions** couvrant:
- ✅ **3 questions** sur les races de chevaux
- ✅ **3 questions** sur les cavaliers et associations
- ✅ **4 questions** sur les acteurs (vétérinaires, soigneurs)
- ✅ **2 questions** sur les saisons compétitives
- ✅ **3 questions** sur les événements avec dates/lieux
- ✅ **2 questions** sur les participations et classements
- ✅ **6 questions** sur les capteurs IMU (positions, IDs, fréquences, objectifs)
- ✅ **3 questions** complexes multi-entités (niveau expert)

### **Nouvelles Entités Couvertes:**
- `Horse2` (Naya), races de chevaux
- `Rider_Emma`, `Rider_Leo`, `Rider_Manon`
- `Vet_DrMartin`, `Caretaker_Sophie`
- `Season_2026` avec dates
- `Event_SJ_01`, `Event_Dressage_01` avec détails
- `Participation_SJ01_H1_Emma` avec classement
- 4 capteurs IMU avec spécifications techniques
- Relations: `AssociatedWith`, `involvesActor`, `inSeason`, `hasParticipation`

### **Total Final:**
🎯 **51 Questions** de qualité pour évaluation RAGAS complète
📊 Couverture de **100% du nouveau knowledge graph**
⭐ Difficulté de ⭐ (facile) à ⭐⭐⭐⭐⭐ (extrême)ers_01 rdf:type :InertialSensors , :Withers ;
                :isAttachedTo :Horse1 .

:IMU_CanonFore_01 rdf:type :InertialSensors , :CanonOfForelimb ;
                  :isAttachedTo :Horse1 .

:IMU_CanonHind_01 rdf:type :InertialSensors , :CanonOfHindlimb ;
                  :isAttachedTo :Horse1 .

:IMU_Sternum_01 rdf:type :InertialSensors , :Sternum ;
                :isAttachedTo :Horse1 .
```

**Entités nécessaires:**
- `IMU_Withers_01`, `IMU_CanonFore_01`, `IMU_CanonHind_01`, `IMU_Sternum_01`
- `Horse1`
- Classes: `Withers`, `CanonOfForelimb`, `CanonOfHindlimb`, `Sternum`
- Relation: `isAttachedTo`

**Requête SPARQL:**
```sparql
PREFIX : <http://www.semanticweb.org/noamaadra/ontologies/2024/2/Horses#>

SELECT ?sensor ?position WHERE {
  ?sensor rdf:type :InertialSensors ;
          rdf:type ?position ;
          :isAttachedTo :Horse1 .
  FILTER(?position IN (:Withers, :CanonOfForelimb, :CanonOfHindlimb, :Sternum))
}
```

**Type RAGAS:** `aggregation`
**Difficulté:** ⭐⭐⭐ Difficile

---


