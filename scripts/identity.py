import math, colorsys
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'docs/assets'
# Original mathematical ribbon, rendered as a continuous depth-sorted surface.
def point(t, u):
    # One wide, twisting closed ribbon, with a three-lobed center line.
    r=2.15 + .42*math.cos(3*t)
    x=(r+u*math.cos(1.5*t))*math.cos(t)
    y=(r+u*math.cos(1.5*t))*math.sin(t)
    z=.65*math.sin(3*t)+u*math.sin(1.5*t)
    # Oblique view, independent of any scientific data.
    ay=.33; ax=.7
    x,z=x*math.cos(ay)+z*math.sin(ay),-x*math.sin(ay)+z*math.cos(ay)
    y,z=y*math.cos(ax)-z*math.sin(ax),y*math.sin(ax)+z*math.cos(ax)
    a=-.3
    x,y=x*math.cos(a)-y*math.sin(a),x*math.sin(a)+y*math.cos(a)
    return x,y,z
faces=[]
nt,nu=180,24
for i in range(nt):
    t=2*math.pi*i/nt
    for j in range(nu):
        u=-.58+1.16*j/nu
        ps=[point(t,u),point(t+2*math.pi/nt,u),point(t+2*math.pi/nt,u+1.16/nu),point(t,u+1.16/nu)]
        z=sum(p[2] for p in ps)/4
        hue=(.72+.14*math.sin(t-.6)+.035*j/nu)%1
        saturation=.48+.16*math.cos(t)
        lightness=.63+.1*(j/nu)+.06*math.sin(t+1)
        color=colorsys.hls_to_rgb(hue,lightness,saturation)
        fill='#'+''.join(f'{round(v*255):02x}' for v in color)
        d='M'+'L'.join(f'{300+p[0]*86:.2f} {287+p[1]*86:.2f}' for p in ps)+'Z'
        faces.append((z,f'<path d="{d}" fill="{fill}" stroke="{fill}" stroke-width=".35"/>'))
faces.sort()
mesh=''.join(f for _,f in faces)
# A light set of longitudinal lines makes the recursion visible without micro-labels.
strands=[]
for j in range(0,nu+1,2):
    u=-.58+1.16*j/nu
    ps=[point(2*math.pi*i/nt,u) for i in range(nt+1)]
    strands.append('<path d="M'+'L'.join(f'{300+p[0]*86:.2f} {287+p[1]*86:.2f}' for p in ps)+'" fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width=".5"/>')
art=mesh+''.join(strands)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="570" viewBox="0 0 600 570" role="img" aria-labelledby="t d"><title id="t">Harness RSI recursive ribbon</title><desc id="d">Original abstract project artwork: a continuous ribbon twists into a closed form, in violet and blue. This is a brand illustration, not research data.</desc><defs><radialGradient id="g"><stop stop-color="#d6c7ff" stop-opacity=".65"/><stop offset="1" stop-color="#f7f4ff" stop-opacity="0"/></radialGradient></defs><ellipse cx="300" cy="335" rx="280" ry="220" fill="url(#g)"/>{art}</svg>'''
(root/'recursive-loop.svg').write_text(svg)
# Banner uses the same mark, with a readable title and a single research subtitle.
banner=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="540" viewBox="0 0 1440 540" role="img" aria-labelledby="t d"><title id="t">Harness RSI — A living research atlas</title><desc id="d">How agent harnesses evolve. Official project repository with an original violet recursive-ribbon identity.</desc><defs><radialGradient id="bg"><stop stop-color="#eae2ff"/><stop offset="1" stop-color="#faf9ff"/></radialGradient></defs><rect width="1440" height="540" rx="20" fill="#faf9ff"/><ellipse cx="1120" cy="270" rx="340" ry="280" fill="url(#bg)"/><g transform="translate(877 0) scale(.96)">{art}</g><g font-family="Arial,Helvetica,sans-serif"><rect x="65" y="72" width="239" height="34" rx="17" fill="#eee7ff"/><circle cx="86" cy="89" r="4" fill="#7655d7"/><text x="101" y="94" fill="#6148a5" font-size="12" letter-spacing="1.3">LIVING RESEARCH ATLAS</text><text x="61" y="246" fill="#222132" font-size="112" font-weight="600" letter-spacing="-7">Harness <tspan fill="#7853cc">RSI</tspan></text><text x="67" y="307" fill="#55536a" font-size="29" letter-spacing="-.4">How agent harnesses evolve.</text><text x="67" y="359" fill="#858194" font-size="17">Editable components. Emergent mechanisms. Traceable evidence.</text><path d="M67 417H758" stroke="#ded9e8"/><text x="67" y="461" fill="#737083" font-size="12" letter-spacing="1.2">SURVEY + VISUAL ATLAS</text><text x="758" y="461" fill="#737083" font-size="12" letter-spacing="1.2" text-anchor="end">RESEARCH IN PROGRESS</text></g></svg>'''
(root/'project-banner.svg').write_text(banner)
(root/'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#f1eaff"/><g fill="none" stroke-width="4.2" stroke-linecap="round"><path d="M32 13C12 13 8 37 23 45C43 57 58 36 46 24C39 17 31 26 32 37" stroke="#7655ce"/><path d="M32 51C52 51 56 27 41 19C21 7 6 28 18 40C25 47 33 38 32 27" stroke="#a999e7"/></g></svg>''')
print('Artwork and banner generated.')
