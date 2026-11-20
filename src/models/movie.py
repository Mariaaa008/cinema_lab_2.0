from dataclasses import dataclass

@dataclass
class Movie:
    id: int | None
    title: str
    description: str
    duration_min: int
    age_limit: int
    is_active: bool = True