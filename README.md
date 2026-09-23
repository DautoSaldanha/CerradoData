# CerradoData

## Variáveis da Vercel

Além das variáveis de conexão do PostgreSQL (`NAME`, `USER`, `PASSWORD` e
`HOST`), configure estas variáveis no ambiente **Production** da Vercel:

- `SECRET_KEY`
- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

Durante cada deploy, as migrações são aplicadas e o superusuário é criado ou
atualizado com esses valores. Não salve a senha no repositório.