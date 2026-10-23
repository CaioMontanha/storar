# STORAR - Previsao de estoque

Aplicacao de controle e previsao de estoque. `frontend` contem o React + TypeScript + Vite. `backend` contem a API Django REST e o banco SQLite local.

## Iniciar em desenvolvimento

Abra dois terminais na raiz do projeto:

```powershell
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

```powershell
cd frontend
npm install
npm run dev
```

Acesse http://localhost:5173. O Vite encaminha `/api` para `http://127.0.0.1:8000`. O banco persistente fica em `backend/db.sqlite3`; nao e necessario instalar PostgreSQL para desenvolvimento. Para usar PostgreSQL, defina `DATABASE_URL` e instale `backend/requirements.txt`.

O primeiro acesso cria apenas o local vazio `Porto de Galinhas`. Produtos e vendas nao sao pre-carregados. Se houver produtos na versao anterior, a interface tenta importalos para o banco na primeira conexao.

## Testes e build

```powershell
cd backend
python manage.py test
```

```powershell
cd frontend
npm test
npm run build
```

## Persistencia e portfolio

Cidades/estoques, produtos, vendas e reposicoes sao persistidos no banco. O endereco do portfolio pode ser configurado pelo botao flutuante; fica salvo no navegador. Tambem aceita a variavel de ambiente `VITE_PORTFOLIO_URL`.
