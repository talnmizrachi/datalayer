from flask import send_file
from flask_smorest import Blueprint

import os
# Define the blueprint

heatmap_bp = Blueprint("heatmapping", __name__)


@heatmap_bp.route('/heatmap')
def serve_heatmap():
    # Serve the static HTML file
    html_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'heatmaps/heatmap_with_annotations.html')
    return send_file(html_file_path)

