# DESIGN.md — fundament

Instrucciones para agentes que crean artifacts HTML (páginas, informes, landings, dashboards, fichas) con la identidad visual de **fundament** (fundament.es).

Fuentes: *Fundament Identity Guidelines v1.0* (`Brandbook/fundament-brandbook.pdf`), hoja de pesos tipográficos `Brandbook/Design.pdf` (oct. 2026), SVG oficiales de `Design elements/Logo` y `Design elements/Symbol`, y la hoja de estilos en producción de formacion.fundament.es (`Business-Design-Regenerativo.html`). Donde estas fuentes discrepan, manda el brandbook (ver §11).

---

## 1. Principios

La identidad de fundament es deliberadamente un **"un-design"**: reduccionista, sin ruido visual, centrada en el contenido (propuestas de proyecto, documentación de proyectos realizados, contenido editorial y promocional). Debe ser fácil de aplicar por no-diseñadores.

Al diseñar, aplica estas reglas en este orden:

1. **El contenido manda.** Si un elemento no ayuda a leer o entender, sobra.
2. **Negro sobre blanco.** El texto es negro, el fondo es blanco. El color es secundario y se reserva para contenido editorial y visualización de datos.
3. **Pocos elementos, reglas fijas.** Una sola familia tipográfica, cuatro colores confirmados, filetes de 1–2 px, sin sombras, sin degradados, sin esquinas redondeadas.
4. **Espacio generoso.** El blanco es parte del diseño: márgenes amplios y una columna de lectura estrecha.
5. **Calidez humana, no frialdad corporativa.** Los secundarios (salmón y bisque) aportan el carácter cálido y empático; úsalos con intención, no como decoración.

---

## 2. Logotipo

El logotipo es la palabra **fundament** en minúsculas, dibujada en Helvetica. Expresa un enfoque "con los pies en la tierra" del diseño centrado en las personas.

**Reglas (brandbook):**

- Siempre en **negro** (`#000000`).
- Siempre a partir del **archivo original** (SVG de abajo). **Nunca** recrearlo escribiendo "fundament" con una fuente.
- No crear variantes, versiones con otros colores, contornos, sombras ni deformaciones.
- Respetar la zona de exclusión. El brandbook la define gráficamente, pero el texto extraído no da la medida. **Provisional:** deja como mínimo un espacio libre igual a la altura de la "f" (≈ la altura total del logo) por cada lado hasta confirmarlo con la página del brandbook.
- Tamaño mínimo recomendado en pantalla: 96 px de ancho.

