# Churrascaria Norma's — site em Python/Flask

Site responsivo com backend em Flask, reservas, formulário de contato, painel administrativo, mapa, links de rota e integração com a loja do restaurante no iFood.

## Recursos

- Home premium e responsiva
- CTA direto para o iFood
- Google Maps incorporado + link de rota
- Link para Waze e Instagram
- Horários e telefone
- Formulário de solicitação de reservas salvo em SQLite
- Formulário de contato salvo em SQLite
- Painel administrativo para visualizar reservas e mensagens
- Status de reserva: Pendente, Confirmada, Cancelada
- SEO com dados estruturados Schema.org
- Endpoint `/health` para monitoramento
- Pronto para Render/Railway/Fly.io/servidor com Gunicorn

## Rodar localmente

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Crie um arquivo `.env` se quiser usar um carregador de variáveis, ou configure no terminal/hosting:

- `SECRET_KEY`: chave aleatória longa
- `ADMIN_PASSWORD`: senha forte do painel
- `PORT`: opcional

Depois:

```bash
python app.py
```

Abra `http://127.0.0.1:5000`.

Painel: `http://127.0.0.1:5000/admin/login`

> Se `ADMIN_PASSWORD` não estiver configurada, o fallback de desenvolvimento é `troque-esta-senha`. Troque antes de publicar.

## Integração com iFood

O projeto usa o link oficial da loja do Norma's no iFood para concluir pedidos dentro da plataforma do iFood. Isso funciona sem armazenar dados de pagamento e sem depender de APIs privadas.

Uma sincronização de catálogo/pedidos dentro do próprio site exige credenciais e aprovação do ecossistema/API oficial do iFood para o estabelecimento. Não é correto inventar tokens ou contornar esse acesso; com as credenciais oficiais, o backend pode ser ampliado.

## Fotos

A galeria inclui uma imagem pública externa apenas como referência visual de protótipo. Antes de colocar o site comercial em produção, substitua por fotos próprias/autorizadas do restaurante para evitar dependência de terceiros e garantir os direitos de uso.

## Dados usados

- Nome: Churrascaria Norma's
- Endereço: R. José d'Ávila, 40 - Centro, Nova Lima - MG, 34000-000
- Telefone: (31) 3541-3001
- Categorias públicas: churrascaria, self-service e pizzaria
- Perfil público: @normasrestaurante
- Horários públicos consultados em setembro de 2026

Os horários e o cardápio podem mudar. Atualize as informações antes da publicação definitiva.
