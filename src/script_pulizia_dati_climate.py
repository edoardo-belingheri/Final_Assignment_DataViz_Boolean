# pulizia_dati_climate.py
"""
Script per la pulizia automatica dei dati Climate ESS
Da utilizzare per pulire nuovi file CSV con la stessa struttura
"""

import pandas as pd
import numpy as np


def carica_dati(climate_path, variables_path=None):
    """
    Carica i dati dai file CSV
    
    Parameters:
    -----------
    climate_path : str
        Percorso del file Climate Data Clean.csv
    variables_path : str, optional
        Percorso del file variables.csv (opzionale, per reference)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con i dati climatici
    """
    print(f"\nCaricamento dati dal file: {climate_path}")
    climate = pd.read_csv(climate_path)
    
    if variables_path:
        print(f"\nCaricamento dati dal file: {variables_path}")
        variables = pd.read_csv(variables_path)
        return climate, variables
    return climate


def rimuovi_colonne_inutili(df):
    """
    Rimuove colonne metadata non necessarie per l'analisi
    """
    colonne_da_rimuovere = ["Unnamed: 0", "name", "essround", "edition", "proddate"]
    print(f"\nRimozione colonne inutili: {', '.join(colonne_da_rimuovere)}")
    df = df.drop(columns=colonne_da_rimuovere, errors='ignore')
    return df


def verifica_duplicati(df):
    """
    Verifica duplicati basate su tutte le colonne
    e rimuove eventuali righe duplicate
    """
    duplicates = df.drop_duplicates(keep=False)
    n_removed = len(df) - len(duplicates)
    if n_removed >= 0:
        print(f"\nRimossi {n_removed} duplicati")
    return duplicates


def converti_tipi_dati(df):
    """
    Converte le colonne numeriche in Int32 per gestire i NaN
    """
    colonne_int = [
        'eneffap', 'rdcenr', 'cflsenr', 'elgcoal', 'elgngas', 'elghydr',
        'elgnuc', 'elgsun', 'elgwind', 'elgbio',
        'ccnthum', 'ccrdprs',
        'ccgdbd', 'lkredcc', 'lklmten', 'gvsrdcc',
        'ownrdcc'
    ]
    print(f"\nConversione tipi di dati numerici: {', '.join(colonne_int)}")
    for col in colonne_int:
        if col in df.columns:
            df[col] = df[col].astype('Int32')
    return df


def rinomina_colonne(df):
    """
    Rinomina le colonne con nomi descrittivi in italiano.
    
    Questa funzione mappa i nomi tecnici delle colonne (es. 'eneffap') 
    in nomi descrittivi in italiano (es. 'prob_acquisto_apparecchio_efficiente')
    per rendere il dataset più leggibile e comprensibile.
    
    I gruppi di colonne rinominati sono:
    - Gruppo 1: eneffap → elghydr (azioni di risparmio energetico)
    - Gruppo 2: elgnuc → elgbio (quote di energia per fonte)
    - Gruppo 3: wrpwrct → wrtratc (preoccupazioni su interruzioni)
    - Gruppo 4: clmchng → ccrdprs (opinioni sul cambiamento climatico)
    - Gruppo 5: wrclmch → gvsrdcc (preoccupazioni e probabilità)
    - Gruppo 6: ownrdcc → banhhap (efficacia azioni e posizioni politiche)
    """
    rename_map = {
        # Gruppo 1: da eneffap a elghydr - Azioni di risparmio energetico
        'eneffap': 'prob_acquisto_apparecchio_efficiente',
        'rdcenr': 'freq_azioni_risparmio_energ',
        'cflsenr': 'confidenza_ridurre_consumo_energ',
        'elgcoal': 'quota_elettr_da_carbone',
        'elgngas': 'quota_elettr_da_gas_naturale',
        'elghydr': 'quota_elettr_da_idroelettrico',
        
        # Gruppo 2: da elgnuc a elgbio - Fonti di energia elettrica
        'elgnuc': 'quota_elettr_da_nucleare',
        'elgsun': 'quota_elettr_da_solare',
        'elgwind': 'quota_elettr_da_eolico',
        'elgbio': 'quota_elettr_da_biomassa',
        
        # Gruppo 3: da wrpwrct a wrtratc - Preoccupazioni su interruzioni energetiche
        'wrpwrct': 'preoccupa_tagli_elettr',
        'wrenexp': 'preoccupa_energ_troppo_costosa',
        'wrdpimp': 'preoccupa_dipend_import_energ',
        'wrdpfos': 'preoccupa_dipend_combust_fossili',
        'wrntdis': 'preoccupa_interruz_disastri_nat',
        'wrinspw': 'preoccupa_interruz_produz_insuff',
        'wrtcfl': 'preoccupa_interruz_guasti_tecnici',
        'wrtratc': 'preoccupa_interruz_attacc_terror',
        
        # Gruppo 4: da clmchng a ccrdprs - Opinioni sul cambiamento climatico
        'clmchng': 'opinione_clima_sta_cambiando',
        'clmthgt1': 'quanto_ci_pensa_negazionista',
        'clmthgt2': 'quanto_ci_pensa_non_negazionista',
        'ccnthum': 'cause_cambiamento_climatico',
        'ccrdprs': 'responsabilita_personale_clima',
        
        # Gruppo 5: da wrclmch a gvsrdcc - Preoccupazioni e probabilità di azione
        'wrclmch': 'preoccup_camb_clima',
        'ccgdbd': 'impatto_globale_clima',
        'lkredcc': 'impatto_rid_energ_larga_scala',
        'lklmten': 'prob_rid_energ_larga_scala',
        'gvsrdcc': 'prob_intervent_governi',
        
        # Gruppo 6: ultime colonne - Efficacia personale e posizioni politiche
        'ownrdcc': 'efficacia_azione_personale',
        'inctxff': 'posizione_increm_tasse_fossili',
        'sbsrnen': 'posizione_sussidi_energ_rinn',
        'banhhap': 'posizione_divieto_elettrodom_inef'
    }
    
    print(f"\nRinomina colonne: {len(rename_map)} colonne rinominate")
    df = df.rename(columns=rename_map, errors='ignore')
    return df


