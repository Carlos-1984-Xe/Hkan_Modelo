import argparse
import glob
import os
import pandas as pd
from pathlib import Path

def read_csv_force_seqn(path):
    df = pd.read_csv(path, dtype=str, low_memory=False)
    if 'SEQN' not in df.columns:
        raise ValueError(f"'SEQN' no está en las columnas de {path}")
    df['SEQN'] = df['SEQN'].astype(str)
    return df

def merge_all(csv_paths, how='outer'):
    base = read_csv_force_seqn(csv_paths[0])
    print(f"Base: {os.path.basename(csv_paths[0])} rows={len(base)} cols={len(base.columns)}")
    for p in csv_paths[1:]:
        df = read_csv_force_seqn(p)
        print(f"Merging: {os.path.basename(p)} rows={len(df)} cols={len(df.columns)} (how={how})")
        base = pd.merge(base, df, on='SEQN', how=how, suffixes=('', '_dup'))
        # Resolver columnas duplicadas simples: si existe col_dup y la original vacía, rellenar
        dup_cols = [c for c in base.columns if c.endswith('_dup')]
        for dc in dup_cols:
            orig = dc[:-4]
            if orig in base.columns:
                base[orig] = base[orig].fillna(base[dc])
            else:
                base.rename(columns={dc: orig}, inplace=True)
        # eliminar restantes *_dup
        base = base[[c for c in base.columns if not c.endswith('_dup')]]
    # Eliminar duplicados finales basados en SEQN
    base = base.drop_duplicates(subset=['SEQN'])
    return base

def main():
    parser = argparse.ArgumentParser(description="Merge CSVs por SEQN")
    parser.add_argument('-d', '--dir', default='.', help='Directorio con .csv (por defecto: directorio actual)')
    parser.add_argument('-o', '--out', default='merge_listo.csv', help='Archivo de salida CSV (por defecto: merge_listo.csv)')
    parser.add_argument('--how', choices=['outer', 'inner', 'left', 'right'], default='outer', help='Tipo de join (por defecto outer)')
    args = parser.parse_args()

    path = Path(args.dir)
    csv_paths = sorted([str(p) for p in path.glob('*.csv')])
    if not csv_paths:
        print("No se encontraron archivos .csv en", args.dir)
        return

    try:
        merged = merge_all(csv_paths, how=args.how)
    except Exception as e:
        print("Error:", e)
        return

    merged.to_csv(args.out, index=False)
    print(f"Guardado: {args.out} filas={len(merged)} columnas={len(merged.columns)}")

if __name__ == "__main__":
    main()