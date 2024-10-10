# harsh/text.py

def reverse_text(text):
    """Returns the reversed version of the input text."""
    return text[::-1]

def count_words(text):
    """Counts the number of words in the input text."""
    return len(text.split())

def unique_words(text):
    """Returns the unique words in the text."""
    return set(text.split())
