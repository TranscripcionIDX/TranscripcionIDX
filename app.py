from flask import Flask, request, jsonify, send_file
import os
from odf.opendocument import OpenDocumentText
from odf.text import P

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

@app.route('/guardar_transcripcion_odt', methods=['POST'])
def guardar_transcripcion_odt():
    data = request.json
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"error": "No hay texto para guardar"}), 400
    
    # Crear el archivo ODT
    doc = OpenDocumentText()
    
    # Aquí se puede añadir la transcripción con una codificación adecuada
    p = P(text=texto)  # El texto se pasa tal cual
    doc.text.addElement(p)

    # Guardar el archivo con el nombre específico
    try:
        doc.save("transcripcion.odt")  # Guardamos el archivo en la misma carpeta
        return jsonify({"mensaje": "Archivo ODT creado correctamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al guardar el archivo ODT: {e}"}), 500

@app.route('/descargar_transcripcion', methods=['GET'])
def descargar_transcripcion():
    archivo = request.args.get("archivo", "transcripcion.odt")
    
    if archivo not in ["transcripcion_audio.txt", "transcripcion_microfono.txt", "transcripcion.odt"]:
        return jsonify({"error": "Nombre de archivo no válido"}), 400
    
    if os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    else:
        return jsonify({"error": "Archivo no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
