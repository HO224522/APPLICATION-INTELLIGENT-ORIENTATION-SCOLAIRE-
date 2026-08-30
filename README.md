PROJET D’APPLICATION INTELLIGENTE D’ORIENTATION SCOLAIRE ET PROFESSIONNELLE
Document de conception fonctionnelle, stratégique et technique
Contexte : Burkina Faso | Version concept / cadrage initial

1. Résumé exécutif
Le projet consiste à créer une plateforme numérique d’orientation scolaire, universitaire et professionnelle intégrant un moteur d’analyse intelligent. Son objectif est d’aider les élèves, étudiants, parents, établissements et structures d’orientation à prendre des décisions mieux informées à partir des résultats scolaires, préférences, aptitudes déclarées, contraintes, objectifs et informations officielles sur les filières et formations.
L’idée part d’un constat : de nombreux élèves ne savent pas quelle série choisir après le collège, quelle filière suivre après le baccalauréat, ni quelles formations ou métiers correspondent réellement à leur profil. La solution proposée transforme l’orientation en un parcours continu : connaître son profil, explorer les possibilités, comparer les options, comprendre les conditions d’accès, construire un plan et suivre son évolution.
Le produit peut également être conçu comme un module d’intelligence d’orientation pouvant être intégré à une application scolaire existante. Il pourrait ainsi compléter une plateforme déjà consacrée au suivi des élèves au lieu de la remplacer.
2. Vision du projet
Construire un « GPS scolaire et professionnel » adapté au contexte burkinabè et, à terme, extensible à d’autres pays africains. L’application doit accompagner un jeune de l’orientation au collège jusqu’aux études supérieures et à l’insertion professionnelle.
Vision à long terme : devenir une infrastructure d’aide à la décision en matière d’orientation, capable d’être utilisée directement par les élèves et parents, par les établissements scolaires et par les institutions chargées de l’orientation, de l’affectation, de l’information scolaire et des bourses.
3. Problème à résoudre
    • Des élèves sont orientés vers des séries ou filières sans comprendre suffisamment les raisons et les conséquences de ce choix.
    • Après le baccalauréat, beaucoup hésitent entre plusieurs filières et connaissent mal les débouchés, conditions d’admission, coûts et parcours.
    • Les conseils disponibles peuvent être généraux, tardifs ou dépendre fortement de la disponibilité d’un conseiller humain.
    • Les parents disposent parfois de peu d’informations structurées pour accompagner leurs enfants.
    • Les établissements et institutions peuvent avoir besoin d’outils pour mieux informer, analyser et accompagner les profils.
    • Les informations sur les formations, métiers, établissements, conditions d’accès et bourses sont dispersées.
4. Proposition de valeur
La plateforme ne doit pas se limiter à un chatbot. Elle doit combiner données scolaires, questionnaire de profil, moteur de recommandation, base documentaire vérifiée et interface conversationnelle.
    • Personnalisation : les recommandations tiennent compte du profil individuel.
    • Explicabilité : l’utilisateur voit pourquoi une filière est recommandée.
    • Comparaison : plusieurs filières peuvent être comparées selon des critères clairs.
    • Projection : l’élève voit les études, compétences et débouchés associés à une orientation.
    • Suivi : le profil peut évoluer avec les résultats scolaires et les préférences.
    • Contexte local : les recommandations intègrent les réalités et formations disponibles au Burkina Faso.
    • Accessibilité : l’information est disponible à tout moment, tout en conservant la possibilité d’un accompagnement humain.
5. Publics cibles
5.1 Élèves
    • Élèves du collège.
    • Élèves du secondaire.
    • Candidats au baccalauréat.
    • Nouveaux bacheliers.
    • Étudiants souhaitant changer ou préciser leur orientation.
5.2 Parents
    • Suivi du profil et des progrès.
    • Compréhension des options proposées.
    • Accès aux informations sur les formations.
    • Accompagnement des décisions de l’enfant.
5.3 Établissements scolaires
    • Tableau de bord d’orientation.
    • Suivi des profils.
    • Statistiques anonymisées et agrégées.
    • Accompagnement des élèves.
