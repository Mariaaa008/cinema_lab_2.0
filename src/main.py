from .cli import CinemaCLI


def main() -> None:
    """Точка входа в приложение."""
    app = CinemaCLI()
    app.run()


if __name__ == "__main__":
    main()