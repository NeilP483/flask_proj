from app import app
from app.models import User, Log

@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'Log': Log}
