"""Compatibility wrapper for the unified assistant.

The project previously exposed a ``synthia_assistant.py`` entry point.  To
avoid breaking existing workflows this lightweight module simply proxies
to :mod:`ultimate_assistant`.
"""

from ultimate_assistant import main


if __name__ == "__main__":  # pragma: no cover - thin wrapper
    main()

