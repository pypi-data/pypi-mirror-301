from masterpiece.base import Plugin, Composite


class Foo(Plugin):
    """An object with a description."""

    def __init__(self, name: str = "noname", description: str = "foo") -> None:
        """Create a foo object."""
        super().__init__(name)
        self.description = description

    # @override
    def install(self, app: Composite) -> None:
        obj = Foo("Hello World - A Plugin")
        app.add(obj)

    # @override
    def to_dict(self):
        """Convert instance attributes to a dictionary."""
        return {
            "_class": self.get_class_id(),  # the real class
            "_version:": 0,
            "_foo": {
                "description": self.description,
            },
        }

    # @override
    def from_dict(self, data):
        """Update instance attributes from a dictionary."""
        for key, value in data["_foo"].items():
            setattr(self, key, value)
