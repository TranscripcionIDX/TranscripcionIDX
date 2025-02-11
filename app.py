from flask import Flask, request, jsonify, send_file
import os
app = Flask(__name__)
# Asegurar que los archivos existen
for archivo in ["transcripcion_audio.txt", "transcripcion_microfono.txt"]:
    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("")
def guardar_en_archivo(texto, nombre_archivo):
    """ Guarda la transcripción en un archivo de texto específico en tiempo real """
    try:
        with open(nombre_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        return True
    except Exception as e:
        print(f"Error al guardar en {nombre_archivo}: {e}")
        return False
@app.route('/guardar_transcripcion', methods=['POST'])
def guardar_transcripcion():
    data = request.json
    texto = data.get("texto", "")
    archivo = data.get("archivo", "")
    if not texto:
        return jsonify({"error": "No hay texto para guardar"}), 400
    if archivo not in ["transcripcion_audio.txt", "transcripcion_microfono.txt"]:
        return jsonify({"error": "Nombre de archivo no válido"}), 400
    if guardar_en_archivo(texto, archivo):
        return jsonify({"mensaje": f"Transcripción guardada en {archivo}"}), 200
    else:
        return jsonify({"error": "Error al guardar la transcripción"}), 500
@app.route('/descargar_transcripcion', methods=['GET'])
def descargar_transcripcion():
    archivo = request.args.get("archivo", "transcripcion_microfono.txt")
    
    if archivo not in ["transcripcion_audio.txt", "transcripcion_microfono.txt"]:
        return jsonify({"error": "Nombre de archivo no válido"}), 400
    
    if os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404
if __name__ == '__main__':
    app.run(debug=True)