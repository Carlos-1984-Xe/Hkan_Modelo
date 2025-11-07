# Unión de CSV por SEQN

Este repositorio contiene un script `merge_csvs.py` que busca todos los archivos
`.csv` en el mismo directorio y los une por la columna `SEQN`.

Cómo usar:

1. Instalar dependencias (opcional, si aún no están instaladas):

```powershell
python -m pip install -r requirements.txt
```

2. Ejecutar el script:

```powershell
python merge_csvs.py
```

Salida:

- `merged_all.csv` en el directorio actual.

Notas:

- Si una columna aparece en varios CSV se conserva la primera 値 no nula encontrada
  (prioridad por el orden de lectura). Si prefieres otra prioridad dímelo y lo cambio.
