"""Example application for demonstration purposes.

Implements the following classes:
- MyHomeArgs - application startup options
- MyHome - application 

"""

from argparse import ArgumentParser
from typing import Optional
from masterpiece.base import Application, MasterPiece, Composite, Args


class MyHomeArgs(Args):
    """Startup arguments"""

    solar: Optional[float] = None


class MyHome(Application):
    """Application demonstrating the structure of masterpiece applications.
    Demonstrates also plugin awareness and startup arguments.
    When run the application prints out its instance hierarchy.
    ::

        home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        ├─ garage
        │   └─ EV charger
        └─ solar plant 5.0 kW

    If --solar [kW] startup argument is passed in with the power, then "solar plant" instance is
    added to the hierarchy.

    """

    # Class attributes.
    solar_plant: float = 0

    def __init__(self, name: str = "myhome") -> None:
        """Initialize home application with the given name.

        Args:
            name (str): The name of the application.
        """
        super().__init__(name)
        self.create_home()
        self.install_plugins()

    def create_home(self):
        """Create stuff to be mastered with this sweet home application"""
        self.create_power_grid()
        self.create_downstairs()
        self.create_garage()
        self.create_solar_plant()

    def create_power_grid(self):
        """Create object representing power grid."""
        grid = MasterPiece("grid")
        self.add(grid)

    def create_solar_plant(self):
        """Create solar plant, if configured. Classes can be configured
        in two ways: either through class configuration files,
        e.g., appname/config/[classname.json], or via startup arguments."""
        if self.solar_plant > 0:
            self.add(MasterPiece(f"solar plant {self.solar_plant} kW"))

    def create_downstairs(self):
        """Create kitchen with a few electric devices."""
        downstairs = Composite("downstairs")
        self.add(downstairs)
        kitchen = Composite("kitchen")
        downstairs.add(kitchen)
        oven = MasterPiece("oven")
        kitchen.add(oven)
        fridge = MasterPiece("fridge")
        kitchen.add(fridge)

    def create_garage(self) -> None:
        """Create garage with EV charger."""
        garage = Composite("garage")
        self.add(garage)
        ev_charger = MasterPiece("EV charger")
        garage.add(ev_charger)

    def run(self) -> None:
        super().run()
        self.print()

    @classmethod
    def register_args(cls, parser: ArgumentParser) -> None:
        """Register startup arguments to be parsed.

        Args:
            parser (argparse.ArgumentParser): parser to add the startup arguments.
        """
        parser.add_argument(
            "-s",
            "--solar",
            type=float,
            help="Add solar power plant with the given power, in kW",
        )

    @classmethod
    def configure_args(cls, args) -> None:
        if args.solar is not None and float(args.solar) > 0.0:
            cls.solar_plant = float(args.solar)


def main() -> None:
    """The standard Python's main function with all the bells and whistles.
    Initializes, instantiates and runs `MyHome` application."""

    # Let's make this application plugin aware
    MyHome.load_plugins()

    # Support class initialization through startup arguments
    MyHome.parse_args()

    # Create an instance of MyHome application
    home = MyHome("home")

    # Support serialization
    home.deserialize()

    # Run
    home.run()


if __name__ == "__main__":
    main()
