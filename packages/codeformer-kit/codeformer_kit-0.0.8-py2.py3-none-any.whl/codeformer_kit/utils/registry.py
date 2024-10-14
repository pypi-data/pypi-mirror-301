class Registry:
    """
    A registry for mapping names to objects (e.g., classes or functions), supporting 
    modular extension of systems through third-party modules.

    Example Usage:

    Creating a registry (e.g., for models):

    .. code-block:: python

        MODEL_REGISTRY = Registry('MODEL')

    Registering an object:

    .. code-block:: python

        @MODEL_REGISTRY.register()
        class MyModel:
            ...

    Or alternatively:

    .. code-block:: python

        MODEL_REGISTRY.register(MyModel)
    """

    def __init__(self, name: str):
        """
        Initialize the registry.

        Args:
            name (str): The name of the registry (used for identification).
        """
        self._name = name
        self._obj_map = {}

    def _do_register(self, name: str, obj: object) -> None:
        """
        Internal method to register an object under a specific name.

        Args:
            name (str): The name to register the object under.
            obj (object): The object to be registered.

        Raises:
            AssertionError: If an object with the same name already exists.
        """
        if name in self._obj_map:
            raise AssertionError(f"An object named '{name}' is already registered in the '{self._name}' registry!")
        self._obj_map[name] = obj

    def register(self, obj=None):
        """
        Register the given object under its `__name__`.
        Can be used as a decorator or as a function call.

        Args:
            obj (optional): The object to register. If None, used as a decorator.

        Returns:
            If used as a decorator, returns a function that registers the decorated object.
            Otherwise, directly registers the object.

        Example:
        .. code-block:: python

            @registry.register()
            class MyClass:
                ...
            
            OR

            registry.register(MyClass)
        """
        if obj is None:
            # Used as a decorator
            def decorator(func_or_class):
                name = func_or_class.__name__
                self._do_register(name, func_or_class)
                return func_or_class
            return decorator
        
        # Used as a direct function call
        name = obj.__name__
        self._do_register(name, obj)

    def get(self, name: str) -> object:
        """
        Retrieve an object from the registry by its name.

        Args:
            name (str): The name of the object to retrieve.

        Returns:
            object: The registered object.

        Raises:
            KeyError: If the object with the given name is not found in the registry.
        """
        if name not in self._obj_map:
            raise KeyError(f"No object named '{name}' found in the '{self._name}' registry!")
        return self._obj_map[name]

    def __contains__(self, name: str) -> bool:
        """Check if a given name exists in the registry."""
        return name in self._obj_map

    def __iter__(self):
        """Allow iteration over registered objects (name, object) pairs."""
        return iter(self._obj_map.items())

    def keys(self):
        """Return all registered object names."""
        return self._obj_map.keys()


ARCH_REGISTRY = Registry('arch')
MODEL_REGISTRY = Registry('model')
