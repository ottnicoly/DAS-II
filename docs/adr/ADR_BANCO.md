\# ADR-001: Escolha da biblioteca Python para conexão com banco SQL Server



\*\*Status:\*\* Proposto  |  \*\*Data:\*\* 2026-05-27  |  \*\*Autores:\*\* Nicoly Ott



\## Contexto



O código Python precisa acessar um banco hospedado no Azure:

Foram realizados testes comparando duas bibliotecas Python para conexão e execução de consultas SELECT:



\- pyodbc

\- pymssql



Nos testes, ambas as bibliotecas conseguiram executar a consulta com sucesso e carregar 205 linhas.



Resultados observados:



\- pyodbc:

&#x20; - Tempo médio aproximado de SELECT: 0,53 segundos

&#x20; - Execução total da função: entre 1113 ms e 1294 ms



\- pymssql:

&#x20; - Tempo médio aproximado de SELECT: 0,34 segundos

&#x20; - Execução total da função: 717 ms



Além do desempenho, também foi considerada a simplicidade de uso no código Python e a compatibilidade com SQL Server.



\## Decisão



A biblioteca escolhida para conexão com o banco SQL Server no código Python será a \*\*pymssql\*\*.



A decisão foi tomada principalmente com base no melhor desempenho observado nos testes executados, onde a pymssql apresentou menor tempo médio de SELECT e menor duração total da função em comparação com a pyodbc.



\## Consequências



(+) Melhor desempenho nas consultas testadas, com tempo médio menor de SELECT.



(+) Menor tempo total de execução da função.



(+) Biblioteca simples de utilizar para conexão direta com SQL Server.



(-) A decisão foi baseada em testes com volume pequeno de dados, apenas 205 linhas.



(-) Pode ser necessário reavaliar a decisão caso o volume de dados aumente ou surjam requisitos específicos de driver, autenticação ou compatibilidade.



\## Alternativas rejeitadas



\- pyodbc: Foi rejeitada porque, nos testes realizados, apresentou tempo médio de SELECT maior que a pymssql.

