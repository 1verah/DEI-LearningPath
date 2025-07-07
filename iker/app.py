import os
import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request
import platform

app = Flask(__name__)

def get_desktop_path():
    """Obtiene la ruta del escritorio según el sistema operativo"""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # Linux
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # En algunos sistemas Linux, el escritorio puede estar en diferentes ubicaciones
        if not os.path.exists(desktop_path):
            desktop_path = os.path.join(os.path.expanduser("~"), "Escritorio")
        return desktop_path

def get_file_tree(path, max_depth=3, current_depth=0):
    """
    Genera un árbol de archivos y carpetas
    """
    if current_depth >= max_depth:
        return []
        
    try:
        items = []
        path_obj = Path(path)
        
        if not path_obj.exists() or not path_obj.is_dir():
            return []
            
        # Obtener todos los elementos del directorio
        for item in sorted(path_obj.iterdir()):
            try:
                # Saltar archivos/carpetas ocultos
                if item.name.startswith('.'):
                    continue
                    
                item_info = {
                    'name': item.name,
                    'path': str(item),
                    'is_dir': item.is_dir(),
                    'size': None,
                    'children': []
                }
                
                if item.is_dir():
                    # Recursivamente obtener contenido de subdirectorios
                    children = get_file_tree(str(item), max_depth, current_depth + 1)
                    if children:
                        item_info['children'] = children
                else:
                    # Obtener tamaño del archivo
                    try:
                        size = item.stat().st_size
                        item_info['size'] = format_file_size(size)
                    except:
                        item_info['size'] = "N/A"
                
                items.append(item_info)
                
            except PermissionError:
                continue
            except Exception as e:
                continue
                
        return items
        
    except Exception as e:
        print(f"Error accediendo a {path}: {e}")
        return []

def format_file_size(size_bytes):
    """Convierte bytes a formato legible"""
    if size_bytes == 0:
        return "0 B"
        
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.1f} {size_names[i]}"

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/desktop-folders')
def get_desktop_folders():
    """API para obtener las carpetas del escritorio"""
    desktop_path = get_desktop_path()
    
    try:
        folders = []
        desktop_obj = Path(desktop_path)
        
        if desktop_obj.exists():
            for item in sorted(desktop_obj.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    folders.append({
                        'name': item.name,
                        'path': str(item)
                    })
        
        return jsonify({
            'success': True,
            'desktop_path': desktop_path,
            'folders': folders
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/folder-tree')
def get_folder_tree_api():
    """API para obtener el árbol de archivos de una carpeta"""
    folder_path = request.args.get('path')
    max_depth = int(request.args.get('depth', 3))
    
    if not folder_path:
        return jsonify({'success': False, 'error': 'No se especificó la ruta'})
    
    try:
        tree = get_file_tree(folder_path, max_depth)
        return jsonify({
            'success': True,
            'tree': tree,
            'path': folder_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def create_templates_directory():
    """Crea el directorio templates si no existe"""
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print(f"✅ Directorio {templates_dir} creado")
    return templates_dir

def main():
    """Función principal"""
    print("🚀 Iniciando Explorador de Archivos Web...")
    print("=" * 50)
    
    # Crear directorio templates
    create_templates_directory()
    
    # Mostrar información del sistema
    desktop_path = get_desktop_path()
    print(f"🖥️  Sistema operativo: {platform.system()}")
    print(f"📁 Escritorio detectado en: {desktop_path}")
    print(f"✅ Escritorio existe: {'Sí' if os.path.exists(desktop_path) else 'No'}")
    
    # Contar carpetas en el escritorio
    try:
        if os.path.exists(desktop_path):
            folders = [f for f in os.listdir(desktop_path)
                       if os.path.isdir(os.path.join(desktop_path, f)) and not f.startswith('.')]
            print(f"📂 Carpetas encontradas: {len(folders)}")
        else:
            print("⚠️  No se pudo acceder al escritorio")
    except Exception as e:
        print(f"⚠️  Error al leer escritorio: {e}")
    
    print("=" * 50)
    print("🌐 Servidor web iniciado en: http://localhost:5000")
    print("🔗 También disponible en: http://127.0.0.1:5000")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    # Iniciar servidor Flask
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")

if __name__ == '__main__':
    main()