**SVG oficial** (proporción 457 × 76; escalar solo con `width` o `height`, nunca ambos de forma desproporcionada):

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 457 76" role="img" aria-label="fundament"><g fill="#000" transform="translate(0,-1)"><path transform="translate(0,0.7344)" d="M11.9791,3.3349 C9.5041,5.5129 8.2171,8.9779 8.2171,13.9279 L8.2171,21.2539 L0.0001,21.2539 L0.0001,28.4809 L8.2171,28.4809 L8.2171,74.4159 L17.4241,74.4159 L17.4241,28.4809 L28.3141,28.4809 L28.3141,21.2539 L17.4241,21.2539 L17.4241,14.3229 C17.4241,8.8789 19.7011,7.4929 28.4131,8.0869 L28.4131,0.4639 C26.7301,0.3639 25.0471,0.2659 23.6611,0.2659 C18.5131,0.2659 14.5531,1.1569 11.9791,3.3349"/><path d="M68.774,54.3603 C68.774,62.5773 63.527,68.8143 55.409,68.8143 C48.083,68.8143 43.826,64.8543 43.826,58.1223 L43.826,21.9883 L34.619,21.9883 L34.619,58.6173 C34.619,69.7053 41.648,76.3393 52.637,76.3393 C60.26,76.3393 64.913,72.9723 68.675,67.7253 L68.873,67.7253 L68.873,75.1503 L77.981,75.1503 L77.981,21.9883 L68.774,21.9883 L68.774,54.3603 Z"/><path d="M110.9844,20.7011 C103.2624,20.7011 98.0154,24.1661 94.1544,29.5121 L93.8574,29.5121 L93.8574,21.9881 L84.7494,21.9881 L84.7494,75.1501 L93.9564,75.1501 L93.9564,42.7771 C93.9564,34.2641 99.8964,28.4231 108.1134,28.4231 C115.3404,28.4231 119.7954,32.2841 119.7954,39.1141 L119.7954,75.1501 L128.9034,75.1501 L128.9034,38.0251 C128.9034,26.9371 122.0724,20.7011 110.9844,20.7011"/><path d="M159.2593,69.1113 C149.4583,69.1113 144.5083,60.4993 144.5083,48.8163 C144.5083,37.1343 149.4583,28.4233 159.2593,28.4233 C169.9503,28.4233 175.5933,36.8383 175.5933,48.8163 C175.5933,60.4993 170.6443,69.1113 159.2593,69.1113 L159.2593,69.1113 Z M175.0993,20.3043 C175.0993,23.8693 175.1973,27.7293 175.3963,30.1053 L175.1973,30.1053 C171.8313,24.4633 165.8923,20.7013 158.3673,20.7013 C145.2003,20.7013 135.1033,31.1943 135.1033,48.7173 C135.1033,65.8443 144.2113,76.7343 158.5663,76.7343 C165.9903,76.7343 171.6343,73.2693 174.9993,67.5273 L175.1973,67.5273 L175.1973,75.1503 L184.3063,75.1503 L184.3063,1.4953 L175.0993,1.4953 L175.0993,20.3043 Z"/><path d="M226.3477,55.5488 C226.3477,61.6868 221.3987,69.5078 210.8057,69.5078 C205.4597,69.5078 200.2137,67.8238 200.2137,60.9928 C200.2137,53.6678 205.9547,52.0838 214.6657,50.5988 C219.0227,49.8068 223.6747,48.5198 226.3477,46.8368 L226.3477,55.5488 Z M234.7627,62.8738 L234.7627,38.0258 C234.7627,30.8978 232.0897,26.2448 227.6347,23.5718 C224.2697,21.5918 219.8147,20.7008 214.7657,20.7008 C200.4107,20.7008 193.5797,28.7198 193.1837,37.7288 L202.0947,37.7288 C202.3907,31.3928 206.4497,27.4328 214.8647,27.4328 C222.1907,27.4328 226.2487,30.9968 226.2487,36.7388 C226.2487,42.1838 221.2007,43.4708 213.3787,44.3608 C199.6187,46.0448 190.5117,48.7178 190.5117,61.0928 C190.5117,71.2888 198.4307,76.2388 208.5287,76.2388 C217.5367,76.2388 222.9827,71.9828 226.3477,67.3288 L226.4477,67.3288 C227.4377,72.9728 230.2087,75.6458 235.8517,75.6458 C238.0307,75.6458 239.5147,75.2488 240.8017,74.8538 L240.8017,68.4188 L240.4067,68.4188 C235.7527,69.4078 234.7627,67.1318 234.7627,62.8738 L234.7627,62.8738 Z"/><path d="M301.6172,20.7011 C295.1822,20.7011 288.9452,23.9681 285.1832,30.6001 L284.9852,30.6001 C282.8072,24.0671 277.6602,20.7011 271.2242,20.7011 C264.3932,20.7011 258.7512,24.1661 255.4842,29.9081 L255.1862,29.9081 L255.1862,21.9881 L246.0792,21.9881 L246.0792,75.1501 L255.2862,75.1501 L255.2862,42.3821 C255.2862,34.2641 262.1172,28.4231 268.4532,28.4231 C273.8972,28.4231 277.5602,32.2841 277.5602,38.8171 L277.5602,75.1501 L286.6692,75.1501 L286.6692,42.3821 C286.6692,34.2641 292.5102,28.4231 299.2412,28.4231 C304.5882,28.4231 308.8452,32.2841 308.8452,38.8171 L308.8452,75.1501 L318.0522,75.1501 L318.0522,38.0251 C318.0522,26.9371 311.3192,20.7011 301.6172,20.7011"/><path d="M333.5538,44.164 C334.7408,34.759 339.7898,27.829 349.3938,27.829 C358.5998,27.829 363.8468,33.967 364.3418,44.164 L333.5538,44.164 Z M367.6088,28.918 C363.4508,23.769 357.3138,20.701 349.3938,20.701 C334.1478,20.701 323.9498,33.175 323.9498,48.618 C323.9498,64.161 333.5538,76.636 349.8878,76.636 C362.1638,76.636 370.6778,69.903 373.0538,60.004 L364.0448,60.004 C362.3628,65.646 357.3138,69.111 349.9878,69.111 C339.6918,69.111 334.0478,61.191 333.3558,50.797 L374.1428,50.797 C374.1428,41.788 371.9648,34.165 367.6088,28.918 L367.6088,28.918 Z"/><path d="M406.1426,20.7011 C398.4206,20.7011 393.1736,24.1661 389.3136,29.5121 L389.0166,29.5121 L389.0166,21.9881 L379.9086,21.9881 L379.9086,75.1501 L389.1156,75.1501 L389.1156,42.7771 C389.1156,34.2641 395.0546,28.4231 403.2726,28.4231 C410.4986,28.4231 414.9546,32.2841 414.9546,39.1141 L414.9546,75.1501 L424.0616,75.1501 L424.0616,38.0251 C424.0616,26.9371 417.2306,20.7011 406.1426,20.7011"/><path transform="translate(428,4.7344)" d="M28.8262,24.3818 L28.8262,17.2538 L17.8382,17.2538 L17.8382,0.5228 L8.7292,0.5228 L8.7292,17.2538 L0.4142,17.2538 L0.4142,24.3818 L8.7292,24.3818 L8.7292,60.0218 C8.7292,67.8418 13.6802,70.7128 20.8072,70.8118 C23.1832,70.8118 25.7582,70.5148 28.2322,69.9208 L28.2322,62.1988 L27.9352,62.1988 C26.9452,62.4958 24.8662,62.8918 23.2822,62.8918 C19.9172,62.8918 17.8382,61.8028 17.8382,57.9428 L17.8382,24.3818 L28.8262,24.3818 Z"/></g></svg>
```

Uso típico en cabecera: `<a href="https://fundament.es" class="brand" aria-label="fundament">[SVG]</a>` con `.brand svg{height:22px;width:auto;display:block}`.

---

## 3. Símbolo (mark)

Una forma continua que une una "u" y una "n" con una curva: representa **unión, movimiento y colaboración**, el propósito estratégico de fundament.

**Reglas:**

- Siempre en **negro**.
- Es un elemento icónico de marca: puede aparecer solo (favicon, avatar, sello en portadas, cierre de documento, marca de agua grande y recortada en una sección destacada).
- No sustituye al logotipo cuando la marca tiene que identificarse por su nombre (cabecera, pie, portada principal).
- Nunca rotarlo, colorearlo, rellenarlo con imagen ni combinarlo con otras formas dentro del mismo dibujo.

**SVG oficial** (proporción 245 × 173):

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 245 173" role="img" aria-label="fundament símbolo"><path fill="#000" d="M244.6694,55.2463 C244.6674,55.1893 244.6654,55.1223 244.6634,55.0683 C243.3344,18.3563 223.5004,0.0003 185.1624,0.0003 C141.8324,0.0003 130.4134,36.7693 120.4524,74.1273 C109.5234,115.7673 109.4334,148.0813 61.4544,148.0813 C44.6764,148.0813 34.6064,137.7623 31.2284,117.1463 C30.3764,111.9493 29.9424,106.1093 29.9424,99.6013 L29.9424,6.2173 L0.0464,6.2173 C-0.0676,75.4363 0.0274,108.4533 0.3344,117.1463 C0.3364,117.1803 0.3374,117.2213 0.3384,117.2543 C1.6674,153.9663 21.5014,172.3223 59.8394,172.3223 C103.1694,172.3223 113.4264,138.2183 123.3884,100.8603 C134.3164,59.2213 135.5684,24.2403 183.5474,24.2403 C200.3444,24.2403 210.4194,34.5833 213.7854,55.2463 C214.6294,60.4263 215.0594,66.2433 215.0594,72.7203 L215.0594,166.1043 L244.9554,166.1043 C245.0694,97.0623 244.9744,64.0413 244.6694,55.2463"/></svg>
```

