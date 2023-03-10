# MTB_Res_UCaldas
EFICACIA DIAGNÓSTICA in silico DE TÉCNICAS MOLECULARES DE USO CLÍNICO EN Mycobacterium tuberculosis.

El siguiente programa está dividido en varias secciones:
1. Preprocesamiento de datos.
2. Análisis inicial.
3. Análisis de resistencia antibiótica.
4. Análisis MTBGT.

---

## Preprocesamiento de datos
### Entrada del programa
*Directorio (ruta de acceso) donde se encuentran todas las muestras a analizar, clasificadas por país de origen.
*Archivo en formato .xlsx (ruta de acceso) donde se encuentra información (estructurada de una manera establecida) que relaciona TGN, TACH y Genes con la resistencia hacia un antibiótico dado.
*Archivo en formato .txt donde se lista la relación entre codón y una posición del genoma

### Preprocesamiento
a) Se realiza un filtrado de muestras, clasificadas por país de origen, eligiendo aquellas posiciones del genoma que son estadísticamente significativas, es decir, aquellas cuyo valor en la columna "FILTER" sea "PASS", y se almacenan en formato .xlsx, por cada muestra, para una fácil visualización de los registros y posterior acceso a los mismos.
b)
