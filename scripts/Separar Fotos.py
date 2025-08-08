import os
import re
import shutil
from datetime import datetime
from pathlib import Path

DIR_ATUAL = Path.cwd()

regex_data = re.compile(r'_(\d{8})')
regex_vsr_info = re.compile(r'-VSR-(.+?)_(\d{8})')  # Pega tudo entre -VSR- e _DATA
regex_ponto = re.compile(r'P(\d+)', re.IGNORECASE)

arquivos = [f for f in os.listdir(DIR_ATUAL) if f.lower().endswith('.jpg')]

for arquivo in arquivos:
    match_data = regex_data.search(arquivo)
    if not match_data:
        continue

    data_str = match_data.group(1)
    try:
        data = datetime.strptime(data_str, "%Y%m%d")
    except ValueError:
        continue

    nome_pasta_data = f"{data.month:02}.{data.day:02}"
    pasta_data = DIR_ATUAL / nome_pasta_data
    pasta_data.mkdir(exist_ok=True)

    destino_final = pasta_data / arquivo

    # Se for VSR
    match_vsr = regex_vsr_info.search(arquivo)
    if match_vsr:
        vsr_bruto = match_vsr.group(1)
        pasta_vsr = pasta_data / "VSR"
        pasta_vsr.mkdir(exist_ok=True)

        # Extrai nome do setor + número do ponto
        partes = re.split(r'[-_ ]+', vsr_bruto)
        setor_nome = ''
        ponto_num = ''

        for parte in partes:
            if re.match(r'P\d+', parte, re.IGNORECASE):
                ponto_num = str(int(parte[1:]))  # remove o 0 à esquerda
            else:
                setor_nome += parte.lower()

        if setor_nome and ponto_num:
            pasta_ponto = pasta_vsr / f"{setor_nome}{ponto_num}"
            pasta_ponto.mkdir(exist_ok=True)

            semana = data.isocalendar()[1]
            destino_final = pasta_ponto / f"w{semana:02}.jpg"
        else:
            destino_final = pasta_vsr / arquivo

    shutil.move(DIR_ATUAL / arquivo, destino_final)

print("✅ Separação concluída com sucesso!")