---

## 4. Tipografía

**Familia de marca: Helvetica**, elegida por su herencia democrática, neutral y minimalista.

Pila tipográfica para HTML (una sola familia para todo):

```css
--font: "Helvetica Neue", Helvetica, Arial, sans-serif;
```

Alternativa web con fuente cargada: **Open Sans** (Google Fonts), según `Design.pdf`. Úsala solo cuando haga falta un resultado idéntico en todas las plataformas; nunca mezcles Open Sans con Helvetica en la misma página.

```html
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

### Pesos y su uso

| Peso | Uso | Regla |
|---|---|---|
| Light 300 | Titulares de display muy grandes (portadas, cifras clave) | Opcional, solo en tamaños ≥ 48 px |
| **Regular 400** | **Titulares (h1, h2) y texto corrido**; itálica para énfasis | Es el peso por defecto de la marca. Los titulares grandes van en Regular, no en negrita |
| Medium 500 / SemiBold 600 | **Solo etiquetas pequeñas en MAYÚSCULAS** (eyebrows, categorías, leyendas de gráficos, rótulos de ficha) | Medium en Helvetica; SemiBold 600 si se usa Open Sans |
| **Bold 700** | **Títulos de párrafo** (h3, h4, preguntas de FAQ, títulos de tarjeta) | Nunca en titulares grandes |
| ExtraBold 800 | Énfasis puntual | Solo Open Sans; muy poco |

**Prohibido:** escribir titulares, títulos de párrafo o texto corrido en MAYÚSCULAS. Las mayúsculas quedan reservadas a las etiquetas pequeñas.

### Escala

| Rol | Tamaño | Peso | Interlineado | Otros |
|---|---|---|---|---|
| Display | `clamp(2.5rem, 6vw, 4.5rem)` | 300 o 400 | 1.05 | `letter-spacing:-0.02em` |
| h1 | `clamp(2rem, 4.4vw, 3rem)` | 400 | 1.12 | máx. 18ch, `letter-spacing:-0.01em` |
| h2 | `clamp(1.5rem, 2.6vw, 2.1rem)` | 400 | 1.2 | `letter-spacing:-0.01em` |
| h3 / título de párrafo | `1.05–1.1rem` | 700 | 1.35 | |
| Entradilla (lede) | `1.15–1.2rem` | 400 | 1.6 | máx. 56–66ch |
| Cuerpo | `1rem–1.05rem` (16–17 px) | 400 | 1.6–1.7 | máx. 66ch |
| Pequeño / meta | `.86–.9rem` | 400 | 1.5 | color `--muted` |
| Etiqueta | `.72–.78rem` | 500/600 | 1.3 | **MAYÚSCULAS**, `letter-spacing:.06em` |

---

## 5. Color

### Paleta confirmada

| Token | Nombre | HEX | RGB | Uso |
|---|---|---|---|---|
| `--black` | Black | `#000000` | 0 0 0 | Todo el texto, logo, símbolo, filetes fuertes, botón principal |
| `--white` | White | `#FFFFFF` | 255 255 255 | Fondo de página |
| `--salmon` | Dark Salmon | `#E6A198` | 230 161 152 | Secundario: datos, acentos editoriales, formas |
| `--bisque` | Bisque | `#FFE1C2` | 255 225 194 | Secundario: fondos de bloques destacados, datos, formas |

