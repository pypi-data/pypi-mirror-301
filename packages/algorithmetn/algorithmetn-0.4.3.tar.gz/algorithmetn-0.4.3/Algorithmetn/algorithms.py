class Algorithmetn:
    @staticmethod
    def afficher(message):
        """Display a message."""
        print(message)

    @staticmethod
    def entrer(prompt):
        """Get user input."""
        return input(prompt)

    @staticmethod
    def liste():
        """Return an empty list."""
        return []

    @staticmethod
    def ajouter(l, item):
        """Add an item to the list."""
        l.append(item)  # Add as a numeric type

    @staticmethod
    def retirer(l, item):
        """Remove an item from the list if it exists."""
        if item in l:
            l.remove(item)

    @staticmethod
    def existe(l, item):
        """Check if an item exists in the list."""
        return item in l

    @staticmethod
    def longueur(l):
        """Return the length of the list."""
        return len(l)

    @staticmethod
    def position(l, item):
        """Return the position (index) of an item in the list or -1 if not found."""
        return l.index(item) if item in l else -1

    @staticmethod
    def vider(l):
        """Clear the list."""
        l.clear()

    @staticmethod
    def clone(l):
        """Return a copy of the list."""
        return l.copy()

    @staticmethod
    def entier(prompt):
        """Get an integer input from the user."""
        return int(Algorithmetn.entrer(prompt))

    @staticmethod
    def reel(prompt):
        """Get a float input from the user."""
        return float(Algorithmetn.entrer(prompt))

    @staticmethod
    def pour(n, action):
        """Execute action for each number from 0 to n-1."""
        for i in range(n):
            action(i)

    @staticmethod
    def si(condition, action_vrai, action_faux=None):
        """Execute action_vrai if condition is True; otherwise, execute action_faux."""
        if condition:
            action_vrai()
        elif action_faux:
            action_faux()

    @staticmethod
    def maximiser(l):
        """Return the maximum value in the list."""
        return max(l)

    @staticmethod
    def minimiser(l):
        """Return the minimum value in the list."""
        return min(l)

    @staticmethod
    def moyenne(l):
        """Return the average of the numbers in the list."""
        return sum(l) / len(l) if l else 0

    @staticmethod
    def trier(l):
        """Sort the list in ascending order."""
        l.sort()

    @staticmethod
    def rechercher(l, item):
        """Search for an item in the list and return its index or -1 if not found."""
        index = l.index(item) if item in l else -1
        if index != -1:
            Algorithmetn.afficher(f"'{item}' found at position {index}.")
        else:
            Algorithmetn.afficher(f"'{item}' not found in the list.")
        return index

    @staticmethod
    def inverser(l):
        """Reverse the list."""
        l.reverse()

    @staticmethod
    def est_vide(l):
        """Check if the list is empty."""
        return len(l) == 0

    @staticmethod
    def est_palindrome(chaine):
        """Check if the input (string or list) is a palindrome."""
        if isinstance(chaine, list):
            return chaine == chaine[::-1]
        elif isinstance(chaine, str):
            return chaine == chaine[::-1]
        else:
            raise TypeError("Input must be a string or a list.")

    @staticmethod
    def est_cubique(n):
        """Check if a number is a perfect cube."""
        if n < 0:
            n = -n  # Handle negative numbers
        cube_root = round(n ** (1/3))  # Calculate the integer cube root
        return cube_root ** 3 == n  # Check if the cube of the root equals the original number