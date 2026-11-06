"""yontu: Turkish writing linter (TDK spelling, AI tells, genre style, concision).

Stdlib only. No network at runtime.
"""
from . import engine as _engine
from . import fidelity as _fidelity
from . import metrics as _metrics
from . import profiller as _profiller

__version__ = "0.2.0"  # x-release-please-version
__all__ = ["lint", "fix", "compare", "stats", "profiles", "__version__"]


def lint(text, register=None, tur=None, config=None):
    """Lint text. Returns {"register", "tur", "detected_by", "words", "sentences", "findings"}."""
    return _engine.lint(text, register=register, tur=tur, config=config)


def fix(text, register=None, tur=None, config=None):
    """Apply safe tdk autofixes. Returns the fixed text."""
    return _engine.fix(text, register=register, tur=tur, config=config)


def compare(old, new):
    """Fidelity gate. Returns {"findings", "errors", "warnings"}."""
    return _fidelity.compare(old, new)


def stats(text, register=None, tur=None):
    """Sentence length, readability and density figures."""
    return _metrics.stats(text, register=register, tur=tur)


def profiles():
    """All tür profiles keyed by id."""
    return _profiller.profiles()
