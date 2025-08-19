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

Run it with:

```sh
fastapi dev
```

Try it out at [http://localhost:8000](http://localhost:8000). You should see a simple page with the title "Air Blog" and a subtitle "Breathe in good writing."

## Step 5: Adding database dependencies

A blog needs to store articles, so let's add database support. We'll use SQLModel (which combines SQLAlchemy and Pydantic) with SQLite for simplicity:

Stop the server if it's running using `ctrl-c`, then add the SQLModel dependency:

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

## Step 8: Creating forms for blog articles

Now let's create forms to add and edit blog articles. First, add the form model to your `models.py` file:

```python
from pydantic import BaseModel
from air import AirForm, AirField
from typing import List

class BlogArticleFormModel(BaseModel):
    # TODO: leverage in AirForm to inherit directly from models.BlogArticle
    title: str = AirField(max_length=200, label="Article Title")
    description: str = AirField(max_length=500, label="Short Description")
    body: str = AirField(type="textarea", label="Article Body")
    tags: str = AirField(default="", label="Tags (comma-separated)", placeholder="python, web, tutorial")
    is_published: bool = AirField(default=False, label="Publish immediately")

class BlogArticleForm(AirForm):
    model = BlogArticleFormModel
```

## Step 9: Adding form views

Update your `main.py` to include form views:

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


# Forms, try to leverage in 
from pydantic import BaseModel
from air import AirForm, AirField
from typing import List

class BlogArticleFormModel(BaseModel):
    title: str = AirField(max_length=200, label="Article Title", autofocus=True)
    description: str = AirField(max_length=500, label="Short Description")
    body: str = AirField(type="textarea", label="Article Body")
    tags: str = AirField(default="", label="Tags (comma-separated)", placeholder="python, web, tutorial")
    is_published: bool = AirField(default=False, label="Publish immediately")

class BlogArticleForm(AirForm):
    model = BlogArticleFormModel        
```

## Step 10: Displaying articles

Let's add views to list and display individual articles:

```python
@app.page
async def articles():
    with next(get_session()) as session:
        # Get only published articles, ordered by date
        statement = select(BlogArticle).where(BlogArticle.is_published == True).order_by(BlogArticle.date_published.desc())
        articles = session.exec(statement).all()
    
    article_list = []
    for article in articles:
        article_list.extend([
            air.Article(
                air.H2(air.A(article.title, href=f"/articles/{article.id}")),
                air.P(article.description),
                air.Small(f"Published: {article.date_published.strftime('%B %d, %Y')}"),
                air.P(f"Tags: {', '.join(article.tags_list)}" if article.tags_list else "")
            )
        ])
    
    return air.layouts.mvpcss(
        air.H1("All Articles"),
        *article_list if article_list else [air.P("No articles published yet.")],
        air.A("← Back to Blog", href="/"),
        air.A("Create New Article", href="/new-article")
    )

@app.get("/articles/{article_id}")
async def view_article(article_id: int):
    with next(get_session()) as session:
        article = session.get(BlogArticle, article_id)
        if not article or not article.is_published:
            return air.layouts.mvpcss(
                air.H1("Article Not Found"),
                air.P("The article you're looking for doesn't exist or isn't published."),
                air.A("← Back to Blog", href="/")
            )
    
    return air.layouts.mvpcss(
        air.H1(article.title),
        air.P(article.description, style="font-style: italic; font-size: 1.2em;"),
        air.Small(f"Published: {article.date_published.strftime('%B %d, %Y')}"),
        air.P(f"Tags: {', '.join(article.tags_list)}" if article.tags_list else ""),
        air.Hr(),
        air.Div(article.body.replace('\n', '<br>'), style="white-space: pre-wrap;"),
        air.Hr(),
        air.A("← Back to Articles", href="/articles")
    )
```

## Appendix: Entire project code

Still not done yet, this is our entire project code. Still need to:

- add editing of form
- fixing top nav issues with MVP CSS layout, the difference between the HeaderNav and Main is too great. This is in Air, not the tutorial.

```python
import air
import json
from contextlib import asynccontextmanager
from datetime import datetime
from models import create_db_and_tables, BlogArticle, get_session, BlogArticleForm
from sqlmodel import Session, select

@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield

app = air.Air(lifespan=lifespan)

@app.page
async def index():
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("View Articles", href="/articles"),
                air.A("New Article", href="/new-article"),
            ),    
            air.H1("Air Blog"),
            air.P("Breathe in good writing."),
        )
    )

@app.get('/new-article')
async def new_article():
    form = BlogArticleForm()
    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                air.A("Home", href="/"),
                air.A("Articles", href="/articles")
            ),            
            air.H1("Create New Article"),
            air.Form(
                form.render(),
                air.Br(),
                air.Button("Create Article", type="submit"),
                action="/articles",
                method="post"
            ),
        )
    )

@app.post("/articles")
async def create_article(request: air.Request):
    form = BlogArticleForm()
    form_data = await request.form()
    
    if form.validate(form_data):
        # Create new article from validated data
        with next(get_session()) as session:
            # Convert tags string to list for storage
            tags_list = [tag.strip() for tag in form.data.tags.split(",") if tag.strip()]
            
            article = BlogArticle(
                title=form.data.title,
                description=form.data.description,
                body=form.data.body,
                tags=json.dumps(tags_list),
                is_published=form.data.is_published,
                date_published=datetime.utcnow() if form.data.is_published else None
            )
            session.add(article)
            session.commit()
            session.refresh(article)
        
        return air.layouts.mvpcss(
            air.H1("Article Created!"),
            air.P(f"Your article '{article.title}' has been created."),
            air.Nav(
                air.A("Home", href="/"),
                air.A("View Article", href=f"/articles/{article.id}"),
                air.A("Create Another", href="/new-article")
            )
        )
    else:
        # Form validation failed, show errors
        return air.layouts.mvpcss(
            air.H1("Create New Article"),
            air.P("Please correct the errors below:", style="color: red;"),
            air.Form(
                form.render(),
                air.Button("Create Article", type="submit"),
                action="/articles",
                method="post"
            ),
            air.A("← Back to Blog", href="/")
        )
    
@app.page
async def articles():
    with next(get_session()) as session:
        # Get only published articles, ordered by date
        statement = select(BlogArticle).where(BlogArticle.is_published == True).order_by(BlogArticle.date_published.desc())
        articles = session.exec(statement).all()

    article_list = []
    for article in articles:
        article_list.extend([
            air.Article(
                air.H2(air.A(article.title, href=f"/articles/{article.id}")),
                air.P(article.description),
                air.Small(f"Published: {article.date_published.strftime('%B %d, %Y')}"),
                air.P(f"Tags: {', '.join(article.tags_list)}" if article.tags_list else "")
            )
        ])

    return air.layouts.mvpcss(
        air.Header(
            air.Nav(
                    air.A("Home", href="/"),
                    air.A("Create New Article", href="/new-article")
            ),        
            air.H1("All Articles"),
            *article_list if article_list else [air.P("No articles published yet.")],
        ),
    )
```