### Pendientes de confirmar

El brandbook incluye además **Light Blue** y **Thistle**, pero sus valores no se pudieron extraer del PDF (salen corruptos en el texto). **No los uses** hasta confirmar sus HEX en `Design elements/Color` (fundament-color.ai o .afdesign). No los sustituyas por los colores CSS homónimos (`lightblue`, `thistle`): los valores de marca de los otros dos secundarios ya difieren de los CSS estándar.

### Neutros derivados (para la interfaz)

El brandbook no define grises. Para filetes y texto secundario usa estos derivados del negro, y nada más:

| Token | Valor | Uso |
|---|---|---|
| `--muted` | `#5C5C5C` | Texto secundario, meta, etiquetas (contraste 6.7:1 sobre blanco) |
| `--rule` | `#E3E3E3` | Filetes finos, bordes de tarjeta y tabla |

### Reglas de uso

- **Texto negro, fondo blanco** (regla del brandbook). Es la combinación por defecto en el 90 % de la superficie.
- Los secundarios se usan en **contenido editorial y visualización de datos**: barras, series, bloques destacados, formas decorativas, fondos de una sección concreta.
- **Nunca texto en salmón sobre blanco** (contraste 2.1:1, ilegible). El salmón va como relleno, con texto negro encima (10:1).
- El bisque funciona como fondo de bloque con texto negro (17:1).
- Nada de degradados, transparencias decorativas ni colores fuera de la paleta.
- Modo de color: los artifacts de fundament son **solo modo claro** (`color-scheme: light`). El logo y el símbolo siempre son negros, así que no se invierten para modo oscuro. Esta regla de marca prevalece sobre cualquier pauta genérica que pida modo oscuro.

