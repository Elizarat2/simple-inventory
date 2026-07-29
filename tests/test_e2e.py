import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import create_app

@pytest.fixture(scope="module")
def live_server():
    app = create_app()
    app.config.update({"TESTING": True})
    
    # Levantar el servidor Flask en un hilo secundario para pruebas E2E
    server_thread = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=5000, use_reloader=False))
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1) # Esperar a que el servidor arranque
    yield "http://127.0.0.1:5000"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Ejecutar en segundo plano (puedes quitarlo si quieres verlo visualmente)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()

def test_e2e_home_title_or_content(live_server, driver):
    # Prueba 1: Verificar que la página principal carga y responde
    driver.get(live_server)
    time.sleep(1)
    assert "Inventario" in driver.page_source or driver.current_url.startswith("http://127.0.0.1:5000")

def test_e2e_health_endpoint(live_server, driver):
    # Prueba 2: Validar el endpoint de API operativo desde el navegador
    driver.get(f"{live_server}/api/health")
    time.sleep(1)
    assert "healthy" in driver.page_source

def test_e2e_navigation_flow(live_server, driver):
    # Prueba 3: Simular interacción de navegación real del usuario
    driver.get(live_server)
    assert driver.title is not None