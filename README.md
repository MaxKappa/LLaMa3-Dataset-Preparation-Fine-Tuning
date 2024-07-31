
# Log Processor and CSV Converter

## Descrizione

Questo progetto consiste in una serie di script Python che lavorano insieme per processare file di log, convertire file CSV e filtrare dati. Utilizza `pymongo` per interagire con un database MongoDB, `python-dotenv` per la gestione delle variabili di configurazione, e `pandas` per la manipolazione dei dati.

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
    git clone https://github.com/tuo-username/log-processor-csv-converter.git
    ```

2. Vai nella directory del progetto:

    ```sh
    cd log-processor-csv-converter
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
## Licenza

Questo progetto è distribuito sotto la licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.
