from flask import Flask
from api.api import mod
from api import api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)
SWAGGER_URL = '/api/v1/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'https://stanley-stackoverflow-lite.herokuapp.com/api/v1'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Stackoverflow-lite api application"
    },

# oauth_config={ # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
# 'clientId': "your-client-id",
# 'clientSecret': "your-client-secret-if-required",
# 'realm': "your-realms",
# 'appName': "your-app-name",
# 'scopeSeparator': " ",
# 'additionalQueryStringParams': {'test': "hello"}
# }
)
app.config['JWT_SECRET_KEY'] = 'testSecretGetsStrong'

jwt = JWTManager(app)

app.register_blueprint(api.mod, url_prefix='/api/v1')
app.register_blueprint(api.mod, url_prefix='/api/v1/auth')
app.register_blueprint(api.mod, url_prefix='/api/v1/questions')
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