5.4 Institutions
    • Structures publiques ou privées intervenant dans l’orientation, l’affectation, les bourses et l’information scolaire.
    • Possibilité d’intégrer le moteur d’orientation à des plateformes institutionnelles.
6. Parcours utilisateur principal
    1. Création du compte et définition du rôle : élève, parent, établissement ou conseiller.
    2. Collecte des informations scolaires : niveau, résultats, matières, progression et autres données autorisées.
    3. Questionnaire de profil : goûts, préférences, aptitudes perçues, méthodes d’apprentissage, centres d’intérêt, contraintes et objectifs.
    4. Analyse du profil par le moteur de recommandation.
    5. Présentation des domaines et filières compatibles.
    6. Explication des raisons de chaque recommandation.
    7. Comparaison de plusieurs options.
    8. Consultation des établissements, conditions d’accès, durée, coûts indicatifs, débouchés et possibilités de bourses lorsque les informations sont disponibles et vérifiées.
    9. Construction d’un plan d’action personnalisé.
    10. Suivi et réévaluation périodique du profil.
7. Fonctionnalités détaillées
7.1 Profil scolaire
    • Niveau et classe.
    • Historique des résultats scolaires.
    • Notes par matière.
    • Évolution des notes dans le temps.
    • Matières fortes et matières à améliorer.
    • Informations sur les examens et diplômes.
    • Objectifs scolaires.
7.2 Questionnaire d’orientation
    • Matières préférées et moins appréciées.
    • Intérêt pour les sciences, lettres, économie, technologie, santé, droit, arts, etc.
    • Préférence pour l’abstrait ou le concret.
    • Préférence pour le travail pratique ou théorique.
    • Goût pour la résolution de problèmes.
    • Intérêt pour les personnes, les machines, les données ou les idées.
    • Auto-évaluation de la concentration, de la régularité et de la capacité à travailler sous pression.
    • Préférence pour les études courtes ou longues.
    • Objectifs professionnels.
    • Mobilité géographique souhaitée.
    • Contraintes financières ou familiales déclarées.
    • Projet de travailler au Burkina Faso ou à l’étranger.
7.3 Moteur de recommandation
Le moteur combine les données scolaires et déclaratives avec une base de connaissances sur les filières. Il produit des recommandations graduées, par exemple « forte compatibilité », « compatibilité intéressante » ou « à explorer », plutôt qu’une décision définitive.
7.4 Explication des recommandations
Pour chaque suggestion, l’application doit présenter les facteurs positifs, les points de vigilance et les informations à vérifier. Exemple : « Cette filière apparaît en bonne position en raison de tes résultats en mathématiques, de ton intérêt pour la résolution de problèmes et de ton attrait pour la technologie. »
7.5 Comparateur de filières
    • Compatibilité avec le profil.
    • Durée des études.
    • Matières importantes.
    • Conditions d’admission.
    • Types d’établissements.
    • Débouchés.
    • Compétences requises.
    • Coût indicatif lorsque disponible.
    • Possibilités de bourses lorsque disponibles.
7.6 Orientation après le collège
Le système peut aider l’élève à explorer les séries, options et parcours compatibles avec ses résultats et ses intérêts, sous réserve des règles officielles d’orientation en vigueur.
7.7 Orientation après le BAC
Le système peut analyser plusieurs choix simultanément et proposer un classement argumenté des domaines d’études, avec les conditions d’accès et les parcours correspondants.
7.8 Parcours vers les métiers
L’application relie filières, formations, compétences et métiers afin de permettre à l’élève de comprendre les conséquences possibles d’un choix d’études.
7.9 Plan personnalisé
    • Objectif choisi.
    • Compétences à renforcer.
    • Matières à travailler.
    • Étapes administratives.
    • Formations à rechercher.
    • Échéances importantes.
    • Ressources d’apprentissage.
7.10 Assistant conversationnel
L’utilisateur peut poser des questions en langage naturel. L’assistant doit utiliser la base de connaissances validée de la plateforme et signaler lorsqu’une information doit être vérifiée auprès d’une source officielle.
7.11 Espace parent
    • Visualisation du parcours.
    • Rapports d’orientation.
    • Alertes et échéances.
    • Ressources d’accompagnement.
    • Contrôle des informations partagées.
