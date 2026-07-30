from flask import Flask, request

from config import Config
from models.db import register_db, init_db
from routes import auth, dashboard, historias, perfil, conquistas, configuracoes, pais, biblioteca, admin, api


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    register_db(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(historias.bp)
    app.register_blueprint(perfil.bp)
    app.register_blueprint(conquistas.bp)
    app.register_blueprint(configuracoes.bp)
    app.register_blueprint(pais.bp)
    app.register_blueprint(biblioteca.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)

    @app.after_request
    def aplicar_cors_na_api(response):
        if request.path.startswith("/api/"):
            response.headers["Access-Control-Allow-Origin"] = app.config["API_CORS_ORIGIN"]
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
        return response

    @app.cli.command("init-db")
    def init_db_command():
        """Cria as tabelas do banco de dados (flask init-db)."""
        init_db(app)
        print("Banco de dados inicializado.")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
