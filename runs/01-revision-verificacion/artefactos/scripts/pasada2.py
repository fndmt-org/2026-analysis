"""Pasada 2 de «Cifras 2026 contrastadas»: reimplementación sin pandas + comprobaciones de redondeo, bases y marcas.
Uso: python -I pasada2.py <raíz del repo>
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path
R=Path(sys.argv[1])
V=json.loads(re.search(r"const V = (\{.*?\});\n",(R/"referencia/Verificación datos 2026.html").read_text()).group(1))
rows=list(csv.DictReader(open(R/"datos/modelos/fundament_2026.csv")))
comp={r["id_respuesta"]:r for r in csv.DictReader(open(R/"datos/modelos/companero_2026_filas.csv"))}
num=lambda x: None if x in ("",None) else float(x)
su=[r for r in rows if comp[r["id_respuesta"]]["en_muestra"]=="True"]
aus=[r for r in rows if comp[r["id_respuesta"]]["en_hoja_limpia"]=="False"]
print("su",len(su),"ausentes",len(aus),"comp en_muestra total",sum(c["en_muestra"]=="True" for c in comp.values()),
      "en hoja no en muestra",sum(c["en_hoja_limpia"]=="True" and c["en_muestra"]=="False" for c in comp.values()))
# 1 likert: recuentos independientes y comprobación de redondeos del doc sobre su propia base
err=[]
for it in V["likert"]:
    vals=[num(r[it["k"]]) for r in su]; vals=[v for v in vals if v is not None and v not in (98,99)]
    c=(sum(v<=4 for v in vals),sum(v==5 for v in vals),sum(v>=6 for v in vals))
    if (it["neg"]-c[0],it["neu"]-c[1],it["pos"]-c[2]) not in [(1,0,0),(0,1,0),(0,0,1)]: err.append(("likert",it["k"],c))
    for a,b in [("neg","negp"),("neu","neup"),("pos","posp")]:
        if round(100*it[a]/it["n"],1)!=it[b]: err.append(("redondeo",it["k"],b,it[b],round(100*it[a]/it["n"],2)))
    if it["neg"]+it["neu"]+it["pos"]!=it["n"]: err.append(("suma",it["k"]))
    print(it["k"], "0s su:",sum(v==0 for v in vals), "10s:",sum(v==10 for v in vals), "%5:",round(100*c[1]/len(vals),1))
# demo pct sobre su base 405
for grp in ("demo","socio","otras"):
    for k,lst in V[grp].items():
        if not isinstance(lst,list): continue
        base=sum(e["n"] for e in lst)
        for e in lst:
            if round(100*e["n"]/base,1)!=e["pct"]: err.append(("pct",k,e["label"],e["pct"],round(100*e["n"]/base,2)))
# sit eco media doc sobre su distribución
d=V["socio"]["situacion_economica"]["dist"]; m=sum(int(e["label"])*e["n"] for e in d)/sum(e["n"] for e in d)
print("media sit eco desde su distribución",round(m,3), "n",sum(e["n"] for e in d))
for e in d:
    if round(100*e["n"]/405,1)!=e["pct"]: err.append(("pct sit",e))
# tenencia: % redondeados del doc
for k,r in V["seg"]["tenencia"].items():
    if r["No"]+r["pasada"]+r["seria"]!=r["n"]: err.append(("ten suma",k))
    print("ten",k,"sí total",r["pasada"]+r["seria"],round(100*(r["pasada"]+r["seria"])/r["n"],1),"seria%",round(100*r["seria"]/r["n"],1))
for x in V["seg"]["edadTen"]:
    if round(100*x["si"]/x["n"])!=x["sip"]: err.append(("edadten",x))
# cualit % sobre sust
for q in ("cambio","preservar"):
    Q=V["cualit"][q]; print(q,[ (l,round(100*n/Q["sust"],1)) for l,n in Q["cats"]], "suma%",round(sum(n for _,n in Q["cats"])*100/Q["sust"],1),"sin clasificar%",round(100*Q["unclass"]/Q["sust"],1))
print("ERRORES:",err)
# marcas de calidad en su muestra y en ausentes
print("su: rapido",sum(r["marca_rapido"]=="True" for r in su),"disp",sum(r["marca_dispositivo_repetido"]=="True" for r in su),"alguna",sum(r["sensibilidad"]=="True" for r in su))
print("413: rapido",sum(r["marca_rapido"]=="True" for r in rows),"disp",sum(r["marca_dispositivo_repetido"]=="True" for r in rows))
print("ausentes: rapido",sum(r["marca_rapido"]=="True" for r in aus),"disp",sum(r["marca_dispositivo_repetido"]=="True" for r in aus),
      "ambas",sum(r["marca_rapido"]=="True" and r["marca_dispositivo_repetido"]=="True" for r in aus),
      "viv",Counter(r["vivienda"] for r in aus),"aband",Counter(r["q_abandono"] for r in aus),"mun distintos fuera de su muestra",len({r["municipio"] for r in aus}-{r["municipio"] for r in su}))
# histórico: columna 2026 frente a §2, con bases posibles
mp={"Precios":"q_precios","Medio ambiente":"q_medio_ambiente","Calidad de vida":"q_calidad_vida","Transporte":"q_transporte","Vida diaria":"q_vida_diaria","Gastos de ocio":"q_gastos_ocio","Espacios públicos":"q_espacios","Bienestar":"q_bienestar","Diversificación":"q_diversificacion","Activismo mejoró gestión":"q_activismo","Futuro de la isla":"q_futuro_isla","Interacciones positivas":"q_interacciones","Gestión mejoró convivencia":"q_gestion"}
L={it["k"]:it for it in V["likert"]}
sm=[r for r in rows if r["sensibilidad"]=="False"]
for h in V["hist"]:
    k=mp[h["lab"]]; it=L[k]; neg="rechazo" in h["m"]
    doc2=it["negp"] if neg else it["posp"]
    def p(base):
        vals=[num(r[k]) for r in base]; return round(100*sum((v<=4) if neg else (v>=6) for v in vals)/len(vals),2)
    print(f'hist {h["lab"]:28} col2026 {h["y"]["2026"]:5} §2 {doc2:5} | su {p(su)} 413 {p(rows)} 346 {p(sm)} | 405 doc {round(100*(it["neg"] if neg else it["pos"])/405,2)}')
# q_abandono: base y vacíos
print("q_abandono vacíos su",sum(r["q_abandono"]=="" for r in su))
print("98 en dependencia su",sum(r["tourism_dependencia"] in ("98","98.0") for r in su),"99 nacionalidad su",sum(r["nacionalidad"] in ("99","99.0") for r in su))