7.12 Espace établissement / conseiller
    • Gestion des profils autorisés.
    • Suivi des élèves.
    • Statistiques agrégées.
    • Outils de comparaison.
    • Possibilité de validation ou correction humaine.
    • Historique des recommandations.
8. Exemple d’utilisation
Un élève obtient un baccalauréat et hésite entre médecine, informatique, économie et droit. Il renseigne ses résultats, ses préférences, sa manière d’apprendre, son intérêt pour les problèmes, les sciences, la lecture et le travail pratique, ainsi que ses objectifs.
Le système pourrait produire un résultat du type : Informatique — forte compatibilité ; Médecine — bonne compatibilité ; Économie — compatibilité intéressante ; Droit — à explorer. Chaque résultat serait accompagné d’une justification et de points de vigilance. Ces résultats seraient présentés comme des aides à la décision et non comme une vérité absolue.
9. Architecture fonctionnelle
    • Application mobile et/ou web.
    • API backend.
    • Base de données utilisateurs et données scolaires.
    • Base de connaissances sur filières, établissements, métiers et règles d’accès.
    • Moteur de scoring/recommandation.
    • Assistant conversationnel IA.
    • Module de recherche et de mise à jour des informations.
    • Tableaux de bord élèves, parents, établissements et administrateurs.
    • Système d’authentification et de gestion des rôles.
    • Journalisation et mécanismes d’audit.
10. Architecture IA : stratégie recommandée
Il est déconseillé de commencer par entraîner un modèle d’intelligence artificielle complexe. La première version doit combiner des règles métier explicites, un système de scoring et une base de connaissances vérifiée.
    11. Définir précisément les décisions que le système doit aider à prendre.
    12. Collecter et structurer les données nécessaires.
    13. Construire le questionnaire de profil.
    14. Définir des règles d’orientation avec des professionnels de l’orientation.
    15. Construire un premier moteur de scoring.
    16. Tester les recommandations sur des profils fictifs et réels avec supervision humaine.
    17. Ajouter un assistant conversationnel utilisant la base de connaissances.
    18. Mesurer les erreurs, biais et incohérences.
    19. Améliorer progressivement les modèles.
L’IA générative doit être utilisée pour dialoguer, expliquer et synthétiser, tandis que les décisions sensibles doivent être appuyées par des règles, données vérifiées et contrôles humains.
11. Données nécessaires
    • Données scolaires : notes, classes, historique, progression.
    • Données de profil : intérêts et préférences.
    • Catalogue des filières et formations.
    • Conditions officielles d’accès.
    • Catalogue des établissements.
    • Informations sur les métiers et compétences.
    • Informations sur les bourses et aides disponibles.
    • Calendrier des échéances.
    • Données statistiques agrégées pour améliorer le système, lorsque légalement et éthiquement possible.
Les données personnelles des mineurs doivent être traitées avec des protections renforcées, une collecte minimale, des finalités claires et des mécanismes d’autorisation adaptés.
12. Fiabilité et sécurité
    • Ne jamais présenter une recommandation comme une décision définitive.
    • Afficher la date et la source des informations institutionnelles lorsque possible.
    • Prévoir une validation humaine pour les cas sensibles.
    • Limiter l’accès aux données selon les rôles.
    • Chiffrer les données sensibles en transit et au repos.
    • Conserver des journaux d’accès et d’actions.
    • Prévoir des mécanismes de correction et de contestation.
    • Tester régulièrement les biais du système.
    • Éviter les recommandations fondées sur des caractéristiques sensibles ou discriminatoires.
13. Base de connaissances burkinabè
Une priorité du projet est de construire une base locale fiable. Elle devra répertorier les séries, filières, formations, établissements, conditions d’admission, procédures, métiers, concours, bourses et autres informations utiles, avec une méthode de vérification et de mise à jour.
Les règles officielles doivent rester prioritaires sur toute estimation algorithmique. L’application doit permettre de distinguer clairement les informations officielles, les estimations et les conseils généraux.
14. Intégration à une application scolaire existante
Le projet peut être développé comme un module complémentaire d’une application de gestion scolaire déjà existante. Au lieu de concurrencer l’application de suivi scolaire, le module ajoute une couche d’intelligence orientée vers l’accompagnement et la décision.
    • Réutilisation des données scolaires autorisées.
    • Accès à l’orientation depuis le dossier de l’élève.
    • Transmission sécurisée des résultats au moteur de recommandation.
    • Tableau de bord commun.
    • Possibilité de vendre le module séparément à d’autres plateformes.