### Visualización de datos

- Orden de series: negro → salmón → bisque (y Light Blue / Thistle cuando estén confirmados).
- Leyendas y categorías en etiqueta (MAYÚSCULAS, peso 500/600), p. ej. `COMERCIO`, `TURISTA RESIDENTE`, `CULTURA Y SOCIEDAD`.
- Ejes y rejilla finos en `--rule`; números del eje en `--muted`, tamaño pequeño.
- El bisque es muy claro: si es una serie de barras, dale un borde de 1 px negro o úsalo solo junto a series más oscuras.
- Sin efectos 3D, sombras, degradados ni gráficos de tarta decorativos.

---

## 6. Espacio y retícula

El espacio en blanco es el recurso principal de la marca. Ante la duda, más aire.

### Escala de espaciado (base 4 px)

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 80 · 120`

### Medidas

| Elemento | Valor |
|---|---|
| Contenedor máximo | `1120px` |
| Columna de lectura (prosa) | `720px` (≈ 66ch) |
| Margen lateral | `24px` (escritorio y móvil, mínimo 16 px) |
| Padding vertical de sección | `64px` (80 px en la última sección / CTA) |
| Separación título de sección → contenido | `36px` |
| Separación entre párrafos | `18px` |
| Hueco entre tarjetas de rejilla | `18–24px` |
| Padding interno de tarjeta | `20px 22px` |
| Panel destacado | `36px 40px` |

### Ritmo y estructura

- Una columna de lectura estrecha alineada a la izquierda, dentro de un contenedor más ancho. El texto **no se centra** salvo en portadas puntuales.
- Rejillas de 2 columnas para tarjetas (1 en < 700 px), 3 como máximo.
- Filas de "etiqueta | valor" con la etiqueta en una columna fija de 120–200 px.
- Las secciones se separan con espacio y, entre secciones principales, con un **filete negro de 2 px** a todo el ancho del contenedor.
- Dentro de una sección, separadores de **1 px en `--rule`**.
- Diseño responsive: todo debe funcionar a 360 px de ancho sin scroll horizontal.

---

## 7. Formas

Inspiradas en los elementos básicos del mind-mapping y del diseño de flujos de interacción, las formas abstractas componen una letra **F** siempre cambiante (o un alfabeto, o números) o actúan como patrones decorativos. Reflejan curiosidad, diversidad y convivencia de elementos distintos.

- Construye las formas solo con **primitivas geométricas simples**: círculos, semicírculos, cuartos de círculo, rectángulos y líneas de conexión. Deben poder hacerse en Keynote o PowerPoint, así que nada de trazos complejos.
- Relleno plano en negro, salmón o bisque (sin contornos decorativos, sin degradados).
- Usos: portadas, cabeceras de sección editorial, piezas de sensibilización y elementos gráficos dentro de visualizaciones de datos.
- Una composición de formas por pantalla o sección; nunca como fondo repetido en toda la página ni detrás de texto corrido.
- Referencia visual oficial: `Design elements/Shapes/shapes.png`. Ante la duda, un círculo y un rectángulo bien colocados bastan.

---

## 8. Componentes

| Componente | Especificación |
|---|---|
| **Cabecera** | Fondo blanco, `position:sticky`, filete inferior 1 px `--rule`, padding `18px 24px`. Logo SVG a la izquierda (22 px de alto), navegación a la derecha en cuerpo `.92rem`, regular, sin subrayado; hover con `opacity:.6`. En < 820 px, menú desplegable |
| **Eyebrow / etiqueta** | Texto en MAYÚSCULAS, `.75rem`, 500/600, `letter-spacing:.06em`, `--muted` |
| **Botón principal** | Fondo negro, texto blanco, 600, `padding:15px 30px`, sin radio, sin sombra. Hover: fondo salmón y texto negro |
| **Botón secundario** | Fondo transparente, borde 1.5 px negro, texto negro. Hover: fondo bisque |
| **Enlaces** | Negro, subrayados en texto corrido (`text-underline-offset:3px`); en navegación sin subrayado |
| **Tarjeta** | Fondo blanco, borde 1 px `--rule`, sin radio, sin sombra, padding `20px 22px`. Número o etiqueta arriba, título en 700, texto en 400 |
| **Panel destacado** | Fondo blanco o bisque, `border-left:5px solid #000`, padding `36px 40px`, ancho de prosa |
| **Listas** | Viñeta personalizada `→` en negro (destacadas) o `·` en `--muted` (secundarias), sangría de 18–28 px |
| **Ficha / tabla** | Filas con filete inferior 1 px `--rule`; etiquetas en `--muted`; sin fondos alternos de cebra; cabecera de tabla en etiqueta MAYÚSCULAS |
| **FAQ** | `<details>` con filete superior 1 px, pregunta en 700, signo `+` / `–` en `--muted` a la derecha |
| **Cifra clave** | Número grande en display Light/Regular, etiqueta en MAYÚSCULAS debajo; opcionalmente sobre un bloque bisque |
| **Imágenes** | Recorte rectangular (16:9, 16:6 o 4:3), borde 1 px `--rule`, sin radio. Excepción: avatares de personas en círculo |
| **Pie** | Filete superior 1 px, texto `.86rem` en `--muted`, símbolo o logo pequeño, enlaces sin subrayado |
| **Foco** | `outline:2px solid #000; outline-offset:3px` |
| **Movimiento** | Solo transiciones de 150 ms en opacidad o color. Respetar `prefers-reduced-motion` |

