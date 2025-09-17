import air
from pathlib import Path

app = air.Air()


@app.page
def index():
    return air.RedirectResponse('https://feldroy.github.io/air/')

@app.get('/{slug:path}')
def page(slug: str):
    slug = slug.replace('reference', 'api')
    return air.RedirectResponse(f'https://feldroy.github.io/air/{slug}')