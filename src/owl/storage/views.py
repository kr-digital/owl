from owl import app
from owl.storage.core import Core


@app.route('/')
def index():
    return 'Owl storage'