def mappa_valori_categorici(df):
    """
    Mappa i valori numerici in etichette categoriche descrittive.
    
    Questa funzione converte i codici numerici (1-6, 1-5, 1-4) in 
    etichette testuali più comprensibili per l'analisi.
    
    Le mappature effettuate sono:
    - Frequenza azioni risparmio (1-6): Never → Always
    - Opinione cambiamento climatico (1-4): Definitely changing → Definitely not changing
    - Quanto ci pensa (1-5): Not at all → A great deal
    """
    
    # Mappatura per freq_azioni_risparmio_energ (1-6)
    # 1=Mai, 2=Quasi mai, 3=Qualche volta, 4=Spesso, 5=Molto spesso, 6=Sempre
    label_map_frequenza = {
        1: "Never",
        2: "Hardly ever",
        3: "Sometimes",
        4: "Often",
        5: "Very often",
        6: "Always"
    }
    
    if 'freq_azioni_risparmio_energ' in df.columns:
        print("\nMappatura frequenza azioni risparmio energia...")
        df['freq_azioni_risparmio_energ'] = df['freq_azioni_risparmio_energ'].map(
            label_map_frequenza, na_action='ignore'
        )
    
    # Mappatura per opinioni sul cambiamento climatico (1-4)
    # 1=Sicuramente in cambiamento, 2=Probabilmente, 3=Probabilmente no, 4=Sicuramente no
    label_map_opinione = {
        1: "Definitely changing",
        2: "Probably changing",
        3: "Probably not changing",
        4: "Definitely not changing"
    }
    
    if 'opinione_clima_sta_cambiando' in df.columns:
        print("Mappatura opinione cambiamento climatico...")
        df['opinione_clima_sta_cambiando'] = df['opinione_clima_sta_cambiando'].map(
            label_map_opinione, na_action='ignore'
        )
    
    # Mappatura per quanto_ci_pensa (1-5)
    # 1=Per niente, 2=Molto poco, 3=Qualche volta, 4=Molto, 5=Moltissimo
    label_map_pensiero = {
        1: "Not at all",
        2: "Very little",
        3: "Some",
        4: "A lot",
        5: "A great deal"
    }
    
    colonne_pensiero = ['quanto_ci_pensa_negazionista', 'quanto_ci_pensa_non_negazionista']
    for col in colonne_pensiero:
        if col in df.columns:
            print(f"Mappatura {col}...")
            df[col] = df[col].map(label_map_pensiero, na_action='ignore')
    
    return df


