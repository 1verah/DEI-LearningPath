import subprocess
import sys

def install_flask():
    """Instala Flask si no está disponible"""
    try:
        import flask
        print("✅ Flask ya está instalado")
        return True
    except ImportError:
        print("📦 Instalando Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar Flask")
            print("💡 Intenta ejecutar manualmente: pip install flask")
            return False

def check_dependencies():
    """Verifica todas las dependencias"""
    print("🔍 Verificando dependencias...")
    
    # Verificar módulos estándar
    modules = ['os', 'json', 'pathlib', 'platform']
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}: OK")
        except ImportError:
            print(f"❌ {module}: No disponible")
    
    # Verificar Flask
    flask_ok = install_flask()
    
    if flask_ok:
        print("\n🎉 ¡Todas las dependencias están listas!")
        print("🚀 Ahora puedes ejecutar: python file_explorer_complete.py")
    else:
        print("\n⚠️  Hay problemas con las dependencias")
        print("📋 Dependencias necesarias:")
        print("   - Flask: pip install flask")

if __name__ == "__main__":
    check_dependencies()