---

## 9. Plantilla CSS base

Copia este bloque como punto de partida de todo artifact de fundament:

```css
:root{
  color-scheme: light;
  --black:#000000; --white:#FFFFFF;
  --salmon:#E6A198; --bisque:#FFE1C2;
  --muted:#5C5C5C; --rule:#E3E3E3;
  --font:"Helvetica Neue", Helvetica, Arial, sans-serif;
  --container:1120px; --prose:720px; --gutter:24px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--white);color:var(--black);font-family:var(--font);
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2{font-weight:400;letter-spacing:-0.01em;margin:0}
h1{font-size:clamp(2rem,4.4vw,3rem);line-height:1.12;max-width:18ch}
h2{font-size:clamp(1.5rem,2.6vw,2.1rem);line-height:1.2}
h3,h4{font-weight:700;font-size:1.05rem;line-height:1.35;margin:0}
p{margin:0;max-width:66ch}
a{color:inherit;text-underline-offset:3px}
img{max-width:100%;display:block}
::selection{background:var(--salmon);color:var(--black)}
:focus-visible{outline:2px solid var(--black);outline-offset:3px}
.wrap{max-width:var(--container);margin:0 auto;padding:0 var(--gutter)}
.prose{max-width:var(--prose);display:flex;flex-direction:column;gap:18px;font-size:1.05rem;line-height:1.7}
.label{font-size:.75rem;font-weight:500;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.section{padding:64px 0}
.section + .section{border-top:2px solid var(--black)}
.card{background:var(--white);border:1px solid var(--rule);padding:20px 22px;display:flex;flex-direction:column;gap:8px}
.panel{border-left:5px solid var(--black);padding:36px 40px;max-width:var(--prose)}
.panel--warm{background:var(--bisque)}
.btn{display:inline-block;padding:15px 30px;font:600 1rem/1 var(--font);text-decoration:none;
  background:var(--black);color:var(--white);border:1.5px solid var(--black);cursor:pointer;
  transition:background .15s ease,color .15s ease}
.btn:hover{background:var(--salmon);color:var(--black);border-color:var(--salmon)}
.btn--ghost{background:transparent;color:var(--black)}
.btn--ghost:hover{background:var(--bisque);border-color:var(--black)}
@media (prefers-reduced-motion:reduce){*{transition-duration:.01ms!important;scroll-behavior:auto!important}}
```

