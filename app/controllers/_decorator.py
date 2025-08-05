from functools import wraps
from flask import jsonify

def handle_api_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        
        except KeyError as e:
            return jsonify({
                "done": False,
                "message": f"حقل مفقود: {str(e)}"
            }), 400

        except ValueError as e:
            return jsonify({
                "done": False,
                "message": str(e)
            }), 400

        except PermissionError as e:
            return jsonify({
                "done": False,
                "message": str(e)
            }), 403

        except Exception as e:
            return jsonify({
                "done": False,
                "message": e
            }), 500
    
    return decorated_function
