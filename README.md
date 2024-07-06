## Snake Game avec Agent d'Apprentissage par Renforcement

Ce projet implémente un jeu de Snake utilisant l'apprentissage par renforcement pour contrôler le serpent. Le projet est divisé en plusieurs fichiers Python interconnectés, chacun ayant un rôle distinct dans le fonctionnement global du jeu et de l'agent d'apprentissage.

### Structure du Projet

- `snakegame.py` : Ce fichier contient le code de base pour le jeu de Snake.
- `agent.py` : Ce fichier contient l'implémentation de base de l'agent d'apprentissage par renforcement.
- `advenced_snakegame.py` : Ce fichier est une version améliorée du jeu de Snake intégrant des fonctionnalités supplémentaires.
- `advanced_agent.py` : Ce fichier contient une version avancée de l'agent avec des techniques de double Q-learning.

### Prérequis

Avant de pouvoir exécuter ce projet, vous devez installer les bibliothèques suivantes :

```bash
pip install pygame numpy
```

### Utilisation

Pour exécuter le jeu de Snake avec l'agent d'apprentissage par renforcement, lancez simplement le fichier `advenced_snakegame.py` :

```bash
python advenced_snakegame.py
```

### Détails des Fichiers

#### `snakegame.py`

Ce fichier configure le jeu de Snake en utilisant Pygame. Il initialise la fenêtre de jeu, la position et la direction du serpent, ainsi que les positions des pommes. Il intègre également un agent (`Agent1`) pour contrôler le serpent.

#### `agent.py`

Ce fichier implémente un agent d'apprentissage par renforcement de base utilisant une table de Q-valeurs pour prendre des décisions. L'agent choisit des actions basées sur une politique ε-greedy et met à jour ses Q-valeurs en fonction des récompenses reçues.

#### `advenced_snakegame.py`

Ce fichier est une version améliorée du jeu de Snake. Il ajoute des fonctionnalités comme un écran de démarrage, les limites du jeu, et intègre des mises à jour de l'agent pour améliorer ses performances. Le jeu utilise également un agent pour contrôler le serpent et met à jour les Q-valeurs en temps réel.

#### `advanced_agent.py`

Ce fichier contient une version avancée de l'agent utilisant le double Q-learning pour éviter le biais de surévaluation. L'agent utilise deux tables de Q-valeurs et un buffer de relecture pour stocker et échantillonner les expériences passées. Cela permet un apprentissage plus stable et efficace.

### Contribuer

Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

### Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.



---

Merci d'avoir utilisé ce projet ! Amusez-vous bien avec le jeu de Snake et l'apprentissage par renforcement.
