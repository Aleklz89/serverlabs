from flask_smorest import Api

from serverlabs import app



from serverlabs.resources.user import blp as UserBlueprint
from serverlabs.resources.category import blp as CategoryBlueprint
from serverlabs.resources.record import blp as RecordBlueprint

app.config["PROPAGATE_EXCEPTION"] = True
app.config["API_TITLE"] = "Finance REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPEN_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm.swagger-ui-dist/"

api = Api(app)

api.register_blueprint(UserBlueprint)
api.register_blueprint(CategoryBlueprint)
api.register_blueprint(RecordBlueprint)

