# The-Clash-of-Clans (2020101088)

- I have used the OOPS concept: Inheritance, Polymorphism, Encapsulation, Abstraction.

## Game Specifications in 3.1
 
### Village

- Spawning points: Created 3 spawning points controlled by the keys, 'r', 't', 'y', denoted by 'S'
- Town Hall: Central building with size = 4x3, denoted by 'Î'. This is the only defensive building among all buildings
- Huts: Created 5 huts with size = 4x3, denoted by 'Â'
- Walls: Created walls around the village with size = 1x1, denoted by 'W'
- Cannon: Created 2 cannons, denoted by 'C'
- Hit points are deonted by 3 colors - Green, Yellow, Red

### King
- Denoted by 'K'
- The King is controlled with W/A/S/D corresponding to Up/Left/Down?Right.
- King's initial damage value = 50
- King's max health value = 500

### Barbarians
- Denoted by 'B'
- Barbarians's initial damage value = 20
- Barbarians's max health value = 250
- Manhattan's distance is used to find the nearest building for attacking
- Assumption: Maximum no. of barbarians = 7

### Spells
- Rage Spell: The Rage spell affects every troop alive in the game and the King by doubling the damage and movement speed.
- Heal Spell: The Heal spell affects every troop alive in the game and the King by increasing their health to 150% of the current health (capped at the maximum health)

### Game Endings
- Victory: All buildings (excluding walls) have been destroyed
- Defeat: All troops and the King have died without destroying all buildings.

### Replay
- Done using a dummy file "sample.txt".
- If the file is passed as arguments then replay will be executed.

## Game Specifications in 3.2

### Troops
- Added 2 extra troops - Archers and Balloons

### Archer Queen
- Also added similiar to king.
- To select option for Queen enter 'p' and for king enter 'o'. Then press 'Enter' to continue.
- Queen's AOE is 5X5 and an amendment is made for easy attack of the queen due to the large size of the building.
- Denoted by 'Q'.

### Buildings
- Added a new building, Wizard Tower which can attack aerially. The AoE damage is a 3x3 tile area around the troop it is attacking.

### Levels
- Added 3 levels in total - 
○ Level 1: 2 cannons and 2 wizard towers
○ Level 2: 3 cannons and 3 wizard towers
○ Level 3: 4 cannons and 4 wizard towers
- The user is directed to the next level once he/she wins the previous level. 
- The maximum achievable level is 3rd level.



