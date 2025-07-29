# Aplicație de raportare folosind Python

Aplicația are ca scop generarea de grafice utilizând informații preluate dintr-o bază de date PostgreSQL, care conține date structurate pe baza ticketelor din Jira (Atlassian).

### Componentele aplicației
Aplicatia include următoarele elemente principale de interfață:

* 9 grafice de tip donut (Donut Charts) – Reprezintă vizual datele sub formă de diagrame circulare pentru o analiză rapidă și intuitivă.
* Un tabel 
* 3 meniuri dropdown – Permit utilizatorilor să filtreze și să exploreze datele din mai multe perspective.

### Funcționalități principale
* Extracția și prelucrarea datelor din baza PostgreSQL cu structura specifică ticketelor Jira.
* Generarea de grafice diverse, inclusiv pie chart-uri și tabele cu date sumarizate.
<img width="1868" height="912" alt="Image" src="https://github.com/user-attachments/assets/efe118ae-6d24-4e4b-8bc8-24cfe92dcccd" />

* Interfață interactivă care permite utilizatorului să selecteze diferite opțiuni prin dropdown-uri pentru a schimba dinamica graficelor.
* Utilizarea callback-urilor pentru actualizarea instantanee a vizualizărilor în funcție de selecțiile făcute.

   <img width="1832" height="603" alt="Image" src="https://github.com/user-attachments/assets/fed090a8-3eb8-48ec-b096-ccc7ba4c3cb5" />
  <img width="1858" height="628" alt="Image" src="https://github.com/user-attachments/assets/177e5e26-e73e-4b21-8c71-af641fd178eb" />
### Tehnologii folosite
* Dash (Python): Frameworkul principal utilizat pentru crearea interfeței, vizualizarea datelor si dezvoltarea unor clase personalizate pentru afișarea tabelelor, generarea graficelor de tip pie chart.
* Flask: Server web utilizat pentru a găzdui aplicația Dash.
* Docker: Folosit pentru containerizarea aplicației, facilitând astfel implementarea și rularea într-un mediu izolat.



