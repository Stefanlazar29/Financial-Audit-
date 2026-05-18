import requests
import json
import csv
import time
import os

def ruleaza_scraping_audit():
    director = os.path.dirname(os.path.abspath(__file__))
    cale_input = os.path.join(director, "stoc_loken.json")
    
    with open(cale_input, 'r', encoding='utf-8') as f:
        date = json.load(f)
        produse = date.get('rows', [])

    print(f"--- Incepem Verificarea Web pentru {len(produse)} produse ---")
    
    raport_vulnerabilitati = []
    
    # Folosim o sesiune pentru a pastra conexiunea deschisa (mai rapid)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    for i, p in enumerate(produse):
        sku = str(p.get('zpart_number', '')).strip()
        nume = p.get('zname', 'N/A')
        stoc = float(p.get('zqstock') or 0)
        pret = float(p.get('zretail_price') or 0)

        if not sku or stoc <= 0:
            continue

        # Incercam sa vedem daca pagina produsului exista pe front-end
        # Formatul URL-ului la Magento este de obicei bazat pe nume, dar putem incerca cautarea
        url_verificare = f"https://domain.ro/catalogsearch/result/?q={sku}"
        
        try:
            response = session.get(url_verificare, timeout=10)
            # Daca primim "Your search returned no results", e punct slab
            if "nu a returnat niciun rezultat" in response.text.lower() or "no results" in response.text.lower():
                problema = "INVIZIBIL PE SITE (Search 0)"
            elif response.status_code == 404:
                problema = "PAGINA INEXISTENTA (404)"
            else:
                # Produsul pare sa existe in cautare, trecem mai departe
                continue
        except:
            continue

        valoare = stoc * pret
        raport_vulnerabilitati.append({
            "SKU": sku, "Nume": nume, "Stoc": stoc, 
            "Pret": pret, "Valoare_Blocata": valoare, "Status": problema
        })
        
        print(f"PROBLEMA: {sku} | {valoare} RON | {problema}")

        # Pauza mica sa nu ne ia drept atac bot
        if i % 10 == 0:
            time.sleep(0.5)
            if i % 100 == 0:
                print(f"Progres: {i}/{len(produse)}...")

    # Salvare
    cale_iesire = os.path.join(director, "Audit_Web_Final.csv")
    if raport_vulnerabilitati:
        with open(cale_iesire, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=raport_vulnerabilitati[0].keys())
            writer.writeheader()
            writer.writerows(raport_vulnerabilitati)
        print(f"Gata! Verificarea web a salvat {len(raport_vulnerabilitati)} puncte slabe.")
    else:
        print("Nu s-au gasit probleme prin metoda de cautare web.")

if __name__ == "__main__":
    ruleaza_scraping_audit()
