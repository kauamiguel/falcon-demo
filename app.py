import falcon
import json
from sqlalchemy import select
import database
from database import UserModel
from database_middleware import DatabaseSessionMiddleware


class UserCollectionResource():
    def on_get(self, req, resp):
        db = req.context['db']
        users = db.scalars(select(UserModel)).all()
        resp.media = [
            {"id": u.id, "name": u.name, "email": u.email} for u in users
        ]

        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        db = req.context['db']

        try:

            body = req.get_media()
            name = body.get('name')
            email = body.get('email')

            new_user = UserModel(name=name, email=email)
            db.add(new_user)
            db.flush()

            resp.media = {
                    "message": "Usuário criado com sucesso!",
                    "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}
                }
            resp.status = falcon.HTTP_201

        except json.JSONDecodeError:
            raise falcon.HTTPBadRequest(
                title="JSON inválido",
                description="O corpo da requisição precisa ser um JSON válido."
            )


app = falcon.App(middleware=[DatabaseSessionMiddleware()])

user_collection_resource = UserCollectionResource()
app.add_route('/users', user_collection_resource)
