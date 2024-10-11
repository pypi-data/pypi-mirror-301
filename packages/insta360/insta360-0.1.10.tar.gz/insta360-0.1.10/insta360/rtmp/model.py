import dataclasses


@dataclasses.dataclass(frozen=True)
class CameraInfo:
    loaded: bool = False

    model: str = None  # TODO: Use an enum instead
    firmware_version: str = None

    def copy(self, **replacements):
        replacements.setdefault("loaded", True)
        return dataclasses.replace(self, **replacements)