15. Opportunité institutionnelle
Le produit pourrait être proposé à des structures intervenant dans l’orientation, l’affectation, les bourses et l’information scolaire au Burkina Faso. La proposition de valeur serait d’ajouter un outil d’aide à la décision et d’information personnalisée, sans remplacer les compétences et responsabilités des conseillers et institutions.
Une version institutionnelle pourrait offrir des tableaux de bord, statistiques agrégées, campagnes d’information, outils de simulation et accès à un moteur d’orientation configurable selon les règles officielles.
16. Modèle économique
    • Abonnement établissement.
    • Licence institutionnelle.
    • Version gratuite avec fonctionnalités limitées.
    • Fonctionnalités premium pour familles, lorsque pertinent.
    • Licence/API du moteur d’orientation.
    • Services d’intégration et de personnalisation.
    • Contrats de maintenance et de support.
    • Prestations de mise à jour de bases de connaissances.
Les informations éducatives essentielles devraient rester accessibles de manière équitable. Le modèle économique ne doit pas pousser l’algorithme à recommander une formation parce qu’elle est plus rémunératrice.
17. MVP — première version
Pour éviter un projet trop lourd dès le départ, le MVP devrait se concentrer sur une seule promesse : aider un élève à comprendre les filières qui correspondent le mieux à son profil.
    20. Création de profil.
    21. Saisie des résultats scolaires.
    22. Questionnaire d’intérêts et préférences.
    23. Moteur de scoring initial.
    24. Top 5 des domaines recommandés.
    25. Explication des recommandations.
    26. Fiches détaillées des filières.
    27. Comparateur de deux ou trois filières.
    28. Assistant conversationnel limité à la base de connaissances.
    29. Interface administrateur pour mettre à jour les informations.
18. Version 2
    • Orientation après collège.
    • Orientation post-BAC.
    • Base d’établissements et formations.
    • Bourses et échéances.
    • Espace parent.
    • Espace conseiller.
    • Plan de progression personnalisé.
    • Notifications.
    • Statistiques agrégées.
19. Version 3 — plateforme complète
    • Suivi du parcours de l’élève sur plusieurs années.
    • Intégration avec des applications scolaires.
    • API pour partenaires.
    • Moteur de recommandation plus avancé.
    • Analyse prédictive avec supervision.
    • Déploiement national ou régional.
    • Support multilingue selon les besoins.
20. Indicateurs de réussite
    • Nombre d’élèves utilisant le système.
    • Taux de complétion du profil.
    • Taux de satisfaction.
    • Nombre de recommandations consultées.
    • Part des utilisateurs qui comprennent les raisons d’une recommandation.
    • Taux de correction ou contestation des recommandations.
    • Qualité et actualité des données.
    • Utilisation par les établissements et institutions.
    • Évolution du nombre de partenaires.
21. Risques et limites
    • Données incomplètes ou obsolètes.
    • Biais dans les questionnaires ou données historiques.
    • Surconfiance des utilisateurs dans l’algorithme.
    • Erreurs de l’IA générative.
    • Mauvaise interprétation d’une recommandation.
    • Risques liés aux données des mineurs.
    • Dépendance à des informations institutionnelles qui peuvent changer.
    • Complexité de l’intégration avec les systèmes existants.
La règle centrale est : l’IA conseille, explique et aide à explorer ; elle ne doit pas décider seule de l’avenir scolaire d’un jeune.
22. Stratégie de lancement
    30. Interroger des élèves, parents, enseignants et conseillers d’orientation.
    31. Identifier les décisions d’orientation les plus problématiques.
    32. Créer un prototype fonctionnel.
    33. Tester avec un petit groupe d’utilisateurs.
    34. Faire valider la logique par des professionnels de l’orientation.
    35. Corriger les biais et erreurs.
    36. Présenter une démonstration à un établissement ou partenaire.
    37. Proposer une phase pilote.
    38. Mesurer les résultats.
    39. Déployer progressivement.
