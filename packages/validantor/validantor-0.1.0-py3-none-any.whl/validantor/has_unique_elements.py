def has_unique_elements(collection):
    """Comprueba si todos los elementos en una colección son únicos."""
    return len(collection) == len(set(collection))

# Ejemplo
print(has_unique_elements([1, 2, 3, 4]))
print(has_unique_elements([1, 2, 2, 4]))