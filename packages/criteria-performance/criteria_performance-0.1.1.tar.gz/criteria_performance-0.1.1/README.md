# CriteriaPerformanceReadCSV

**CriteriaPerformanceReadCSV** est un module Python permettant de calculer et de visualiser les performances de modèles à partir de données CSV. Il génère plusieurs courbes de performance, telles que les courbes ROC, PR (Rappel-Précision), DET (Detection Error Tradeoff), ainsi que d'autres indicateurs clés.

## Table des matières

- [Installation](#installation)
- [Pré-requis](#pré-requis)
- [Utilisation de base](#utilisation-de-base)
- [Exemple de CSV](#exemple-de-csv)
- [Fonctionnalités](#fonctionnalités)
- [Exemple d'utilisation avancée](#exemple-dutilisation-avancée)
- [Méthodes disponibles](#méthodes-disponibles)

## Installation

Vous pouvez installer le package en utilisant pip:

```bash
pip install criteria_performance
```

## Pré-requis

Vous aurez besoin d'un fichier CSV contenant les performances de votre modèle. Ce fichier doit avoir au minimum deux colonnes :

- **classe** : Indicateur de la classe (1 pour les valeurs positives, -1 pour les valeurs négatives).
- **score** : Score de confiance ou probabilité attribuée par le modèle pour chaque observation.

## Utilisation de base

### 1. Chargement des données

Utilisez le module en chargeant un fichier CSV. Par exemple :

```python
from criteria_performance import CriteriaPerformanceReadCSV

# Chemin vers le fichier CSV
url_data = "path/to/your/data.csv"

# Initialisation de l'objet
performance = CriteriaPerformanceReadCSV(url_data)
```

### 2. Visualisation des courbes

Une fois les données chargées, vous pouvez afficher diverses courbes pour évaluer la performance de votre modèle :

#### Courbe ROC

```python
performance.dispROC()
```

#### Courbe Rappel-Précision (PR)

```python
performance.dispPR()
```

#### Courbe DET

```python
performance.dispDET()
```

#### Courbe avec intersection FNR/FPR (DET modifiée)

```python
performance.dipoldDET(point=True)
```

#### Affichage de toutes les courbes ensemble

```python
performance.displaygraphe(taille=(18, 10), save=True, name="criteres_performance")
```

Cela génère un fichier PNG contenant toutes les courbes si `save=True`.

### Exemple de CSV

Voici un exemple de structure de fichier CSV compatible avec le module :

csv

| Classe | Score |
|--------|-------|
| 1      | 0.9   |
| 1      | 0.8   |
| -1     | 0.4   |
| -1     | 0.1   |

Assurez-vous que les colonnes **classe** et **score** sont bien nommées de cette manière, ou adaptez votre code pour tenir compte de vos propres noms de colonnes.

## Fonctionnalités

- **Courbe ROC** : Représente le taux de faux positifs (TFP) vs. taux de vrais positifs (TTP).
- **Courbe PR** : Montre la précision et le rappel de votre modèle.
- **Courbe DET** : Compare le taux de faux positifs (FPR) et le taux de faux négatifs (FNR).
- **Intersection DET modifiée** : Affiche le point d'intersection entre FPR et FNR.
- **Sauvegarde des graphiques** : Les graphiques peuvent être enregistrés sous forme d'images.

## Exemple d'utilisation avancée

Vous pouvez personnaliser les titres et les couleurs des courbes pour correspondre à vos besoins :

```python
performance.dipoldDET(title="Mon DET modifié", point=True, c1="green", c2="red", cp="purple")
performance.dispPR(label="Courbe PR personnalisée", c="blue", title="PR Custom")
```

Vous pouvez également ajuster le nombre de seuils pour un contrôle plus fin lors de la génération des courbes :

```python
performance.generate_seuil(val=50)
```

## Méthodes disponibles

Voici une description des méthodes clés :

### `__init__(url_data: str)`

- **Description** : Initialise l'objet et charge les données depuis un fichier CSV.
- **Paramètre** : `url_data` – chemin vers le fichier CSV.
  
### `ppv_pnv()`

- **Description** : Calcule les PPV (Positive Predictive Value) et PNV (Negative Predictive Value).
  
### `generate_seuil(val=20)`

- **Description** : Génère les seuils pour les courbes.
- **Paramètre** : `val` – nombre de seuils à générer (par défaut à 20).
  
### `fp_tp()`

- **Description** : Calcule les faux positifs et vrais positifs à chaque seuil.
  
### `Tfp_Ttp()`

- **Description** : Calcule les taux de faux positifs (TFP) et taux de vrais positifs (TTP).
  
### `calculate_fn()`

- **Description** : Calcule le nombre de faux négatifs (FN) à chaque seuil.

### `coordonne()`

- **Description** : Renvoie les coordonnées pour la courbe Rappel-Précision.
  
### `fnr_fpr()`

- **Description** : Renvoie le taux de faux négatifs (FNR) et taux de faux positifs (FPR).
  
### `dipoldDET(point=False, title="Hold DET", c1="b", c2="orange", cp="red")`

- **Description** : Affiche la courbe DET avec FNR et FPR. Option d'afficher l'intersection.
  
### `dispROC()`

- **Description** : Affiche la courbe ROC.

### `displaygraphe(taille=(18, 10), save=False, name="criteres_performance")`

- **Description** : Affiche toutes les courbes (ROC, PR, DET) et permet de les sauvegarder sous forme d'image.

## Licence

Ce projet est sous licence MIT.
