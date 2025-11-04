Title: Python packages and circular dependencies
Created: 2025-10-01
Tags: python, packages, circular-dependencies, imports, general-technical

Category: General Technical (AI & SW Dev Tools)

Key questions

- What are Python packages exactly?
- What are circular dependencies?
- How may I have introduced them into my project?
- How do I prevent circular dependencies from happening?

What are Python packages?

**Definition:**
A Python package is a directory containing Python modules, identified by the presence of an `__init__.py` file (can be empty). Packages organize related modules into a namespace hierarchy.

**Package structure example:**
```
mypackage/
    __init__.py          # Makes it a package
    module1.py           # A module in the package
    module2.py           # Another module
    subpackage/
        __init__.py      # Subpackage
        submodule.py     # Module in subpackage
```

**Key concepts:**
- **Module**: A single Python file (.py)
- **Package**: A directory with `__init__.py` containing modules/subpackages
- **Distribution package**: What you install with pip (contains one or more packages)
- **Namespace**: Dot-notation access (e.g., `mypackage.module1`)

What are circular dependencies?

**Definition:**
Circular dependencies occur when two or more modules directly or indirectly import each other, creating a cycle in the import chain.

**Examples:**
```python
# Direct circular dependency
# file: a.py
from b import something_from_b

# file: b.py  
from a import something_from_a  # ERROR: circular import
```

```python
# Indirect circular dependency
# file: a.py
from b import func_b

# file: b.py
from c import func_c

# file: c.py
from a import func_a  # ERROR: creates a->b->c->a cycle
```

How circular dependencies might be introduced

**Common scenarios:**
- **Shared utilities**: Two modules both need the same helper functions
- **Cross-references**: Model classes that reference each other
- **Initialization order**: Modules that depend on each other's initialization
- **Refactoring mistakes**: Moving code without updating import structure
- **Global state**: Modules sharing global variables or singletons

**Detection strategies:**
- Import errors at runtime (`ImportError: cannot import name`)
- Static analysis tools (`import-linter`, `pydeps`)
- Dependency visualization tools
- Code review focusing on import statements

Prevention strategies

**Design patterns:**
- **Dependency injection**: Pass dependencies as parameters instead of importing
- **Interface/abstraction layer**: Use abstract base classes or protocols
- **Event-driven architecture**: Use signals/events instead of direct imports
- **Factory patterns**: Centralize object creation to avoid cross-imports

**Code organization:**
- **Layered architecture**: Clear hierarchy (models -> services -> views)
- **Separate concerns**: Keep related functionality in the same module
- **Late imports**: Import inside functions when needed (not at module level)
- **Extract common code**: Move shared utilities to a separate module

**Specific techniques:**
```python
# Instead of module-level imports that cause cycles:
# from other_module import SomeClass  # At top of file

# Use late imports:
def my_function():
    from other_module import SomeClass  # Import when needed
    return SomeClass()

# Or use string-based imports for type hints:
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from other_module import SomeClass

def my_function() -> 'SomeClass':  # String annotation
    from other_module import SomeClass
    return SomeClass()
```

Detection and debugging tools

**Tools to find circular dependencies:**
- `pydeps package_name --show-cycles`
- `import-linter` with circular imports rule
- `vulture` (finds unused imports that might hide cycles)
- Manual dependency graph analysis

**Debugging steps:**
1. Identify the import error message and stack trace
2. Map out the import chain causing the cycle
3. Choose which dependency to break (usually the weaker coupling)
4. Refactor using one of the prevention patterns above

Next actions for your projects

- Audit current import structure in main projects
- Set up `pydeps` or `import-linter` to detect cycles
- Review any recent `ImportError` messages
- Establish import conventions for team (layered architecture)

Done: saved as `data/notes/python_packages_circular_deps.md`