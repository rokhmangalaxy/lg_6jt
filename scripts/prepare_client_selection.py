"""Extract attachment cells 1/8/9 without borders and prepare a four-logo catalog.
Requires ImageMagick. Artwork is cropped/quantized, not regenerated.
"""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'android-logo/logo-assets';OUT.mkdir(exist_ok=True)
RED=(220,38,38);BLUE=(23,50,87);WHITE=(255,255,255);BLACK=(0,0,0)
source=ROOT/'04-desain/pilihan-client/lampiran-asli.png'
# Cell numbering is left-to-right, top-to-bottom.
regions=[(1,22,22,412,350),(8,465,755,404,351),(9,902,755,404,351)]
for number,x,y,w,h in regions:
 raw=subprocess.check_output(['convert',str(source),'-crop',f'{w}x{h}+{x}+{y}','+repage','-alpha','off','-depth','8','rgb:-'])
 assert len(raw)==w*h*3
 rgba=bytearray()
 for i in range(0,len(raw),3):
  pixel=raw[i:i+3]
  color=min((RED,BLUE,WHITE,BLACK),key=lambda c:sum((pixel[j]-c[j])**2 for j in range(3)))
  rgba.extend((*color,0 if color==BLACK else 255))
 subprocess.run(['convert','-size',f'{w}x{h}','-depth','8','rgba:-','-trim','+repage','-bordercolor','none','-border','24','-strip',f'PNG32:{OUT/f"client-attachment-{number:02d}.png"}'],input=rgba,check=True)
# Already extracted no.4: remove only the connected exterior white.
subprocess.run(['convert',str(ROOT/'04-desain/ekstraksi-logo-04/mcm-04-simbol.png'),'-alpha','on','-fill','none','-draw','matte 0,0 floodfill','-strip',f'PNG32:{OUT/"client-logo-04.png"}'],check=True)
print('Prepared exactly four selected logo sources')
