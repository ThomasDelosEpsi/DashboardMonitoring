import tempfile
import shutil
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from multiprocessing import Process, Manager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def launch_browser(profile_dir, site, query, result_dict):
    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)

    try:
        if site == "google":
            driver.get("https://www.google.com")
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            first_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#search a"))
            ).get_attribute("href")
            result_dict["google"] = first_link

        elif site == "amazon":
            driver.get("https://www.amazon.fr")
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            first_obj = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2 a span"))
            ).text
            result_dict["amazon"] = first_obj

        elif site == "cultura":
            driver.get("https://www.cultura.com")
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            first_cd = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-item__title"))
            ).text
            result_dict["cultura"] = first_cd

        elif site == "auchan":
            driver.get("https://www.auchan.fr")
            search_box = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            first_fruit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.product-thumbnail-title a"))
            ).text
            result_dict["auchan"] = first_fruit

    except Exception as e:
        result_dict[site] = f"Erreur: {e}"

    finally:
        driver.quit()
        shutil.rmtree(profile_dir)

def main():
    manager = Manager()
    result_dict = manager.dict()
    jobs = []

    tasks = [
        ("google", "switch2"),
        ("amazon", "tournevis"),
        ("cultura", "cd"),
        ("auchan", "fruit")
    ]

    for i, (site, query) in enumerate(tasks):
        profile_dir = tempfile.mkdtemp(prefix=f"profile_{i}_")
        p = Process(target=launch_browser, args=(profile_dir, site, query, result_dict))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("resultats_recherche.txt", "w", encoding="utf-8") as f:
        f.write(f"Résultats récupérés le {now} :\n\n")
        for site, result in result_dict.items():
            f.write(f"{site.capitalize()}: {result}\n")

    print("Résultats enregistrés dans resultats_recherche.txt")

if __name__ == "__main__":
    main()
