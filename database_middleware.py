from database import SessionLocal


class DatabaseSessionMiddleware:

    def process_resource(self, req, resp, resource, param):
        req.context['db'] = SessionLocal()


    def process_response(self, req, resp, resource, req_succeeded):
        db = req.context.get('db')

        if db is not None:
            try:
                if req_succeeded:
                    db.commit()
                else:
                    db.rollback()
            except:
                db.rollback()
                raise
            finally:
                db.close()