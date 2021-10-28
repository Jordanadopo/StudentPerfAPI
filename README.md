## Prédiction de la performance des étudiants ##

## TRICKY-TEST ##

**Ensemble de données:** 
[Ensemble de données sur les performances des élèves](https://archive.ics.uci.edu/ml/datasets/Student+Performance)

**Document d'accompagnement:** 
[Using Data Mining to Predict Secondary School Student Performance](http://www3.dsi.uminho.pt/pcortez/student.pdf)

## Objectif ##

Mon objectif était de construire un modèle permettant de prédire si un élève échouerait ou non au cours de mathématiques faisant l'objet du suivi. J'ai mis l'accent sur les taux d'échec car je pensais que cette mesure était plus utile pour signaler les élèves en difficulté qui pourraient avoir besoin d'une aide supplémentaire.

Pouvoir évaluer de manière préventive les élèves qui ont le plus besoin d'attention est, à mon avis, une étape importante de l'éducation personnalisée.

## Processus ##

La valeur cible est `G3`, qui, selon le document d'accompagnement de l'ensemble de données, peut être classée dans une catégorie de réussite ou d'échec. Si `G3` est supérieur ou égal à 10, alors l'étudiant réussit. Dans le cas contraire, il échoue. De même, les caractéristiques `G1` et `G2` sont classées de la même manière.

Les données peuvent être réduites à 4 caractéristiques fondamentales, par ordre d'importance :
1. Le score `G2`.
2. Le score `G1`.
3. L'école
4. Les absences

Lorsque la connaissance du niveau scolaire n'est pas connue, `School` et `Absences` capturent la plupart de la base prédictive. Lorsque la connaissance des notes devient disponible, les notes `G1` et `G2` suffisent pour atteindre une précision de plus de 90%. J'ai découvert expérimentalement que le modèle est plus performant lorsqu'il utilise seulement 2 caractéristiques à la fois pour chaque expérience.

Le modèle est une machine à vecteur de support linéaire avec un facteur de régularisation de 100. Ce modèle a donné les meilleurs résultats après comparaison à d'autres modèles, tels que les classificateurs de type arbre binaire et régression logistique.

## Résultats ##

Les résultats suivants ont été calculés en moyenne sur 5 essais.

| Caractéristiques prises en compte | G1 & G2 | G1 & Ecole | Ecole & Absences |
|-----------------------------------|:-------:|:----------:|:----------------:|
| Précision du papier | 0,919 | 0,838 | 0,706|
| Taux d'exactitude de mon modèle | 0.9165 | 0.8285 | 0.6847 |
| Taux de fausses réussites : 0.096 | 0.12 | 0.544 | Taux de faux succès|
| Taux de faux échecs : 0.074 | 0.1481 | 0.2185 | 1|

[Pourquoi ces mesures ?](https://github.com/sachanganesh/student-performance-prediction/issues/1#issuecomment-508577754)

## Discussion ##

En l'absence de performances académiques antérieures dans des cours similaires, le problème est difficile à résoudre ; cependant, mon modèle atteint une précision de 68 % en utilisant uniquement l'école fréquentée par l'étudiant et le nombre d'absences qu'il a accumulées pour déterminer s'il a échoué ou non. Ce qui est intéressant, c'est que mon modèle, avec ces paramètres, a un taux de faux succès de plus de 50 %, ce qui signifie qu'il classe plus de la moitié des étudiants qui finissent par échouer comme réussissant. Ce chiffre diminue considérablement à mesure que l'on dispose de plus d'informations et que l'on utilise de meilleurs paramètres, mais il met en évidence un domaine majeur d'amélioration du modèle.

Pour atteindre les performances mentionnées ci-dessus, les auteurs originaux ont dû alterner les modèles pour chaque expérience, en utilisant à la fois des machines à vecteurs de support et des bayes naïves. Les performances de ma machine à vecteurs de support suivent de près les résultats de l'auteur original et présentent une approche plus rationnelle de la résolution du problème, puisque le modèle sous-jacent ne change pas. En outre, les auteurs originaux ont utilisé toutes les variables (à l'exception de la connaissance de la note) pour atteindre la précision de 70,6 % dans la troisième expérience, alors que mon modèle n'utilise que deux paramètres à la fois pour obtenir des résultats similaires.
