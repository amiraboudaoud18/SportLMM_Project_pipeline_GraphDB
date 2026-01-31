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