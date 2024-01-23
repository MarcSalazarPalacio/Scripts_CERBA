def bed_file_downloader(panel):

    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import time

    try:

# Generar el webdriver: Al parecer, esta versión de chrome necesita esta línea de código
# extra llamada "executable_path" para poder acceder a donde hemos guardado el driver.

        driver_path = "C:/Users/Usuario/Documents/Formación_Académica/Marc/Programación/Python/chromedriver.exe"
        cService = webdriver.ChromeService(executable_path = driver_path)

# Configurar la ubicación de descarga

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option("prefs", prefs)

# Inicializar el navegador con las opciones configuradas y el ChromeDriver:

        driver = webdriver.Chrome(service = cService, options = options)

# Cargar el archivo txt donde guardamos usuario y contraseña:

        txt = open("C:/Users/Usuario/Documents/Formación_Académica/Marc/Programación/Python/user_password.txt", "r+")
        user = txt.readline()
        password = txt.readline()
        txt.close()

# Abrir la pagina principal de Illumina:

        driver.get("https://euc1.sh.basespace.illumina.com/dashboard")

# Acceder mediante credenciales:

        WebDriverWait(driver, 10) \
            .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'email']"))) \
            .send_keys(user)

        WebDriverWait(driver, 10) \
            .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']"))) \
            .send_keys(password)

        login = "/html/body/div/div[2]/div/div/div/div/div/div/div[3]/div/form/div[2]/div[4]/div[1]/input[1]"
        login_button = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, login)))
        driver.execute_script("arguments[0].click();", login_button)

# Cambiar de usuario:

        time.sleep(1)

        users = "/html/body/section/section[1]/app-bs-univ-nav-bar/lib-universal-navbar/div/div/section[1]/ul/li[1]/div/button"
        user_selection = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, users)))
        driver.execute_script("arguments[0].click();", user_selection)

        user_change = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='Cerba_BIomol']")))
        driver.execute_script("arguments[0].click();", user_change)

# Seleccionar los proyectos:

        time.sleep(1)

        projects = "/html/body/section/section[1]/app-bs-univ-nav-bar/lib-universal-navbar/div/div/section[2]/div[1]/button"

        selection = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, projects)))
        driver.execute_script("arguments[0].click();", selection)

        projects_select = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Projects")))
        driver.execute_script("arguments[0].click();", projects_select)

# Seleccionar el panel que deseamos descargar:

        time.sleep(1)

        try:
            panel = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Panel_" + str(panel))))
            driver.execute_script("arguments[0].click();", panel)

        except:
            panel = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Panel_0" + str(panel))))
            driver.execute_script("arguments[0].click();", panel)

# Seleccionar 'otros ficheros':

        time.sleep(1)

        other_files = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[title = 'Other Datasets']")))
        driver.execute_script("arguments[0].click();", other_files)

        time.sleep(2)

# Contar cuantas muestras tenemos en el panel:

        try:
            contenido_html = driver.page_source
            soup = BeautifulSoup(contenido_html, 'html.parser')
            cadena_buscada = 'DRAGEN Enrichment'
            references = (contenido_html.count(cadena_buscada)) / 2  # DRAGEN Enrichment sale 2 veces por muestra.

        except:
            print("Cambiar la cadena buscada.")
            return

# Iniciamos bucle de descarga:

        for i in range(1, int(references) + 1):

# Seleccionar muestra:

            time.sleep(2)

            sample = "/html/body/section/section[2]/app-project-details/section[2]/div/app-project-details-other-datasets/div/lib-data-table/ag-grid-angular/div/div[2]/div[1]/div[3]/div[2]/div/div/div["+ str(i) +"]/div[1]/div/span[2]/lib-data-table-link/a"
            elemento = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, sample)))
            driver.execute_script("arguments[0].click();", elemento)

            time.sleep(2)

# Desplegar muestra:

            desplegable = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "span[class='filename']")))
            driver.execute_script("arguments[0].click();", desplegable)

            time.sleep(2)

# Seleccionar el fichero bed:

            intentos = 0

            while True:

                try:
                    bed = "/html/body/section/section[2]/app-analysis-details/section[2]/div/app-analysis-details-files/app-file-browser/div/lib-file-browser/div/div/ag-grid-angular/div/div[2]/div[1]/div[3]/div[2]/div/div/div[61]/div[1]/span/span[4]/span/a"
                    bed_file = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, bed)))
                    driver.execute_script("arguments[0].click();", bed_file)

                except:
                    desplegable = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "span[class='filename']")))
                    driver.execute_script("arguments[0].click();", desplegable)
                    intentos += 1
                    if intentos > 5:
                        print("Error al refrescar la pagina.")
                    break

# Descargar fichero bed:

                else:
                    download = "/html/body/app-file-preview-modal/div/ngx-smart-modal/div/div/div/div/div[2]/div[2]/button"
                    download_file = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, download)))
                    driver.execute_script("arguments[0].click();", download_file)
                    break

# Volver a seleccionar muestras:

            time.sleep(2)

            driver.execute_script("window.history.go(-1)")

        error = 0
        print(error)

    except:
        print("Ha ocurrido un error. Las fuentes de error más comunes al ejecutar este scritp suelen ser: \n- Minimizar la venta del navegador\n- Conexión a internet demasiado lenta\n- Fallos en los servidores de Illumina\n- Cambioa de la página web\nRevisa estos posibles escenarios.")
        error = 1


bed_file_downloader(49)