def is_string_length(value, min_length, max_length):
    """Valida la longitud de una cadena."""
    return min_length <= len(value) <= max_length

# Ejemplo
print(is_string_length("Hello", 3, 10))  # True
print(is_string_length("Hi", 3, 10))      # False
