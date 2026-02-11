# Final Assignment – European Social Survey (ESS) Climate Change Dashboard

Questo progetto è il risultato del Final Assignment del corso di Data Visualization del Master in Data Analytics di Boolean (classe 24).  
L’obiettivo è analizzare le opinioni degli europei riguardo al cambiamento climatico utilizzando i dati della **European Social Survey (ESS) – Round 8 (2016/17)** e costruire una dashboard interattiva in Power BI che rispetti i principi di **Graphical Excellence** e una buona **User Experience**.

---

## 📊 Contesto del progetto

L’ESS è un’indagine europea su larga scala che raccoglie oltre 500 variabili e più di 40.000 risposte.  
Per questo assignment ci si concentra esclusivamente sul **gruppo di domande relative al cambiamento climatico**, contenute nel file:

- **Climate Data Clean.xlsx**  
  (versione parzialmente pulita del dataset, con codici di missing già convertiti in NA)

La documentazione completa del survey è disponibile nel file “ESS Documentation.pdf”.

---

## 🎯 Obiettivo dell’Assignment

Il brief richiede di immaginare di lavorare per il **European Institute for Social Policy (EISP)**, incaricati di produrre una dashboard che:

- permetta agli utenti di **esplorare i dati** sulle opinioni europee riguardo al cambiamento climatico  
- evidenzi **le principali insight** emerse dal dataset  
- presenti le informazioni in modo chiaro, leggibile e coerente con i principi di visualizzazione

La dashboard deve rispondere a domande come:

- Qual era l’opinione generale degli europei sul cambiamento climatico?  
- Quanto erano preoccupati?  
- Quali erano le preferenze energetiche?  
- Come variavano le opinioni tra i diversi Paesi europei?

---

## 🧹 Data Cleaning

La pulizia dei dati è stata effettuata tramite:

- analisi del file “variables.csv” per comprendere struttura e codici  
- gestione dei valori mancanti e dei codici speciali  
- normalizzazione dei nomi delle colonne  
- conversione dei formati numerici e categoriali 

Il codice completo è disponibile in:

- `notebooks/pulizia final assign.ipynb` (per vedere passo dopo passo i ragionamenti fatti) 
- `src/script_pulizia_dati_climate.py`   (per eseguire la pulizia in modo automatico)

---

## 📈 Dashboard in Power BI

La dashboard finale (file `.pbix`) è stata progettata per:

- rispettare i principi di **Graphical Excellence**  
- evitare chart junk e massimizzare la leggibilità  
- utilizzare pre-attentive attributes (colore, forma, posizione)  
- offrire una buona user experience tramite:
  - slicer intuitivi   
  - bookmarks  
  - field parameters

La dashboard si trova in:

- `powerbi/final_assignments.pbix`

---

## 🚀 Come riprodurre il progetto

1. Clona il repository

2. Crea e attiva un ambiente virtuale

3. Installa le dipendenze (requirements.txt)

4. Apri ed esegui le celle del notebook `notebooks/pulizia final assign.ipynb` o esegui lo script `src/script_pulizia_dati_climate.py`.

5. Apri la dashboard Power BI (Installa **Microsoft Power BI Desktop** -> gratuito)
La dashboard utilizza il file: data/Climate Data Pulito.xlsx  
Questo file è stato generato tramite il processo di pulizia svolto in Python.

6. Assicurati che il file “Climate Data Pulito.xlsx” sia nella cartella `data/`,
così Power BI può caricarlo tramite percorso relativo.

7. La dashboard è ora completamente funzionante e permette di esplorare:
- opinioni sul cambiamento climatico
- livello di preoccupazione degli europei
- preferenze energetiche
- differenze tra Paesi





