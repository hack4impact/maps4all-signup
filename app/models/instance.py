from sqlalchemy import desc
from ..docker import docker
from .. import db


def filter(source):
    return ''.join(c for c in source if c.isalnum() or c == ' ')


# One to Many
# One User can have Many Instances
class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(64))
    port = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=False)
    secret = db.Column(db.String(64), unique=False)  # SECRET_KEY

    name = db.Column(db.String(64), unique=True)  # name of the instance
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        super(Instance, self).__init__(**kwargs)

        count = Instance.query.count()
        if count > 0:
            highest_port = Instance.query.order_by(
                desc(Instance.port)).limit(1).first().port
        else:
            highest_port = 3000

        self.port = highest_port + 1

        if self.secret is None:
            self.secret = 'super secret key lol lol omg so secret'

    def create_container(self):
        self.is_active = True
        docker.create(self)

    def stop_container(self):
        self.is_active = False
        docker.stop(self)

    def sanitized_name(self):
        return filter(self.name)

    def __repr__(self):
        return '<Instance \'%s\'>' % self.name
