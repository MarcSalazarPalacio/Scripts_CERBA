def bed_file_downloader(panel):

    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    import time

### Generar el webdriver ###

    try:

    # Generar el webdriver: Al parecer, esta versión de chrome necesita esta línea de código
    # extra llamada "executable_path" para poder acceder a donde hemos guardado el driver.

        driver_path = "C:/Users/Usuario/Documents/Formación_Académica/Marc/Programación/Python/chromedriver.exe"
        cService = webdriver.ChromeService(executable_path = driver_path)

    # Configurar las opciones del webdriver. La variable prefs hace que se puedan descargar archivos sin límites:

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.automatic_downloads": 1}
        options.add_experimental_option("prefs", prefs)

    # Inicializar el navegador con las opciones configuradas y el ChromeDriver:

        driver = webdriver.Chrome(service = cService, options = options)

    except:

        print("Ha ocurrido un error al gener el webdriver. Asegúrate de que la ruta donde está guardado el driver sea correcta.")



### Cargar el archivo txt donde guardamos usuario y contraseña ###

    try:

    # Ruta donde se encuentra el txt:

        txt = open("C:/Users/Usuario/Documents/Formación_Académica/Marc/Programación/Python/user_password.txt", "r+")

    # El usuario debería estar en la primera línea del txt y la contraseña en la segunda línea:

        user = txt.readline()
        password = txt.readline()
        txt.close()

    except:

        print("Ha ocurrido un error al cargar el documento que contiene el usuario y la contraseña. Asegúrate de que la ruta sea correcta.")



### Iniciar sesion en la página web de Illumina ###

    try:

    # Abrir la pagina principal de Illumina:

        driver.get("https://euc1.sh.basespace.illumina.com/dashboard")

    # Introducir el usuario que está en la primera línea del txt:

        WebDriverWait(driver, 10) \
            .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'email']"))) \
            .send_keys(user)

    # Introducir la contraseña que está en la segunda línea del txt:

        WebDriverWait(driver, 10) \
            .until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']"))) \
            .send_keys(password)

    # Ruta XPath del 'Botón' para inciar sesión en la página web de Illumina:

        login = "/html/body/div/div[2]/div/div/div/div/div/div/div[3]/div/form/div[2]/div[4]/div[1]/input[1]"

    # Clickar en el boton de inicio de sesión:

        login_button = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, login)))
        driver.execute_script("arguments[0].click();", login_button)

    except:

        print("Ha ocurrido un error al inciar sesión. Asegúrate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir.")



### Cambiar al usuario de CERBA BIOMOL ###

    try:

    # Cambiar de usuario:

        time.sleep(1)

    # Ruta XPath del 'Botón' desplegable para seleccionar 'usuarios':

        users = "/html/body/section/section[1]/app-bs-univ-nav-bar/lib-universal-navbar/div/div/section[1]/ul/li[1]/div/button"

    # Clickar en el desplegable:

        user_selection = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, users)))
        driver.execute_script("arguments[0].click();", user_selection)

    # Clickar en el usuario 'Cerba_BIomol' mediante la inspección de elementos:

        user_change = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='Cerba_BIomol']")))
        driver.execute_script("arguments[0].click();", user_change)

    except:

        print("Ha ocurrido un error al cambiar de usuario. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")



### Seleccionar los proyectos ###

    try:

        time.sleep(1)

    # Ruta XPath del 'Botón' desplegable para seleccionar 'projects':

        projects = "/html/body/section/section[1]/app-bs-univ-nav-bar/lib-universal-navbar/div/div/section[2]/div[1]/button"

    # Clickar en el desplegable:

        selection = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, projects)))
        driver.execute_script("arguments[0].click();", selection)

    # Clickar en 'projects' mediante el metodo 'LINK_TEXT':

        projects_select = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Projects")))
        driver.execute_script("arguments[0].click();", projects_select)

    except:

        print("Ha ocurrido un error al seleccionar los proyectos. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")



### Seleccionar el panel ###

    try:

        time.sleep(1)

    # Clickar en el panel mediante el metodo 'LINK_TEXT':

        try:
            panel = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Panel_" + str(panel))))
            driver.execute_script("arguments[0].click();", panel)

        except:
            panel = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Panel_0" + str(panel))))
            driver.execute_script("arguments[0].click();", panel)

    except:

        print("Ha ocurrido un error al seleccionar el panel. Comprueba que el nombre del panel comience con 'Panel_'")



