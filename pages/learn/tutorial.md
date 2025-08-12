# Tutorial

Welcome! If you're looking to build a modern web app that combines beautiful HTML pages with a powerful REST API, you're in the right place. Air is a friendly layer over FastAPI, making it easy to create both interactive sites and robust APIs—all in one seamless app. Now that you've seen a minimal app, let's build something a bit more challenging. We'll implement a chat system. 

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
uv init airchat
```

**uv** should respond with something that looks like:

```plaintext
Initialized project `airchat` at `/Users/drg/projects/air-repos/airchat/tutorials/airchat`
```

Go into the new directory:

```sh
cd airchat
```

Take a look at the files. You'll see a folder structure that looks like this:

```plaintext
├── README.md
├── main.py
└── pyproject.toml
```

## Step 2: Create and activate the virtualenv

To avoid `airchat` from installing things globally, we're going to have limit its dependencies to just airchat. To do that, have **uv** create a virtualenv

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

Depending on your system, you may see your terminal promopt is now prefixed with `(airchat)`.

## Step 3: Install air[standard]

Air is designed to be both easy to use for development and easy to deploy. For now we're going to have you install the development version by typing this into the command-line:

```sh
uv add "air[standard]"
```

## Unfinished

- [ ] Create index view
- [ ] Authentication
- [ ] Form
- [ ] Persistence
- [ ] Reactivity


## Want to learn more?

Want to see a handy batch of recipes for doing things in Air? [Check out the Air Cookbook!](/learn/cookbook)