def riclassifica_quote_energia(df):
    """
    Riclassifica le quote di energia in categorie Large/Medium/Small.
    
    Converte i valori numerici (1-5) delle preferenze sulle quote di energia
    elettrica da diverse fonti in categorie semantiche:
    - Large (1-2): Grande quota di elettricità
    - Medium (3): Quota media
    - Small (4-5): Piccola quota
    
    Colonne elaborate: tutte le colonne 'quota_elettr_da_*'
    """
    lista_quote = [
        'quota_elettr_da_carbone', 'quota_elettr_da_gas_naturale', 
        'quota_elettr_da_idroelettrico', 'quota_elettr_da_nucleare', 
        'quota_elettr_da_solare', 'quota_elettr_da_eolico', 
        'quota_elettr_da_biomassa'
    ]
    
    def riclassifica_quantita(val):
        """Converte 1-2 → Large, 3 → Medium, 4-5 → Small"""
        if val in [1, 2]:
            return "Large"
        elif val == 3:
            return "Medium"
        elif val in [4, 5]:
            return "Small"
        else:
            return pd.NA
    
    print(f"\nRiclassificazione quote energia: {len(lista_quote)} colonne")
    for col in lista_quote:
        if col in df.columns:
            df[col] = df[col].apply(riclassifica_quantita)
    
    return df


def riclassifica_preoccupazioni(df):
    """
    Riclassifica le variabili di preoccupazione in Small/Medium/Large.
    
    Converte i valori numerici (1-5, con 7-9 come missing) delle 
    preoccupazioni su vari aspetti energetici in categorie:
    - Small (1-2): Poca preoccupazione
    - Medium (3): Preoccupazione media
    - Large (4-5): Molta preoccupazione
    - NaN (7-9): Valori mancanti/rifiuti
    """
    lista_preoccupazioni = [
        'preoccupa_tagli_elettr', 'preoccupa_energ_troppo_costosa', 
        'preoccupa_dipend_import_energ', 'preoccupa_dipend_combust_fossili',
        'preoccupa_interruz_disastri_nat', 'preoccupa_interruz_produz_insuff',
        'preoccupa_interruz_guasti_tecnici', 'preoccupa_interruz_attacc_terror'
    ]
    
    def riclassifica_preoccupazione(val):
        """Converte 1-2 → Small, 3 → Medium, 4-5 → Large, 7-9 → NaN"""
        if val in [1, 2]:
            return "Small"
        elif val == 3:
            return "Medium"
        elif val in [4, 5]:
            return "Large"
        elif val in [7, 8, 9]:
            return pd.NA
        else:
            return pd.NA
    
    print(f"\nRiclassificazione preoccupazioni: {len(lista_preoccupazioni)} colonne")
    for col in lista_preoccupazioni:
        if col in df.columns:
            df[col] = df[col].apply(riclassifica_preoccupazione)
    
    return df


def riclassifica_cause_clima(df):
    """
    Riclassifica le cause del cambiamento climatico.
    
    Converte i valori numerici (1-5) sulla percezione delle cause 
    del cambiamento climatico in categorie semantiche:
    - Natural Processes (1-2): Solo processi naturali
    - Equally (3): Entrambe ugualmente
    - Human Activity (4-5): Principalmente attività umane
    """
    def riclassifica_cause(val):
        """Converte 1-2 → Natural, 3 → Equally, 4-5 → Human"""
        if val in [1, 2]:
            return "Natural Processes"
        elif val == 3:
            return "Equally"
        elif val in [4, 5]:
            return "Human Activity"
        else:
            return pd.NA
    
    if 'cause_cambiamento_climatico' in df.columns:
        print("\nRiclassificazione cause cambiamento climatico...")
        df['cause_cambiamento_climatico'] = df['cause_cambiamento_climatico'].apply(
            riclassifica_cause
        )
    
    return df


def riclassifica_preoccupa_clima(df):
    """
    Riclassifica preoccupazione sul cambiamento climatico.
    
    Converte i valori numerici (1-5, con 7-9 come missing) della 
    preoccupazione generale sul cambiamento climatico in categorie:
    - Not Worried (1-2): Non preoccupato
    - Somewhat worried (3): Abbastanza preoccupato
    - Very worried (4-5): Molto preoccupato
    """
    def preoccupa_clima(val):
        """Converte 1-2 → Not Worried, 3 → Somewhat, 4-5 → Very worried"""
        if val in [1, 2]:
            return "Not Worried"
        elif val == 3:
            return "Somewhat worried"
        elif val in [4, 5]:
            return "Very worried"
        elif val in [7, 8, 9]:
            return pd.NA
        else:
            return pd.NA
    
    if 'preoccup_camb_clima' in df.columns:
        print("\nRiclassificazione preoccupazione cambiamento climatico...")
        df['preoccup_camb_clima'] = df['preoccup_camb_clima'].apply(
            preoccupa_clima
        )
    
    return df


