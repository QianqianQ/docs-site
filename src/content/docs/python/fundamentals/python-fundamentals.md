---
title: Python Fundamentals & Interview Questions
description: Core Python concepts, features, and common interview questions with answers.
sidebar:
  order: 1  # This will make it appear first in the Python section
tableOfContents:
  minHeadingLevel: 2
  maxHeadingLevel: 3
---

### What is Python
  - high-level programming language known for its readability and simplicity
  - supports various programming paradigms such as procedural, object-oriented, and functional programming.

### Key features of Python
  - dynamic typing, interpreted nature, and a vast standard library.

### Benifits of using Python
  - Easy to learn and read
  - Large standard library and Extensive third-party packages.
  - Cross-platform
  - freely available for use and distribution

### Built-in data types
  A: (8) int, float, str, list, tuple, set, dict, bool

  - A list is a mutable, ordered collection of items

### Difference between a tuple and a list
  A: Lists are mutable (can be changed), while tuples are immutable (cannot be changed after creation).

### Difference between `staticmethod` and `classmethod`
  A:
    - A `staticmethod` is a method that does not receive an implicit first argument. It functions like a regular method but exists within the class's namespace without access to the instance (`self`) or the class (`cls`).
    - A `classmethod` takes the class (`cls`) as the first argument. It can access and modify class state, making it useful for factory methods or modifying class variables across all instances.

### How are function arguments passed (Pass by reference or pass by value)
  - Python uses a model called pass-by-object-reference. This means that mutable objects like lists or dictionaries can be modified within a function, while immutable objects like integers, strings, or tuples cannot. Essentially, Python passes references to objects, but whether the object itself can be modified depends on its mutability.

### Namespace
  - A namespace is a container that holds names of identifiers and ensures that they are unique within a certain scope. In Python, namespaces exist at different levels:
  - Local namespace: Contains names defined within a function.
  - Global namespace: Contains names defined at the module level.
  - Built-in namespace: Contains Python's built-in functions and exceptions.

### List comprehension
  - provides a concise way to create lists
  - [expression for item in iterable if condition]

### Lambda function
a type of anonymous function created using the lambda keyword. It can accept multiple arguments but is limited to a single expression.

### Purpose of the `__init__` method in classes
  - the constructor method for initializing objects in a class. It sets the initial state of an object by assigning values to object properties.

### Difference between `append()` and `extend()` in a list
  - The `append()` method adds one element to the end of a list, while the `extend()` method adds all elements from an iterable (such as another list) to the end of the list.

### Handle exceptions
  - Exceptions in Python are handled using try, except, else, and finally blocks

### Difference between GET and POST methods in HTTP
    - GET: Used to request data from a server. The data is appended to the URL and is visible, making it less secure for sensitive data.
    - POST: Used to send data to the server to create or update resources. The data is sent in the request body, making it more secure than GET for transmitting sensitive information.

### How to manage states in a web application
  - Client-Side: Using cookies, local storage, and session storage to store the state data in the browser.
  - Server-Side: Using server-side sessions (Django sessions) or databases to track the state across multiple client requests.

### How does frontend interact with Django
  - Front-end technologies include HTML, CSS, JavaScript, and modern frameworks like React or Angular.They can interact with Django via APIs, typically using Django REST Framework to send and receive JSON data
  - or by rendering Django templates in the case of server-side rendering.

### Virtual environment
A virtual environment is a tool to keep dependencies required by different projects in separate places, by creating isolated Python environments. It ensures that packages required for one project don’t interfere with other projects. This is especially important for full-stack development where different projects might require different versions of libraries or frameworks.

### Check if a class is a child of another class
- issubclass(Child, Parent)

### Why is ‘finalize’ used
  - the ‘finalize’ method is used in the context of resource management and garbage collection. It's part of the ‘weakref’ module, allowing objects to perform cleanup actions before they are destroyed by the garbage collector. It’s generally used to release unmanaged resources.

### Naming conventions
Python does not use access specifiers like private, protected, and public. Instead, it uses naming conventions to indicate the intended visibility
  - Public Members: No underscore prefix
  - Protected Members: Single underscore prefix, for internal use only, though still accessible.
  - Private Members: Double underscore prefix. Directly call will raise an AttributeError. accessed only within the class itself. can be accesss through Name Mangling.

### Encapsulation
Encapsulation is the concept of wrapping data (variables) and methods into a single unit (class) and restricting access to some of the object's components.
