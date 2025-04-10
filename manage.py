from flask.cli import FlaskGroup
from app import create_app, db
from models import User, Pilgrimage, Booking

cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    cli()