### Seleccionar los ficheros del panel ###

    try:

        time.sleep(1)

    # Clickar en el 'Other Datasets' mediante el metodo 'CSS_SELECTOR':

        other_files = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[title = 'Other Datasets']")))
        driver.execute_script("arguments[0].click();", other_files)

    except:

        print("Ha ocurrido un error al seleccionar los ficheros del panel. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")

### Contar el número de muestras por panel ###

    try:

        time.sleep(2)

        contenido_html = driver.page_source
        soup = BeautifulSoup(contenido_html, 'html.parser')

        # Cadena de texto buscada:

        cadena_buscada = 'DRAGEN Enrichment'

        # Número de muestras en el panel:

        references = (contenido_html.count(cadena_buscada)) / 2  # DRAGEN Enrichment sale 2 veces por muestra.
        if references <= 12:
            print("Cambia la cadena de texto buscada en caso de que haya más de 12 muestras.")

    except:

        print("Ha ocurrido un error al contar el número de muestras del panel. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir.")




### Bucle para descargar el fichero .bed de cada muestra ###

    for i in range(1, int(references) + 1):

### Seleccionar una muestra ###

        try:

            time.sleep(2)

        # Ruta XPath del 'Botón' desplegable para visualizar los ficheros de la muestra:

            sample = "/html/body/section/section[2]/app-project-details/section[2]/div/app-project-details-other-datasets/div/lib-data-table/ag-grid-angular/div/div[2]/div[1]/div[3]/div[2]/div/div/div["+ str(i) +"]/div[1]/div/span[2]/lib-data-table-link/a"

        # Clickar en la muestra mediante el metodo 'XPATH':

            elemento = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, sample)))
            driver.execute_script("arguments[0].click();", elemento)

        except:

            print("Ha ocurrido un error al seleccionar la siguiente muestra. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")



### Desplegar los ficheros de la muestra ###

        try:

            time.sleep(2)

            desplegable = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "span[class='filename']")))
            driver.execute_script("arguments[0].click();", desplegable)

        except:

            print("Ha ocurrido un error al desplegar los archivos de la muestra. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")



### Seleccionar el fichero .bed y descargarlo ###

        try:

            time.sleep(2)

            intentos = 0

        # Buscar el fichero .bed y clickarlo:

            while True:

                try:

                # Ruta XPath del fichero .bed:

                    bed = "/html/body/section/section[2]/app-analysis-details/section[2]/div/app-analysis-details-files/app-file-browser/div/lib-file-browser/div/div/ag-grid-angular/div/div[2]/div[1]/div[3]/div[2]/div/div/div[61]/div[1]/span/span[4]/span/a"

                # Clickar en el fichero .bed mediante el metodo 'XPATH':

                    bed_file = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, bed)))
                    driver.execute_script("arguments[0].click();", bed_file)

                except:

                # Volver a desplegar los ficheros si no ha sido encontrado el archivo .bed:

                    desplegable = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "span[class='filename']")))
                    driver.execute_script("arguments[0].click();", desplegable)

                # Aumentar el número de intentos. Si llegamos a 5 intentos de desplegable, finalizamos en bucle:

                    intentos += 1
                    if intentos > 5:
                        print("Algo falla, probablemente la conexión con los servidores no sea óptima.")
                    break

        # Descargar el fichero .bed:

                else:

                # Ruta XPath del 'botón' para descargar el fichero:

                    download = "/html/body/app-file-preview-modal/div/ngx-smart-modal/div/div/div/div/div[2]/div[2]/button"

                # Clickar en la descarga mediante el método 'XPATH':

                    download_file = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, download)))
                    driver.execute_script("arguments[0].click();", download_file)
                    break

        except:

            print("Ha ocurrido un error al encontrar el fichero bed. Aségurate de que la página web de Illumina no haya cambiado respecto a como siempre suele lucir o súbele el tiempo al 'time.sleep()'")


### Volver a la selección de muestras ###

        try:

            time.sleep(2)

# Retroceder en el navegador:

            if i < 24:
                driver.execute_script("window.history.go(-1)")

        except:

            print("Ha ocurrido un error al retroceder a la ventana de muestras. Prueba a subir el tiempo de 'time.sleep()'")






bed_file_downloader(49)