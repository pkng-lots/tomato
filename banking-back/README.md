Добавление миграции с кастомным номером ревизии

`alembic revision --autogenerate  -m "create base payments table" --rev-id=1`

Добавление миграции с шаблонным номером ревизии

`alembic revision --autogenerate -m "create base payments table 3"`

Список шаблонов генерации конфигурации
`alembic list_templates`

`alembic init --template async alembic`

`alembic upgrade head`