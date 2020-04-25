# SM64Wrapper
Un petit module Python pour l'édition de la RAM de Super Mario 64

## Prérequis
**OS**: Windows 10

**Version de Python testé**: 3.6

**Emulator**: Project 64 v1.6

**Rom**: Super Mario 64 (US)

## Bibliothéques requis
```
psutil==5.5.0
pymem==1.0
colorama==0.4.3
 ```

## Utilisation

```python
from SM64Wrapper import RAM, Animation, Cap, CheckInput
```

### Basique

```python
sm64RAM = RAM() 
sm64RAM.openEmu("Project64")
print(sm64RAM.getLives())  # Retourne le nombre de vie à Mario
sm64RAM.setCoins(10)  # Met le nombre de piéce à 10
```

### Casquette
```python
sm64RAM = RAM() 
sm64RAM.openEmu("Project64")

cap = Cap(sm64RAM)
cap.wing()  # Met la casquette ailée sur Mario
cap.reset()  # Remet la casquette de mario par défaut
```

### Animation
```python
sm64RAM = RAM() 
sm64RAM.openEmu("Project64")

anim = Animation(sm64RAM)
animation.punch()  # Joue l'animation du coup de poing
```
### CheckInput
```python
sm64RAM = RAM() 
sm64RAM.openEmu("Project64")

check_input = CheckInput(sm64RAM)
while not check_input.B():
  print("Le bouton B n'est pas préssé")

print("Le bouton B a été préssé")
```
