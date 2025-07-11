import requests
import uuid
import json

def autenticar_ely(username, password, totp=None):
    url = "https://authserver.ely.by/auth/authenticate"
    client_token = str(uuid.uuid4())

    # Si se usa TOTP (autenticación de dos factores), se concatena al password
    if totp:
        password = f"{password}:{totp}"

    payload = {
        "username": username,
        "password": password,
        "clientToken": client_token,
        "requestUser": True
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        datos = response.json()
        print("✅ Autenticación exitosa")
        return datos
    else:
        try:
            error = response.json()
            print("❌ Error:", error.get("errorMessage", "Error desconocido"))
        except:
            print("❌ Error desconocido:", response.text)

    return None

# === EJEMPLO DE USO ===
# Si el usuario tiene 2FA, pide el token TOTP después del primer intento