---

## 10. Checklist antes de publicar

- [ ] El logo es el **SVG oficial**, en negro, con su zona de exclusión. No hay "fundament" escrito con fuente haciendo de logo.
- [ ] Una sola familia tipográfica en toda la página.
- [ ] Titulares en Regular 400; títulos de párrafo en Bold 700; etiquetas pequeñas en MAYÚSCULAS con Medium/SemiBold. Ningún titular ni párrafo en mayúsculas.
- [ ] Texto negro sobre blanco en la mayor parte de la superficie; salmón y bisque solo en datos, bloques editoriales y formas.
- [ ] Ningún texto en salmón; ningún color fuera de la paleta; Light Blue y Thistle no usados hasta confirmarlos.
- [ ] Sin sombras, degradados ni esquinas redondeadas (salvo avatares).
- [ ] Contenedor 1120 px, prosa ≤ 720 px, márgenes laterales de 24 px, secciones con 64 px de aire.
- [ ] Funciona a 360 px de ancho sin scroll horizontal.
- [ ] Contraste AA en todo el texto y foco visible.

## 11. Lo que no hay que hacer

- Recrear, redibujar o colorear el logotipo o el símbolo.
- Usar el estilo "startup" genérico: tarjetas con sombra, esquinas redondeadas, degradados, iconos decorativos de librería, emojis.
- Añadir colores de acento propios (azules corporativos, verdes de éxito, naranjas vivos).
- Llenar el espacio: banners, fondos texturizados, formas repetidas como papel pintado.
- Escribir titulares en mayúsculas o en negrita.

---

## 12. Notas y discrepancias

- **Web de formación en producción.** La hoja de estilos de formacion.fundament.es usa una paleta distinta a la del brandbook: tinta azul petróleo `#102b33`, papel crema `#faf8f3`, acento coral `#e8602f` y gris `#5a757c`. También compone el nombre de marca en la cabecera con texto en negrita en lugar del SVG del logotipo, cosa que el brandbook prohíbe. Este DESIGN.md sigue el **brandbook**; si fundament decide adoptar la paleta web como evolución oficial, hay que actualizar §5 y §9.
- **Retícula y medidas.** El brandbook no define medidas de espaciado. Las de §6 proceden de la web en producción, que ya aplica la filosofía reduccionista de la marca (filetes, sin sombras, columna estrecha).
- **Zona de exclusión** del logo: provisional (ver §2).
- **Light Blue y Thistle:** valores pendientes (ver §5).
