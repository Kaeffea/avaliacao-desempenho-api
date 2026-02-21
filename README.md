# Avaliação de Desempenho — API

API REST desenvolvida em Django + DRF para gerenciamento de avaliações de desempenho.

## Pré-requisitos

- Python 3.10+
- PostgreSQL 13+

## Instalação
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Crie o arquivo `.env` na raiz:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=avaliacao_desempenho
DB_USER=avaliacao_user
DB_PASSWORD=avaliacao123
DB_HOST=localhost
DB_PORT=5433
```
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Documentação

Acesse [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) para o Swagger.

## Endpoints principais

| Método | URL | Descrição |
|---|---|---|
| GET | `/api/avaliacoes_desempenho/listar/` | Lista avaliações |
| POST | `/api/avaliacoes_desempenho/cadastrar/` | Cria avaliação |
| GET | `/api/avaliacoes_desempenho/cadastrar_avaliacao_form/` | Dados do formulário |
| GET | `/api/avaliacoes_desempenho/{id}/visualizar/` | Detalhe |
| POST | `/api/avaliacoes_desempenho/{id}/iniciar/` | Inicia avaliação |
| POST | `/api/avaliacoes_desempenho/{id}/editar/` | Edita avaliação |
| POST | `/api/avaliacoes_desempenho/{id}/dar_feedback/` | Envia para avaliação |
| POST | `/api/avaliacoes_desempenho/{id}/concluir/` | Conclui avaliação |