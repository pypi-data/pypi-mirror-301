from datetime import datetime

from pydantic import BaseModel, Field


class ProjectOwner(BaseModel):
    url: str
    username: str
    img: str
    online_at: datetime
    full_name: str
    tags: list[str]


class Project(BaseModel):
    id: int
    url: str
    title: str
    description: str
    public_at: datetime
    tags: list[str]
    price: float | None
    owner: ProjectOwner


class Projects(BaseModel):
    count: int = Field(default=0)
    items: list[Project] = Field(default_factory=list)
