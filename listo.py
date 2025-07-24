"""
Listo - A chainable list replacement that allows method chaining.

Example usage:
    listo = Listo([3, 1, 4, 1, 5, 9, 2, 6])
    result = listo.filter(lambda x: x > 2).map(lambda x: x * 2).sorted()
    # Returns Listo([6, 8, 10, 12, 18])
"""

from typing import Any, Callable, Iterable, Optional, TypeVar, Union, TYPE_CHECKING
from functools import reduce

if TYPE_CHECKING:
    from typing import Self

T = TypeVar('T')
U = TypeVar('U')


class Listo(list):
    """A list subclass that allows method chaining by returning Listo instances."""
    
    def __init__(self, iterable: Iterable[Any] = None):
        """Initialize a Listo from an iterable."""
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)
    
    def map(self, func: Callable[[T], U]) -> 'Listo[U]':
        """Apply a function to each element and return a new Listo."""
        return Listo(func(item) for item in self)
    
    def filter(self, func: Callable[[T], bool]) -> 'Listo[T]':
        """Filter elements based on a predicate function and return a new Listo."""
        return Listo(item for item in self if func(item))
    
    def sorted(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> 'Listo[T]':
        """Return a new sorted Listo."""
        return Listo(sorted(self, key=key, reverse=reverse))
    
    def sort(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> 'Listo[T]':
        """Return a new sorted Listo."""
        return Listo(sorted(self, key=key, reverse=reverse))
    
    def unique(self) -> 'Listo[T]':
        """Return a new Listo with unique elements (preserving order)."""
        seen = set()
        result = []
        for item in self:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return Listo(result)
    
    def reverse(self) -> 'Listo[T]':
        """Return a new Listo with elements in reverse order."""
        return Listo(reversed(self))
    
    def take(self, n: int) -> 'Listo[T]':
        """Take the first n elements and return a new Listo."""
        return Listo(self[:n])
    
    def skip(self, n: int) -> 'Listo[T]':
        """Skip the first n elements and return a new Listo."""
        return Listo(self[n:])
    
    def where(self, **kwargs) -> 'Listo[T]':
        """Filter elements based on attribute values."""
        def matches(item):
            for key, value in kwargs.items():
                if not hasattr(item, key) or getattr(item, key) != value:
                    return False
            return True
        return self.filter(matches)
    
    def pluck(self, attr: str) -> 'Listo[Any]':
        """Extract a specific attribute from each element."""
        return self.map(lambda item: getattr(item, attr))
    
    def flatten(self) -> 'Listo[Any]':
        """Flatten one level of nesting."""
        result = []
        for item in self:
            if isinstance(item, (list, tuple, Listo)):
                result.extend(item)
            else:
                result.append(item)
        return Listo(result)
    
    def chunk(self, size: int) -> 'Listo[Listo[Any]]':
        """Split the list into chunks of specified size."""
        chunks = []
        for i in range(0, len(self), size):
            chunks.append(Listo(self[i:i + size]))
        return Listo(chunks)
    
    def group_by(self, key_func: Callable[[T], Any]) -> dict:
        """Group elements by a key function."""
        groups = {}
        for item in self:
            key = key_func(item)
            if key not in groups:
                groups[key] = Listo()
            groups[key].append(item)
        return groups
    
    def reduce(self, func: Callable[[Any, T], Any], initial: Any = None) -> Any:
        """Reduce the list to a single value using a function."""
        if initial is None:
            return reduce(func, self)
        else:
            return reduce(func, self, initial)
    
    def join(self, separator: str = '') -> str:
        """Join elements into a string."""
        return separator.join(str(item) for item in self)
    
    def sum(self) -> Union[int, float]:
        """Return the sum of all elements."""
        return sum(self)
    
    def min(self) -> T:
        """Return the minimum element."""
        return min(self)
    
    def max(self) -> T:
        """Return the maximum element."""
        return max(self)
    
    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """Test if any element satisfies the predicate (or is truthy if no predicate)."""
        if predicate is None:
            return any(self)
        return any(predicate(item) for item in self)
    
    def all(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """Test if all elements satisfy the predicate (or are truthy if no predicate)."""
        if predicate is None:
            return all(self)
        return all(predicate(item) for item in self)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Find the first element that satisfies the predicate."""
        for item in self:
            if predicate(item):
                return item
        return None
    
    def find_index(self, predicate: Callable[[T], bool]) -> int:
        """Find the index of the first element that satisfies the predicate."""
        for i, item in enumerate(self):
            if predicate(item):
                return i
        return -1
    
    def tap(self, func: Callable[['Listo[T]'], None]) -> 'Listo[T]':
        """Execute a function with the current Listo and return self (for debugging/side effects)."""
        func(self)
        return self
    
    def to_list(self) -> list:
        """Convert back to a regular Python list."""
        return list(self)
    
    def __repr__(self) -> str:
        """String representation of Listo."""
        return f"Listo({list(self)})"


# Convenience function to create a Listo
def listo(iterable: Iterable[Any] = None) -> Listo:
    """Create a new Listo instance."""
    return Listo(iterable)


if __name__ == "__main__":
    # Example usage and demonstrations
    print("=== Listo Examples ===")
    
    # Basic chaining
    numbers = Listo([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
    result = numbers.filter(lambda x: x > 2).map(lambda x: x * 2).sorted().unique()
    print(f"Original: {numbers}")
    print(f"Filtered > 2, mapped *2, sorted, unique: {result}")
    
    # String operations
    words = Listo(["hello", "world", "python", "is", "awesome"])
    caps = words.map(str.upper).filter(lambda w: len(w) > 4).sorted()
    print(f"Words: {words}")
    print(f"Uppercase, length > 4, sorted: {caps}")
    
    # Chunking
    chunked = Listo(range(10)).chunk(3)
    print(f"Range(10) chunked by 3: {chunked}")
    
    # Grouping
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        def __repr__(self):
            return f"Person('{self.name}', {self.age})"
    
    people = Listo([
        Person("Alice", 25),
        Person("Bob", 30),
        Person("Charlie", 25),
        Person("Diana", 30),
    ])
    
    grouped = people.group_by(lambda p: p.age)
    print(f"People grouped by age: {grouped}")
    
    # Using where and pluck
    young_names = people.where(age=25).pluck('name')
    print(f"Names of 25-year-olds: {young_names}")
    
    # Complex chaining
    complex_result = (Listo(range(20))
                     .filter(lambda x: x % 2 == 0)  # Even numbers
                     .map(lambda x: x ** 2)         # Square them
                     .filter(lambda x: x < 100)     # Less than 100
                     .sorted(reverse=True)          # Sort descending
                     .take(5))                      # Take first 5
    print(f"Complex chain result: {complex_result}")
