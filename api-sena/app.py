from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import auth, credentials
from flask_cors import CORS

# Inicializar la app Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para peticiones desde el frontend

# Configurar Firebase con la clave privada
cred = credentials.Certificate("nexus-5c53d-firebase-adminsdk-dzjbj-0e7c69a6d7.json")
firebase_admin.initialize_app(cred)

# Ruta para registrar usuarios
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email y contraseña requeridos"}), 400

        # Crear usuario en Firebase Auth
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "Usuario registrado con éxito", "uid": user.uid}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email y contraseña requeridos"}), 400

        # Iniciar sesión con Firebase
        user = auth.get_user_by_email(email)
        return jsonify({"message": "Autenticación exitosa", "uid": user.uid}), 200

    except Exception:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Ejecutar la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)
