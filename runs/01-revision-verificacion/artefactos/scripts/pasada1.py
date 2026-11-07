"""Pasada 1 de «Cifras 2026 contrastadas»: compara cada cifra 2026 del objeto V con el recálculo
(su muestra = 404 comunes; nuestras 413; 346 sin marcas).
Uso: python -I pasada1.py <raíz del repo> > p1.json
"""
import sys, json, re
from pathlib import Path
import pandas as pd
R=Path(sys.argv[1])
t=(R/"referencia/Verificación datos 2026.html").read_text()
V=json.loads(re.search(r"const V = (\{.*?\});\n",t).group(1))
d=pd.read_csv(R/"datos/modelos/fundament_2026.csv").merge(pd.read_csv(R/"datos/modelos/companero_2026_filas.csv"),on="id_respuesta",how="left")
B={"su":d[d.en_muestra],"413":d,"346":d[~d.sensibilidad]}
print("filas:",{k:len(v) for k,v in B.items()}, "en hoja limpia:",int(d.en_hoja_limpia.sum()), file=sys.stderr)
def lik(s):
    s=s.dropna(); s=s[~s.isin([98,99])]; n=len(s)
    neg,neu,pos=int((s<=4).sum()),int((s==5).sum()),int((s>=6).sum())
    return dict(n=n,neg=neg,neu=neu,pos=pos,negp=round(100*neg/n,1),neup=round(100*neu/n,1),posp=round(100*pos/n,1),mean=round(s.mean(),2))
out={"likert":[]}
for it in V["likert"]:
    r={"k":it["k"],"doc":{k:it[k] for k in ["n","neg","neu","pos","negp","neup","posp","mean"]}}
    for b,df in B.items(): r[b]=lik(df[it["k"]])
    r["nr"]=int(d[it["k"]].isin([98,99]).sum()); r["na"]=int(d[it["k"]].isna().sum())
    out["likert"].append(r)
# demografía
maps={"gender":{1:"Mujer",2:"Hombre",3:"Otro"},"age":{1:"Menos de 18 años",2:"18–25 años",3:"26–35 años",4:"36–45 años",5:"46–55 años",6:"56–65 años",7:"66–75 años",8:"Más de 75 años"},
 "nacionalidad":{1:"Española",2:"Europea (no española)",3:"No europea",99:"Prefiero no decirlo"},"lang":{1:"es",2:"ca"},
 "situacion":{1:"Trabajo",2:"Parado/a",3:"Estudiante",4:"Jubilado/a o pensionista"},
 "convivencia":{0:"Vivo solo/a",1:"1 persona más",2:"2 personas más",3:"3 personas más",4:"4 personas más",5:"5 personas o más"},
 "vivienda":{1:"Propiedad",2:"Alquiler",3:"Otro"},"tourism_dependencia":{0:"No",1:"Sí",98:"No lo sé"},
 "manifestacion":{0:"No",1:"Sí"},"responsable":{1:"El gobierno",2:"Los que traen, alojan y dan servicio a los turistas",3:"Los dos anteriores",4:"Otro"},
 "q_abandono":{0:"No",1:"Sí, de pasada",2:"Sí, seriamente"}}
src={**{k:V["demo"][k] for k in ["gender","age","nacionalidad","lang"]},**{k:V["socio"][k] for k in ["situacion","convivencia","vivienda","tourism_dependencia"]},**V["otras"]}
out["demo"]={}
for v,lst in src.items():
    rows=[]
    for e in lst:
        code=[c for c,l in maps[v].items() if l==e["label"]][0]
        row={"label":e["label"],"doc_n":e["n"],"doc_pct":e["pct"]}
        for b,df in B.items():
            n=int((df[v]==code).sum()); row[b]=n
        rows.append(row)
    out["demo"][v]={"rows":rows,"na":{b:int(df[v].isna().sum()) for b,df in B.items()},"doc_suma":sum(e["n"] for e in lst)}
se=V["socio"]["situacion_economica"]
out["sit_eco"]={"doc_mean":se["mean"],"doc":[(e["label"],e["n"]) for e in se["dist"]],
 **{b:{"mean":round(df.situacion_economica.mean(),2),"n":int(df.situacion_economica.notna().sum()),"dist":df.situacion_economica.value_counts().sort_index().astype(int).to_dict()} for b,df in B.items()}}
# segmentación
seg={}
for b,df in B.items():
    ct=pd.crosstab(df.vivienda,df.q_abandono); seg[b]={maps["vivienda"][i]:{maps["q_abandono"][j]:int(ct.loc[i,j]) for j in ct.columns} for i in ct.index}
out["seg_ten"]={"doc":V["seg"]["tenencia"],**seg}
e3={2:"18–35",3:"18–35",4:"36–55",5:"36–55",6:"56+",7:"56+",8:"56+"}
et={}
for b,df in B.items():
    x=df[df.q_abandono.notna()].assign(e=df.age.map(e3),si=lambda z:z.q_abandono>=1)
    g=x.groupby(["e","vivienda"]).agg(n=("si","size"),si=("si","sum"))
    et[b]=[{"edad":i[0],"ten":maps["vivienda"][i[1]],"n":int(r.n),"si":int(r.si),"sip":round(100*r.si/r.n)} for i,r in g.iterrows()]
out["edad_ten"]={"doc":V["seg"]["edadTen"],**et}
# territorio (no publicar cruces por municipio con n < 5)
terr=[]
tot_doc=sum(m["resp"] for m in V["terr"]["items"])
for m in V["terr"]["items"]:
    r={"name":m["name"],"doc":m["resp"],**{b:int((df.municipio==m["name"]).sum()) for b,df in B.items()}}
    rp=100*m["resp"]/tot_doc; pp=100*m["pop"]/V["terr"]["totalpop"]
    r["idx_recalc"]=round(rp/pp*100); r["idx_doc"]=m["idx"]; r["resppct_ok"]=round(rp,2)==m["resppct"]; r["poppct_ok"]=round(pp,2)==m["poppct"]
    terr.append(r)
out["terr"]=terr
out["terr_extra"]={b:sorted(set(df.municipio.dropna())-{m["name"] for m in V["terr"]["items"]}) for b,df in B.items()}
out["terr_nmun"]={b:int(df.municipio.nunique()) for b,df in B.items()}
out["suma_pop"]=sum(m["pop"] for m in V["terr"]["items"])
# cualitativo: solo recuentos de respuestas no vacías
out["cualit"]={b:{c:int(df[c].fillna("").astype(str).str.strip().ne("").sum()) for c in ["cambio","preservar"]} for b,df in B.items()}
for c in ["cambio","preservar"]:
    q=V["cualit"][c]; ml=q["multilabel"]
    out["cualit"]["doc_"+c]={"resp":q["resp"],"sust":q["sust"],"unclass":q["unclass"],"suma_ml":sum(v for k,v in ml.items()),
      "asignaciones":sum(int(k)*v for k,v in ml.items() if k[0]!="0"),"suma_cats":sum(x[1] for x in q["cats"]),"clasif_pct":q["clasif_pct"],
      "clasif_recalc":round(100*(q["sust"]-q["unclass"])/q["sust"],1)}
json.dump(out,sys.stdout,ensure_ascii=False,indent=1,default=int)