def riclassifica_tasse(df):
    """
    Riclassifica le posizioni sulle politiche fiscali e ambientali.
    
    Converte i valori numerici (1-5, con 7-9 come missing) delle opinioni
    su politiche ambientali in categorie:
    - In Favour (1-2): A favore
    - Neither (3): Neutrale
    - Against (4-5): Contrario
    
    Colonne elaborate:
    - posizione_increm_tasse_fossili: Tasse su combustibili fossili
    - posizione_sussidi_energ_rinn: Sussidi energie rinnovabili
    - posizione_divieto_elettrodom_inef: Divieto elettrodomestici inefficienti
    """
    lista_tasse = [
        'posizione_increm_tasse_fossili',
        'posizione_sussidi_energ_rinn',
        'posizione_divieto_elettrodom_inef'
    ]
    
    def riclassifica_tassa(val):
        """Converte 1-2 → In Favour, 3 → Neither, 4-5 → Against, 7-9 → NaN"""
        if val in [1, 2]:
            return "In Favour"
        elif val == 3:
            return "Neither"
        elif val in [4, 5]:
            return "Against"
        elif val in [7, 8, 9]:
            return pd.NA
        else:
            return pd.NA
    
    print(f"\nRiclassificazione posizioni politiche: {len(lista_tasse)} colonne")
    for col in lista_tasse:
        if col in df.columns:
            df[col] = df[col].apply(riclassifica_tassa)
    
    return df


def pulisci_dati(climate_path, output_path=None):
    """
    Funzione principale che esegue tutta la pipeline di pulizia
    
    Parameters:
    -----------
    climate_path : str
        Percorso del file CSV da pulire
    output_path : str, optional
        Percorso dove salvare il file pulito. Se None, restituisce solo il DataFrame
        
    Returns:
    --------
    pd.DataFrame
        DataFrame pulito
    """
    print("\n=================================================")
    print("INIZIO PULIZIA DATI")
    print("=================================================")
    
    # 1. Carica dati
    print(f"\n1. Caricamento dati dal file: {climate_path}")
    df = carica_dati(climate_path)
    print(f"   Righe: {len(df)}, Colonne: {len(df.columns)}")
    
    # 2. Rimuovi colonne inutili
    print("\n2. Rimozione colonne inutili...")
    df = rimuovi_colonne_inutili(df)
    print(f"   Colonne rimanenti: {len(df.columns)}")
    
    # 3. Verifica duplicati
    print("\n3. Verifica duplicati...")
    df = verifica_duplicati(df)
    
    # 4. Converti tipi di dati
    print("\n4. Conversione tipi di dati...")
    df = converti_tipi_dati(df)
    
    # 5. Rinomina colonne
    print("\n5. Rinomina colonne con nomi descrittivi...")
    df = rinomina_colonne(df)
    
    # 6. Mappa valori categorici
    print("\n6. Mappatura valori categorici...")
    df = mappa_valori_categorici(df)
    
    # 7. Riclassifica quote energia
    print("\n7. Riclassificazione quote energia (Large/Medium/Small)...")
    df = riclassifica_quote_energia(df)
    
    # 8. Riclassifica preoccupazioni
    print("\n8. Riclassificazione preoccupazioni (Small/Medium/Large)...")
    df = riclassifica_preoccupazioni(df)
    
    # 9. Riclassifica cause clima
    print("\n9. Riclassificazione cause cambiamento climatico...")
    df = riclassifica_cause_clima(df)
    
    # 10. Riclassifica preoccupazione cambiamento climatico
    print("\n10. Riclassificazione preoccupazione generale clima...")
    df = riclassifica_preoccupa_clima(df)
    
    # 11. Riclassifica posizioni politiche/tasse
    print("\n11. Riclassificazione posizioni politiche fiscali...")
    df = riclassifica_tasse(df)
    
    # 12. Salva se richiesto
    if output_path:
        print(f"\n12. Salvataggio file pulito in: {output_path}")
        df.to_csv(output_path, index=False)
        print("   File salvato con successo!")
    
    print("\n=================================================")
    print("PULIZIA COMPLETATA")
    print(f"Dati finali: {len(df)} righe, {len(df.columns)} colonne")
    print("=================================================")
    
    return df


if __name__ == "__main__":
    # Esempio di utilizzo:
    
    # Modifica questi percorsi con i tuoi file
    INPUT_FILE = "data/Climate Data Clean.csv"
    OUTPUT_FILE = "data/climate_pulito.csv"
    
    # Esegui la pulizia
    df_pulito = pulisci_dati(INPUT_FILE, OUTPUT_FILE)
