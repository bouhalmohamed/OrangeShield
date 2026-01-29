"""
OrangeShield - Protection d'images contre l'IA
Point d'entrée de l'application Flask.
"""

from flask import Flask
from config import Config
from views.routes import main_bp


def create_app(config_class=Config):
    """Crée et configure l'application Flask."""
    import os
    from pathlib import Path
    
    # Get views directory path
    views_dir = Path(__file__).parent / 'views'
    template_dir = views_dir / 'templates'
    static_dir = views_dir / 'static'
    
    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir)
    )
    
    # Initialize configuration
    config_class.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5001))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(debug=debug_mode, host=host, port=port)
