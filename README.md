
# LLaMa3-Dataset-Preparation-Fine-Tuning

## Descrizione

Questo progetto in Python crea un dataset per il fine tuning di LLaMa3 per Malware Detection a partire da dei log di sistema estratti con Fibratus.

## Struttura del Progetto

- `logprocessor.py`: Contiene funzioni per elaborare i file di log.
- `csvconverter.py`: Contiene funzioni per convertire file CSV in altri formati.
- `filter.py`: Contiene funzioni per filtrare i dati in base a criteri specifici.
- `main.py`: Punto di ingresso principale per eseguire le operazioni del progetto.
- `mongo.py`: Gestisce le operazioni di interazione con il database MongoDB.
- `config.py`: Gestisce la configurazione del progetto utilizzando `python-dotenv`.

## Requisiti

Assicurati di avere installato i seguenti pacchetti Python:

```plaintext
pymongo
python-dotenv
pandas
```

Puoi installarli utilizzando il file `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Installazione

1. Clona il repository:

    ```sh
    git clone https://github.com/MaxKappa/LLaMa3-Dataset-Preparation-Fine-Tuning.git
    ```

2. Vai nella directory del progetto:

    ```sh
    cd LLaMa3-Dataset-Preparation-Fine-Tuning
    ```

3. Crea un file `.env` nella directory principale del progetto e aggiungi le tue configurazioni MongoDB:

    ```dotenv
    MONGO_URI=your_mongo_uri
    MONGO_DB_NAME=your_database_name
    ```

4. Installa le dipendenze del progetto:

    ```sh
    pip install -r requirements.txt
    ```

## Utilizzo

Esegui lo script principale `main.py` per avviare il processo:

```sh
python main.py
```

