# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app. Now that you've seen a minimal app, let's build something a bit more challenging. We'll implement a blog system. 

## Step 0: Install uv if you haven't yet

[uv](https://docs.astral.sh/uv) supports managing Python projects. If you haven't installed it yet, we recommend doing so across your system rather than within a virtual environment. 

Mac and Linux:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows: 

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If you already have **uv** installed, you can update it with the following command:

```sh
uv self update
```

Test the installation by checking the version of **uv**:

```sh
uv --version
```

Install the latest version of Python. Don't worry, this won't override any system Pythons. Rather, it ensures later on **uv** knows exacly where to find the latest Python version

```sh
uv install python
```

## Step 1: Starting the project

In whatever directory or folder where you place your projects, use **uv** to create your project:

```sh
uv init airblog
```

**uv** should respond with something that looks like:

```plaintext
Initialized project `airblog` at `/Users/drg/projects/air-repos/airblog/tutorials/airblog`
```

Go into the new directory:

```sh
cd airblog
```

Take a look at the files. You'll see a folder structure that looks like this:

```plaintext
├── README.md
├── main.py
└── pyproject.toml
```

These files are:

- **README.md** - Every project should have a README providing not just the name of the project, but also how to install and run it
- **main.py** - Where the code for most of this tutorial will go
- **pyproject.toml** - A standardized configuration file for Python projects that defines build system requirements, dependencies, and tool settings in a single place.

## Step 2: Create and activate the virtualenv

To avoid `airblog` from installing things globally, we limit its dependencies to just airblog. To do that, have **uv** create a virtualenv

```sh
uv venv
```

To activate the virtualenv on Mac or Linux:

```sh
source .venv/bin/activate
```

On Windows:

```sh
venv\Scripts\activate.bat
```

Depending on your system, you may see your terminal promopt is now prefixed with `(airblog)`.

## Step 3: Install air[standard]

Air is designed to be both easy to use for development and easy to deploy. For now we're going to have you install the development version by typing this into the command-line:

```sh
uv add "air[standard]"
```

## Step 4: Creating the first view

Open up the `main.py` file and remove all the code in there and replace it with this:

```python
import air

app = air.Air()

@app.get("/")
async def index():
    return air.layouts.mvpcss(
        air.H1("Air Blog"),
        air.P("Breathe in good writing.")
    )
```

## Step 5: Adding database dependencies

A blog needs to store articles, so let's add database support. We'll use SQLModel (which combines SQLAlchemy and Pydantic) with SQLite for simplicity:

```sh
uv add sqlmodel
```

## Step 6: Creating the database model

Create a new file called `models.py` in your project directory:

```python
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, Session
import json

class BlogArticle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(max_length=500)
    body: str
    tags: str = Field(default="")  # Store as JSON string
    date_published: Optional[datetime] = Field(default=None)
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def tags_list(self) -> List[str]:
        """Convert tags JSON string to list"""
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except json.JSONDecodeError:
            return []
    
    @tags_list.setter
    def tags_list(self, value: List[str]):
        """Convert tags list to JSON string"""
        self.tags = json.dumps(value)

# Database setup
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

## Step 7: Initialize the database

Update your `main.py` to initialize the database when the app starts:

```python
import air
from contextlib import asynccontextmanager
from models import create_db_and_tables

@asynccontextmanager
async def lifespan(app):
    # Create database tables on startup
    create_db_and_tables()
    yield
    # Cleanup on shutdown (if needed)

app = air.Air(lifespan=lifespan)

@app.get("/")
async def index():
    return air.layouts.mvpcss(
        air.H1("Air Blog"),
        air.P("Breathe in good writing.")
    )
```





