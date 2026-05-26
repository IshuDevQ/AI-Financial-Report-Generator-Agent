import os


def ensure_directories_exist() -> None:
    """
    Create required project folders if they do not exist.
    """

    folders = [
        "data",
        "charts",
        "reports",
        "reports/markdown",
        "reports/pdf"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)