from app import create_app
import os

app = create_app(os.environ['DATABASE_URL'])
