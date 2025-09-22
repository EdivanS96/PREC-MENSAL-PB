import subprocess

#Agrupas imagens no ImageCollection
# raiz de onde estão suas imagens soltas
src_root = "projects/edivansilva/assets"

# destino: a ImageCollection que você criou
dst_root = "projects/edivansilva/assets/PB-MPGRID"

anos = range(1994, 2025)   # 1994 até 2024
meses = range(1, 13)       # Janeiro (01) até Dezembro (12)

for ano in anos:
    for mes in meses:
        nome = f"PBMPGRID_{ano}_{mes:02d}"
        src = f"{src_root}/{nome}"
        dst = f"{dst_root}/{nome}"

        cmd = ["earthengine", "cp", src, dst]
        print("Copiando:", src, "→", dst)

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("⚠️ Erro ao copiar:", src)
