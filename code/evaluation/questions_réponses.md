# Manual Evaluation Results - Horse Ontology System

**Generation Date:** 2026-01-15T15:51:58.988607  
**Total Questions:** 40  
**Dataset Version:** 2.1_corrected  
**Success Rate:** 100.0%

---

## Q1
**Question:** Quels sont les noms des chevaux dans le système ?

**Ground Truth:** Les chevaux dans le système sont Dakota et Naya.

**Answer:** Les noms des chevaux dans le système sont :

* Dakota
* Naya

Ces deux chevaux sont présents dans la base de données du système.

---

## Q2
**Question:** Quelle est la race de Dakota ?

**Ground Truth:** Dakota est un cheval de race Selle Français.

**Answer:** La race de Dakota est connue.

* La race de Dakota est le Selle Français.

---

## Q3
**Question:** Quelle est la race de Naya ?

**Ground Truth:** Naya est un cheval de race Anglo-Arabe.

**Answer:** La race de Naya est connue.

* La race de Naya est l'Anglo-Arabe (propriété hasRace).

---

## Q4
**Question:** Dans quels événements sportifs Dakota participe-t-il ?

**Ground Truth:** Dakota participe à deux événements sportifs : Event_SJ_01 (saut d'obstacles) et Event_Dressage_01 (dressage).

**Answer:** Dakota participe à plusieurs événements sportifs équestres. Voici les détails :

1. **Saut d'obstacles** : Dakota participe à l'événement de saut d'obstacles (Event_SJ_2026_01) et à l'événement de saut d'obstacles (Event_SJ_01).
2. **Dressage** : Dakota participe au dressage (Event_Dressage_2026_01) et au dressage (Event_Dressage_01).
3. **Cross-country** : Dakota participe à la cross-country (Event_Cross_2026_01).

Ces informations sont basées sur les 5 événements sportifs enregistrés dans le contexte fourni.

---

## Q5
**Question:** Quelles étapes d'entraînement Dakota suit-il ?

**Ground Truth:** Dakota suit deux étapes d'entraînement : Training_Prepa_SJ_01 (préparation) et Training_PreComp_SJ_01 (pré-compétition).

**Answer:** Dakota suit plusieurs étapes d'entraînement pour améliorer ses compétences en saut d'obstacles.

Voici les différentes étapes d'entraînement suivies par Dakota :

1. **Phase de préparation** (Training_Preparation_SJ_01) : 
   - Fréquence : 4 séances par semaine
   - Intensité : Modérée
   - Durée : 45 minutes

2. **Phase de pré-compétition** (Training_PreCompetition_SJ_01 et Training_PreComp_SJ_01) :
   - Fréquence : 3 séances par semaine pour la première, intensité non spécifiée mais mentionné comme étant une phase de pré-compétition
   - Intensité : Élevée pour la deuxième

3. **Phase de compétition** (Training_Competition_SJ_01) :
   - Fréquence : 1 séance par semaine
   - Intensité : Peak
   - Durée : 30 minutes

4. **Transition** (Training_Transition_SJ_01) :
   - Fréquence : 2 séances par semaine
   - Intensité : Faible

5. **Phase de préparation spécifique** (Training_Prepa_SJ_01) :
   - Intensité : Modérée

---

## Q6
**Question:** Quelle est la fréquence d'entraînement pendant la phase de préparation ?

**Ground Truth:** Pendant la phase de préparation, la fréquence d'entraînement est de 4 séances par semaine.

**Answer:** La fréquence d'entraînement pendant la phase de préparation est de 4 séances par semaine.

En effet, deux programmes d'entraînement sont définis pour cette phase :

1. Training_Preparation_SJ_01 avec une fréquence de 4 séances par semaine
2. Training_Prepa_SJ_01 (fréquence non spécifiée)

Il est à noter que la fréquence n'est mentionnée que pour le premier programme d'entraînement, et pas pour le deuxième.

---

## Q7
**Question:** Quelle est l'intensité d'entraînement durant la phase pré-compétition ?

**Ground Truth:** Durant la phase pré-compétition, l'intensité d'entraînement est élevée.

**Answer:** L'intensité d'entraînement durant la phase pré-compétition est élevée.

Voici les détails :

* Élevée (Résultat 2)
* Haute (Résultat 1)

---

## Q8
**Question:** Quelle est la durée des séances pendant la phase de préparation ?

**Ground Truth:** Pendant la phase de préparation, les séances durent 45 minutes.

**Answer:** La durée des séances pendant la phase de préparation est de 45 minutes.

En effet, les deux instances de PreparationStage ont une propriété Volume définie comme suit :

- Résultat 1 : 45min
- Résultat 2 : 45min

---

## Q9
**Question:** Quelle est la durée des séances pendant la phase pré-compétition ?

**Ground Truth:** Pendant la phase pré-compétition, les séances durent 60 minutes.

**Answer:** La durée des séances pendant la phase pré-compétition est de 60 minutes.

Voici les détails :

* La durée de chaque séance est fixée à 60 minutes.
* Il n'y a pas d'autres informations disponibles sur la durée des séances pendant cette phase.

---

## Q10
**Question:** De quel événement dépendent les étapes d'entraînement de Dakota ?

**Ground Truth:** Les deux étapes d'entraînement de Dakota (préparation et pré-compétition) dépendent de l'événement de saut d'obstacles Event_SJ_01.

**Answer:** Je suis désolé, mais je n'ai pas trouvé d'informations dans le graphe de connaissances qui déterminent les étapes d'entraînement de Dakota.

Il est possible que ces informations n'aient pas encore été ajoutées à la base de données ou qu'elles ne soient pas disponibles. Si vous avez besoin d'informations sur un autre sujet, je serais ravi de l'aider !

---

## Q11
**Question:** Combien de capteurs IMU sont attachés à Dakota ?

**Ground Truth:** 4 capteurs IMU sont attachés à Dakota.

**Answer:** Dakota a un total de 4 capteurs IMU attachés.

Voici les informations détaillées :

* Nombre de capteurs IMU : 4
* (Aucune information supplémentaire n'est disponible sur ces capteurs)

---

## Q12
**Question:** Quels sont les identifiants des capteurs IMU ?

**Ground Truth:** Les identifiants des capteurs IMU sont : IMU-W-001, IMU-CF-002, IMU-CH-003 et IMU-ST-004.

**Answer:** Les identifiants des capteurs IMU sont :

* SI-001523
* IMU-W-001
* IMU-CF-002
* IMU-CH-003
* IMU-ST-004

Ces identifiants correspondent à différents types de capteurs IMU (inertial measurement units) qui enregistrent les données de mouvement et d'orientation.

---

## Q13
**Question:** À quelles positions anatomiques les capteurs IMU sont-ils placés sur Dakota ?

**Ground Truth:** Les capteurs IMU sont placés à 4 positions : garrot (Withers), canon antérieur (CanonOfForelimb), canon postérieur (CanonOfHindlimb) et sternum (Sternum).

**Answer:** Je vais essayer de répondre à votre question.

Les capteurs IMU sont placés sur Dakota à différentes positions anatomiques. Voici les positions identifiées :

* Le canon de la jambe avant (CanonOfForelimb)
* Le canon de la jambe arrière (CanonOfHindlimb)
* L'épaule (pas explicitement mentionné, mais il s'agit probablement d'une position proche)
* La poitrine (Sternum)

Il est important de noter que les positions "node5", "node6", etc. ne sont pas des positions anatomiques spécifiques et correspondent probablement à des emplacements génériques sur le cheval.

Je n'ai trouvé aucune information indiquant que les capteurs IMU soient placés sur la tête, le dos ou d'autres parties du corps de Dakota.


---

## Q14
**Question:** Quel est l'identifiant du capteur IMU placé au garrot ?

**Ground Truth:** L'identifiant du capteur IMU placé au garrot est IMU-W-001.

**Answer:** L'identifiant du capteur IMU placé au garrot est le suivant :

* L'identifiant du capteur IMU est : IMU-W-001 (type 'Withers').

Cette information est trouvée en utilisant la propriété 'hasSensorID'.

---

## Q15
**Question:** Quelle est la fréquence d'échantillonnage du capteur IMU au sternum ?

**Ground Truth:** La fréquence d'échantillonnage du capteur IMU au sternum est de 200 Hz.

**Answer:** La fréquence d'échantillonnage du capteur IMU au sternum est de 200 Hz.

Cela signifie que le capteur collecte des données à une cadence très élevée, ce qui permet une précision et une fiabilité optimales pour suivre les mouvements du cheval.

---

## Q16
**Question:** Quel capteur a la fréquence d'échantillonnage la plus élevée ?

**Ground Truth:** Le capteur IMU_CanonFore_01 (canon antérieur) a la fréquence d'échantillonnage la plus élevée avec 250 Hz.

**Answer:** Le capteur ayant la fréquence d'échantillonnage la plus élevée est l'IMU_CanonFore_01.

Voici les détails du capteur :

* Identifiant : IMU_CanonFore_01
* Fréquence d'échantillonnage : 250 Hz

Cela signifie que le capteur IMU_CanonFore_01 prend des mesures à une fréquence de 250 fois par seconde.

---

## Q17
**Question:** Quels cavaliers sont associés à Dakota ?

**Ground Truth:** Deux cavaliers sont associés à Dakota : Emma et Manon.

**Answer:** Dakota est associé à deux cavaliers.

1. Emma (Rider_Emma)
2. Manon (Rider_Manon)

---

## Q18
**Question:** Quel cavalier est associé à Naya ?

**Ground Truth:** Le cavalier Leo est associé à Naya.

**Answer:** Le cavalier associé au cheval Naya est :

* Le cavalier Leo (Rider_Leo) 

C'est le seul résultat trouvé dans le graphe de connaissances.

---

## Q19
**Question:** Combien de cavaliers différents sont dans le système ?

**Ground Truth:** Il y a 3 cavaliers différents dans le système : Emma, Manon et Leo.

**Answer:** Il y a 3 cavaliers différents dans le système.

Voici les détails :

* Le nombre total de cavaliers est de 3 (selon la requête).
* Il s'agit d'individus du type "horses:Rider" (cavalier).

---

## Q20
**Question:** Qui est le vétérinaire impliqué dans les soins des chevaux ?

**Ground Truth:** Le Dr Martin est le vétérinaire impliqué dans les soins des chevaux.

**Answer:** Le vétérinaire impliqué dans les soins des chevaux est :

* Dr Martin (Vet_DrMartin) 

Il s'agit d'un vétérinaire qui est impliqué dans les entraînements des chevaux, ce qui suggère qu'il prend en charge la santé et le bien-être de ces animaux.

---

## Q21
**Question:** Qui est le soigneur responsable des chevaux ?

**Ground Truth:** Sophie est la soigneuse responsable des chevaux.

**Answer:** La personne responsable des chevaux est Sophie.

Elle est soigneur (Caretaker) qui participe aux entraînements (Training). 

Voici les informations disponibles sur elle :

* Elle s'appelle Caretaker_Sophie.

---

## Q22
**Question:** Quels acteurs humains sont impliqués dans la phase de préparation de l'entraînement ?

**Ground Truth:** Trois acteurs sont impliqués dans la phase de préparation : Emma (cavalière), Dr Martin (vétérinaire) et Sophie (soigneuse).

**Answer:** Les acteurs humains impliqués dans la phase de préparation de l'entraînement sont :

1. Emma, le cavalier (Rider_Emma)
2. Dr Martin, le vétérinaire (Vet_DrMartin) 
3. Sophie, la personne chargée des soins aux chevaux (Caretaker_Sophie)

Ils jouent tous un rôle clé dans l'entraînement et la préparation des chevaux avant les compétitions.

---

## Q23
**Question:** Qui participe à la phase pré-compétition de l'entraînement ?

**Ground Truth:** Deux personnes participent à la phase pré-compétition : Manon (cavalière) et Sophie (soigneuse).

**Answer:** Les personnes qui participent à la phase pré-compétition de l'entraînement sont :

1. Rider_Manon (rider)
2. Caretaker_Sophie (soigneur)

---

## Q24
**Question:** Quelle est la période de la saison 2026 ?

**Ground Truth:** La saison 2026 s'étend du 1er mars 2026 au 31 octobre 2026.

**Answer:** La période de la saison 2026 est du **1er mars** au **31 octobre**.

* Cette période correspond à la phase de compétition (CompetitiveSeason) pour l'année 2026.
* Le début de la saison est fixé le 1er mars 2026.
* La fin de la saison est fixée le 31 octobre 2026.

---

## Q25
**Question:** Quels événements font partie de la saison 2026 ?

**Ground Truth:** Deux événements font partie de la saison 2026 : Event_SJ_01 (saut d'obstacles) et Event_Dressage_01 (dressage).

**Answer:** La saison 2026 comprend deux événements sportifs.

1. Saut d'obstacles : Dakota participe à l'événement de saut d'obstacles (Event_SJ_01)
2. Dressage : Dakota participe au dressage (Event_Dressage_01)

---

## Q26
**Question:** Quelle est la date de l'événement Event_SJ_01 ?

**Ground Truth:** L'événement Event_SJ_01 aura lieu le 12 avril 2026.

**Answer:** La date de l'événement "Event_SJ_01" est connue.

Voici les informations disponibles :

1. La date de l'événement Event_SJ_01 est le 12 avril 2026.
(Le format de la date est en format ISO : année-mois-jour)

---

## Q27
**Question:** Où se déroule l'événement de saut d'obstacles Event_SJ_01 ?

**Ground Truth:** L'événement Event_SJ_01 se déroule à Saumur.

**Answer:** L'événement de saut d'obstacles Event_SJ_01 se déroule à Saumur.

* Lieu : Saumur
* (Cette information est disponible dans la propriété eventLocation)

---

## Q28
**Question:** Où se déroule l'événement de dressage Event_Dressage_01 ?

**Ground Truth:** L'événement Event_Dressage_01 se déroule à Angers.

**Answer:** L'événement de dressage Event_Dressage_01 se déroule à Angers.

* L'emplacement exact est : Angers.

---

## Q29
**Question:** Quelle est la catégorie de l'événement Event_SJ_01 ?

**Ground Truth:** L'événement Event_SJ_01 est de catégorie Amateur 1.

**Answer:** La catégorie de l'événement Event_SJ_01 est :

* Amateur 1 (catégorie réservée aux cavaliers amateurs)

---

## Q30
**Question:** Quelle est la catégorie de l'événement Event_Dressage_01 ?

**Ground Truth:** L'événement Event_Dressage_01 est de catégorie Club Elite.

**Answer:** La catégorie de l'événement Event_Dressage_01 est le club élite.

* C'est une compétition pour les chevaux éligibles au niveau Club Elite (détail : pas d'information supplémentaire disponible sur ce contexte).

---

## Q31
**Question:** Quel classement Dakota et Emma ont-ils obtenu à Event_SJ_01 ?

**Ground Truth:** Dakota et Emma ont obtenu la 2ème place à Event_SJ_01.

**Answer:** Dakota a obtenu un classement dans l'événement de saut d'obstacles (Event_SJ_01).

Voici les détails du classement :

1. Dakota est classé 2ème.

Il n'y a pas d'information sur le classement d'Emma dans ce contexte.

---

## Q32
**Question:** Compare les fréquences d'entraînement entre la phase de préparation et la phase pré-compétition.

**Ground Truth:** La phase de préparation a une fréquence de 4 séances par semaine, tandis que la phase pré-compétition a une fréquence de 3 séances par semaine. La préparation est légèrement plus intensive en termes de fréquence.

**Answer:** **Comparaison des fréquences d'entraînement entre la phase de préparation et la phase pré-compétition**

Les données disponibles permettent une comparaison limitée entre les deux phases étudiées.

* **Phase de préparation (PreparationStage)** : 
 + La fréquence d'entraînement est de 4 fois.
 + Il y a au moins deux types d'entraînement correspondants avec cette fréquence.

* **Phase pré-compétition (PreCompetitionStage)** :
 + La fréquence d'entraînement est de 3 fois.
 + Il y a au moins deux types d'entraînement correspondants avec cette fréquence.

Il n'est pas possible de déterminer si les types d'entraînement sont identiques ou non entre les deux phases étudiées.

---

## Q33
**Question:** Quelles sont les différences entre les phases de préparation et de pré-compétition en termes de fréquence, intensité et durée ?

**Ground Truth:** La phase de préparation a 4 séances/semaine avec intensité modérée pendant 45min. La phase pré-compétition a 3 séances/semaine avec intensité élevée pendant 60min. La pré-compétition est plus intense et plus longue, mais moins fréquente.

**Answer:** Les différences entre les phases de préparation et de pré-compétition sont notables en termes de fréquence, intensité et durée.

Voici les principales différences :

* Fréquence :
 + Phase de préparation : 4 fois par semaine (Résultat 1 et Résultat 2)
 + Phase de pré-compétition : 3 fois par semaine (Résultat 3 et Résultat 4)

* Intensité :
 + Phase de préparation : Modérée (Résultat 1) ou Modérée (Résultat 2)
 + Phase de pré-compétition : Élevée (Résultat 3) ou Élevée (Résultat 4)

* Durée :
 + Phase de préparation : 45 minutes par séance
 + Phase de pré-compétition : 60 minutes par séance

En résumé, la phase de pré-compétition est caractérisée par une fréquence plus faible, une intensité plus élevée et une durée plus longue que la phase de préparation.

---

## Q34
**Question:** Compare les acteurs impliqués dans les phases de préparation et de pré-compétition.

**Ground Truth:** La phase de préparation implique Emma (cavalière), Dr Martin (vétérinaire) et Sophie (soigneuse), soit 3 acteurs. La phase pré-compétition implique Manon (cavalière) et Sophie (soigneuse), soit 2 acteurs. Sophie est la seule personne commune aux deux phases. Emma et Dr Martin ne participent qu'à la préparation, tandis que Manon ne participe qu'à la pré-compétition.

**Answer:** **Comparaison des acteurs impliqués dans les phases de préparation et de pré-compétition**

Les acteurs impliqués dans les phases de préparation et de pré-compétition sont différents.

**Acteurs impliqués dans la phase de préparation :**

* Rider_Emma (type : Humain, Cavalier)
* Vet_DrMartin (type : Vétérinaire, Humain)
* Caretaker_Sophie (type : Soigneur, Humain)

(Le type "node15", "node103", "node208" et "node305" n'est pas clairement identifié dans le contexte fourni.)

**Acteurs impliqués dans la phase de pré-compétition :**

* Rider_Manon (type : Humain, Cavalier)
* Caretaker_Sophie (type : Soigneur)

(Le type "node15", "node103", "node208" et "node305" n'est pas clairement identifié dans le contexte fourni.)

Il est notable que Rider_Emma et Vet_DrMartin sont présents uniquement dans la phase de préparation, tandis que Rider_Manon et Caretaker_Sophie sont présents uniquement dans la phase de pré-compétition.

---

## Q35
**Question:** Donne une analyse complète de l'événement Event_SJ_01.

**Ground Truth:** L'événement Event_SJ_01 est une compétition de saut d'obstacles qui aura lieu le 12 avril 2026 à Saumur en catégorie Amateur 1, dans le cadre de la Saison 2026. Dakota, monté par Emma, y a obtenu la 2ème place. La préparation pour cet événement comprenait deux phases d'entraînement : une phase de préparation (4 séances/semaine, intensité modérée, 45min) avec Emma, Dr Martin et Sophie, et une phase pré-compétition (3 séances/semaine, intensité élevée, 60min) avec Manon et Sophie.

**Answer:** Analyse complète de l'événement Event_SJ_01 :

L'événement Event_SJ_01 a lieu le 12 avril 2026 à Saumur.

**Informations générales**

* Date : 12 avril 2026
* Lieu : Saumur

**Catégorie et période de saison**

* Catégorie : Amateur 1
* Période de saison : du 1er mars au 31 octobre 2026

**Capteurs attachés aux chevaux**

* IMU-W-001 (fréquence : 200Hz)
* IMU-CF-002 (fréquence : 250Hz)
* IMU-CH-003 (fréquence : 250Hz)
* IMU-ST-004 (fréquence : 200Hz)

**Remarque**

Il n'y a pas d'informations disponibles sur les cavaliers associés à cet événement.

---

## Q36
**Question:** Combien d'événements sportifs sont enregistrés dans le système ?

**Ground Truth:** Il y a 2 événements sportifs enregistrés dans le système : un événement de saut d'obstacles (Event_SJ_01) et un événement de dressage (Event_Dressage_01).

**Answer:** 
Il y a 5 événements sportifs enregistrés dans le système.

* Événements sportifs comptabilisés : 5
* Types d'événements potentiels : SportingEvent (pas d'informations supplémentaires disponibles sur les types spécifiques)

---

## Q37
**Question:** Quels types d'événements sportifs sont disponibles dans l'ontologie ?

**Ground Truth:** Les événements sportifs dans l'ontologie incluent le saut d'obstacles (ShowJumping) et le dressage (Dressage).

**Answer:** Les types d'événements sportifs disponibles dans l'ontologie sont :

1. **Saut d'obstacles** (ShowJumping)
2. **Cross-country** (Cross)
3. **Dressage**
4. **Événement sportif général** (SportingEvent)

Ces types correspondent aux sous-classes de la classe principale "SportingEvent".

---

## Q38
**Question:** Pour quel objectif expérimental le capteur IMU_Withers_01 est-il utilisé ?

**Ground Truth:** Le capteur IMU_Withers_01 est utilisé pour la classification de la démarche (GaitClassification).

**Answer:** Le capteur IMU_Withers_01 est utilisé pour l'objectif expérimental suivant :

1.  GaitClassif_01
    (étude du comportement équin, classification des gaits)

---

## Q39
**Question:** Pour quel objectif expérimental le capteur IMU_CanonFore_01 est-il utilisé ?

**Ground Truth:** Le capteur IMU_CanonFore_01 est utilisé pour la détection de fatigue (FatigueDetection).

**Answer:** Le capteur IMU_CanonFore_01 est utilisé pour détecter la fatigue.

Voici les détails :

* L'objectif expérimental principal est le **détecteur de fatigue** (FatigueDetection).

---

## Q40
**Question:** Quel est l'âge de Dakota ?

**Ground Truth:** L'information sur l'âge de Dakota n'est pas disponible dans le système.

**Answer:** Je n'ai pas trouvé d'information concernant l'âge de Dakota dans le graphe de connaissances.

Si tu veux obtenir plus d'informations sur Dakota, je pourrais t'aider à explorer les autres propriétés du cheval.