23. Positionnement commercial
Le produit peut être présenté comme une plateforme d’« aide intelligente à l’orientation et au parcours scolaire », et non comme une IA qui « choisit le métier » d’un élève.
Cette formulation protège mieux l’utilisateur, valorise le rôle du conseiller et facilite une collaboration avec des institutions.
24. Différenciation
    • Adaptation au système éducatif burkinabè.
    • Prise en compte des résultats scolaires réels.
    • Questionnaire de profil multidimensionnel.
    • Explications des recommandations.
    • Connexion entre orientation, formation et métier.
    • Mise à jour des informations officielles.
    • Possibilité d’intégration dans des plateformes scolaires existantes.
    • Possibilité de déploiement institutionnel.
25. Exemple de fiche de recommandation
FILIÈRE : Informatique
Compatibilité indicative : forte
    • Facteurs favorables : bons résultats en mathématiques, intérêt pour la technologie, goût pour la résolution de problèmes.
    • Points de vigilance : nécessité de développer la programmation et la logique.
    • Études possibles : à renseigner selon les formations officiellement disponibles.
    • Métiers possibles : développement logiciel, cybersécurité, data, systèmes, réseaux, IA, etc.
    • Prochaine étape : comparer les formations et vérifier les conditions d’accès.
Le score ne constitue pas une vérité scientifique ni une garantie de réussite.
26. Feuille de route technique
    40. Cadrage fonctionnel et interviews.
    41. Conception UX/UI.
    42. Modélisation de la base de données.
    43. Développement du backend et de l’authentification.
    44. Développement du profil et questionnaire.
    45. Création du catalogue de formations.
    46. Développement du moteur de scoring.
    47. Développement du tableau de bord.
    48. Intégration d’un assistant conversationnel.
    49. Tests de sécurité et de qualité.
    50. Pilote utilisateur.
    51. Déploiement et suivi.
27. Équipe nécessaire à terme
    • Chef de produit / responsable du projet.
    • Développeur backend.
    • Développeur frontend/mobile.
    • Spécialiste IA/data.
    • UX/UI designer.
    • Expert en orientation scolaire.
    • Administrateur de données / contenu.
    • Référent sécurité et protection des données.
    • Partenaires institutionnels.
28. Proposition de pitch
« Nous développons une plateforme intelligente d’orientation scolaire et professionnelle adaptée au Burkina Faso. Elle analyse le parcours scolaire, les résultats, les intérêts, les aptitudes déclarées et les objectifs de chaque élève afin de lui présenter les filières et parcours qui semblent les plus compatibles avec son profil. Elle explique ses recommandations, compare les formations, présente les conditions d’accès et accompagne l’élève dans la construction de son parcours. La solution peut fonctionner directement pour les élèves et parents ou être intégrée aux plateformes scolaires et institutionnelles existantes. »
29. Conclusion
Le projet répond à un problème concret : l’orientation est une décision importante, mais les informations sont souvent dispersées et les élèves ne savent pas toujours comment relier leurs résultats, leurs intérêts, les formations disponibles et les métiers.
La force du projet ne réside donc pas uniquement dans l’utilisation de l’intelligence artificielle. Elle réside dans la combinaison de données scolaires, psychologie et préférences déclarées, informations officielles, moteur de recommandation explicable, accompagnement humain et suivi du parcours.
La stratégie recommandée est de commencer petit avec un MVP, de valider la qualité des recommandations avec des professionnels, puis d’élargir progressivement vers les établissements et institutions. À terme, le projet pourrait devenir un véritable moteur d’orientation utilisable par plusieurs plateformes et acteurs de l’éducation.
30. Prochaines étapes immédiates
    52. Définir précisément le premier public cible : par exemple élèves de 3e et nouveaux bacheliers.
    53. Établir la liste des données nécessaires.
    54. Construire le questionnaire d’orientation.
    55. Définir les critères de compatibilité pour les premières filières.
    56. Constituer une première base de formations et de sources officielles.
    57. Créer les maquettes des écrans.
    58. Développer le MVP.
    59. Tester avec un groupe limité d’élèves.
    60. Documenter les résultats et préparer une démonstration.
    61. Présenter la solution à un partenaire potentiel.
