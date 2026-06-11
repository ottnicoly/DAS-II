# DAS-II — Plataforma de Inteligência Operacional · VendaMais

> Solução de analytics para a VendaMais Distribuidora Ltda., eliminando a dependência de relatórios manuais e proporcionando visibilidade operacional com defasagem máxima de 24 horas.

---

## 📌 Descrição do Projeto

A **VendaMais Distribuidora Ltda.** é uma empresa de médio porte com operações em quatro estados, 18 representantes comerciais e cerca de 3.500 pedidos/mês. O principal problema enfrentado era a ausência de visibilidade consolidada sobre indicadores operacionais:

- Relatórios levavam até **2 dias úteis** para serem compilados manualmente;
- A inadimplência era calculada em planilhas desatualizadas;
- A diretoria tomava decisões com dados de até **30 dias de defasagem**.

Este projeto propõe uma **Plataforma de Inteligência Operacional** baseada em Azure, seguindo o pipeline:

```
ERP VendaMais → Ingestão (Azure Functions) → Blob Storage → Transformação (Azure Functions) → Azure SQL Database → Power BI Service
```

A solução entrega dashboards atualizados diariamente para as áreas Comercial, Financeiro, Estoque, Logística e TI.

---

## 👥 Integrantes

| Nome | GitHub |
|---|---|
| Nicoly Cristina Ott | [@ottnicoly](https://github.com/ottnicoly) |
| Matheus Campos | [@matheus](https://github.com/MatheusCampos98) |
| Gabiel Venerusso | [@gabrielvenerusso](https://github.com/gabrielvenerusso) |
| Larissa Bertling | [@larissa](https://github.com/larissabertling) |

---

## 🗂️ Estrutura do Repositório

```
DAS-II/
├── README.md                        ← Você está aqui
└── docs/
    ├── adr/
    │   ├── ADR-001.md               ← ADR: Ingestão com Azure Functions (serverless)
    │   ├── ADR-002.md               ← ADR: Estratégia de armazenamento (Azure SQL Database)
    │   └── estimate-cost.xlsx       ← Estimativa de custos (Azure Calculator)
    └── c4/
        ├── 01-context.md            ← C4 Nível 1: Diagrama de Contexto
        ├── 02-container.md          ← C4 Nível 2: Diagrama de Containers
        ├── c4-context.png           ← Imagem do diagrama de contexto
        ├── c4-container.png         ← Imagem do diagrama de containers
```

---

## 🧭 Navegação

### Arquitetura — C4 Model

| Nível | Documento | Descrição |
|---|---|---|
| Nível 1 — Contexto | [`docs/c4/01-context.md`](docs/c4/01-context.md) | Visão geral do sistema e seus atores externos |
| Nível 2 — Containers | [`docs/c4/02-container.md`](docs/c4/02-container.md) | Containers da solução e como se comunicam |

### Decisões de Arquitetura — ADR

| ADR | Documento | Decisão |
|---|---|---|
| ADR-001 | [`docs/adr/ADR-001.md`](docs/adr/ADR-001.md) | Uso de Azure Functions (serverless) para ingestão de dados |
| ADR-002 | [`docs/adr/ADR-002.md`](docs/adr/ADR-002.md) | Azure SQL Database como repositório analítico central |

### Custos

- [`docs/adr/estimate-cost.xlsx`](docs/adr/estimate-cost.xlsx) — Planilha com estimativa de custos no Azure Calculator (50 GB de dados, 2 cores).

---

## 🏗️ Visão Arquitetural Resumida

```
┌─────────────────────────────────────────────────────────┐
│                    ERP VendaMais                        │
│           (sistema proprietário, desde 2019)            │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS/REST
              ┌─────────▼──────────┐
              │  Azure Function    │  ← Ingestão
              │  (Python)          │
              └─────────┬──────────┘
                        │ Azure SDK / HTTPS
              ┌─────────▼──────────┐
              │   Azure Blob       │  ← Armazenamento bruto
              │   Storage          │
              └─────────┬──────────┘
                        │ Blob Trigger
              ┌─────────▼──────────┐
              │  Azure Function    │  ← Transformação
              │  (Python)          │
              └─────────┬──────────┘
                        │ SQL / TDS
              ┌─────────▼──────────┐
              │  Azure SQL         │  ← Data Warehouse
              │  Database          │
              └─────────┬──────────┘
                        │ DirectQuery / Import
              ┌─────────▼──────────┐
              │  Power BI Service  │  ← Dashboards e KPIs
              └────────────────────┘
```

---

## 📋 Principais Decisões Técnicas

**Azure Functions (serverless)** — escolhidas para ingestão pela escalabilidade elástica, custo proporcional ao uso e integração nativa com Azure Service Bus e Event Grid. Funções de baixa latência utilizam plano Premium; demais, plano Consumption.

**Azure SQL Database** — adotado como repositório analítico central pela sinergia com Power BI (DirectQuery/Import nativo), suporte a transações ACID, baixa curva de aprendizado para a equipe de TI da VendaMais e integração com Azure Active Directory.

---

*Projeto desenvolvido para a disciplina DAS-II — 2026.*


**2B-001 — EL com Azure Functions**

**Objetivo:** Construir um pipeline Extract & Load (EL) com Azure Functions que sincroniza dados do banco do professor para o banco do grupo.

**O que foi feito:** As Azure Functions existentes foram utilizadas para extrair os dados do banco ERP VendaMais (fornecido pelo professor) e carregá-los no banco SQL do grupo, replicando todas as tabelas.

SQL Database          Function App         SQL Database
(ERP VendaMais)  ←— Extrair —— ⚡ —— Carregar —→  (Grupo)

Entrega: Via Git + banco populado.
