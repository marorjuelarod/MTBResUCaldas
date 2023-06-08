# MTB_Res_UCaldas
EFICACIA DIAGNÓSTICA in silico DE TÉCNICAS MOLECULARES DE USO CLÍNICO EN Mycobacterium tuberculosis.

El presente programa realiza un análisis de resistencia antibiótica de aislamientos de Micobacterium tuberculosias a partir de resultados de análisis de llamados de variantes y emplea el programa MTBGT propuesto por Kamela y colaboradores disponible en https://github.com/KamelaNg/MTBGT para realizar una aproximación computacional a pruebas moleculares de uso clínico usadas para el diagnóstico de la tuberculosis. 

MTB_Res_UCaldas es generado como parte del proceso de formación en el programa de Maestría en Bioinformática y Bioinformática de la Universidad de Caldas, Colombia y el convenio SUMA Manizales. 

MTB_Res_UCaldas está dividido en varias secciones:

1. Preprocesamiento de datos.
2. Análisis de resistencia antibiótica.
3. Análisis MTBGT (Aproximación computacional a pruebas moleculares de uso clínico usadas para el diagnóstico de la tuberculosis).
4. Reporte de mutaciones de resistencia y sensibilidad antibíotica.

---

### Entrada del programa
*Directorio (ruta de acceso) donde se encuentran todas las muestras a analizar en formato VCF, clasificadas por país de origen o condición de interés.
*Archivo en formato .xlsx (ruta de acceso) donde se encuentra información (estructurada de una manera establecida) que relaciona el gen, la mutación y la caracterización de resistencia según la OMS frente a un antibiótico dado.

### Salida del programa

1. Resultados generales: 
  1.1 medicalSignificanceReport.txt : Reporte de mutaciones de resistencia y su clasifición según el catálogo de mutaciones de la OMS
  1.2 Registro_mutaciones : Listado de mutaciones encontradas para cada uno de los genes evaluados.
  1.3 Registro_sensibilidad : Asignación de fenotipos de resistencia a cada muestra según las mutaciones encontradas.
  1.4 solo_mutaciones : Genotipos de resistencia por muestra
  
2. Directorio de resultados por país o condición de interés: 
  Se regenerará un directorio por interés en el cual se encontrarán los reportes anteriores por condición y los reportes de mutaciones individuales para cada muestra.
  2.1. tabfiles folder: Se generará un directorio con la trasnformación de los archivos VCF a formato .tab, condición necesaria para la ejecución del MTBGT.
  2.2. GenomeInfo_HainLPA : Reporte de resistencia según la prueba molecular GenoType MDRTB plus II empleando el  MTBGT.
  2.3. GenomeInfo_NiproLPA : Reporte de resistencia según la prueba molecular Genoscholar NTM+MDRTB II empleando el MTBGT.
  2.4. GenomeInfo_XpertClassic : Reporte de resistencia según la prueba molecular Xpert MTB/RIF Classic empleando el MTBGT.
  2.5. GenomeInfo_XpertUltra : Reporte de resistencia según la prueba molecular Xpert MTB/RIF Ultra empleando el MTBGT.
  2.6. GenomeInfo_summaryTables : Resumen de resultados de pruebas moleculares empleando el MTBGT empleando el MTBGT.
  2.7  Clasificación del aislamiento según las condiciones de resistencia presentadas.
  

3. Directorio de reportes de ejecución del programa




Autores: 

Marcela Orjuela Rodríguez
Sebastian Orozo
