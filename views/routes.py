"""
Routes Flask pour OrangeShield.
"""

from flask import Blueprint, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from controllers.watermark_controller import WatermarkController
from services.trustmark_service import TrustMarkService
from config import Config

main_bp = Blueprint('main', __name__)
watermark_controller = WatermarkController()


@main_bp.route('/')
def index():
    """Page d'accueil."""
    trustmark_available = TrustMarkService.is_available()
    return render_template('index.html', trustmark_available=trustmark_available)


@main_bp.route('/apply-watermark', methods=['POST'])
def apply_watermark():
    """Applique le watermark sur l'image uploadée."""
    return watermark_controller.process_watermark_request()


@main_bp.route('/verify-trustmark', methods=['GET', 'POST'])
def verify_trustmark():
    """Vérifie et extrait le message TrustMark d'une image."""
    from flask import request, redirect, url_for
    if request.method == 'GET':
        # Rediriger vers la page principale section verify
        return redirect(url_for('main.index') + '#verify')
    return watermark_controller.verify_trustmark_request()


@main_bp.route('/download/<filename>')
def download_file(filename):
    """Télécharge l'image watermarkée."""
    try:
        secured_filename = secure_filename(filename)
        file_path = os.path.join(Config.OUTPUT_FOLDER, secured_filename)
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='image/jpeg'
            )
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
