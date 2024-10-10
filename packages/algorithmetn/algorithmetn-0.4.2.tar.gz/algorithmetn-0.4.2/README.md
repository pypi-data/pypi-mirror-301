# Algorithmetn

`Algorithmetn` is a Python package designed for basic list operations and algorithms. It provides a collection of static methods that simplify common tasks such as displaying messages, managing lists, and performing mathematical operations.

## Features

- **Display Messages**: Easily print messages to the console.
- **User Input**: Get input from users in various formats (string, integer, float).
- **List Management**: Create, modify, and query lists with methods for adding, removing, and searching items.
- **Mathematical Operations**: Calculate maximum, minimum, average, and check for perfect cubes.
- **Conditional Execution**: Execute actions based on conditions.

## Methods

### Static Methods

- `afficher(message)`: Display a message.
- `entrer(prompt)`: Get user input.
- `liste()`: Return an empty list.
- `ajouter(l, item)`: Add an item to the list.
- `retirer(l, item)`: Remove an item from the list if it exists.
- `existe(l, item)`: Check if an item exists in the list.
- `longueur(l)`: Return the length of the list.
- `position(l, item)`: Return the index of an item or -1 if not found.
- `vider(l)`: Clear the list.
- `clone(l)`: Return a copy of the list.
- `entier(prompt)`: Get an integer input from the user.
- `reel(prompt)`: Get a float input from the user.
- `pour(n, action)`: Execute action for each number from 0 to n-1.
- `si(condition, action_vrai, action_faux=None)`: Conditional execution based on a boolean condition.
- `maximiser(l)`: Return the maximum value in the list.
- `minimiser(l)`: Return the minimum value in the list.
- `moyenne(l)`: Return the average of the numbers in the list.
- `trier(l)`: Sort the list in ascending order.
- `rechercher(l, item)`: Search for an item and return its index or -1 if not found.
- `inverser(l)`: Reverse the list.
- `est_vide(l)`: Check if the list is empty.
- `est_palindrome(chaine)`: Check if the input is a palindrome (string or list).
- `est_cubique(n)`: Check if a number is a perfect cube.

## Usage Example

```python
from Algorithmetn import Algorithmetn

# Create a new list
ma_liste = Algorithmetn.liste()

# Add items to the list
Algorithmetn.ajouter(ma_liste, 'apple')
Algorithmetn.ajouter(ma_liste, 'banana')

# Display the list
Algorithmetn.afficher(ma_liste)

# Check if an item exists
if Algorithmetn.existe(ma_liste, 'apple'):
    Algorithmetn.afficher('Apple is in the list!')

# Get the length of the list
length = Algorithmetn.longueur(ma_liste)
Algorithmetn.afficher(f'List length: {length}')

# Check for a palindrome
is_palindrome = Algorithmetn.est_palindrome('radar')
Algorithmetn.afficher(f'Is "radar" a palindrome? {is_palindrome}')