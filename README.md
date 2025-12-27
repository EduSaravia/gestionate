# Proyecto: Flujo (Finanzas personales)

App web en Django 4.2 para organizar ingresos, gastos y suscripciones con base de datos PostgreSQL (SQLite opcional para pruebas rapidas). Diseno responsivo listo para movil.

## Requisitos
- Python 3.8+
- PostgreSQL si usaras la BD final

## Instalacion rapida
```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows PowerShell
python -m pip install -r requirements.txt
```

Configura tus variables de entorno (se carga automaticamente un archivo `.env` en la raiz):
```bash
copy .env.example .env
```
Variables clave:
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `DJANGO_SECRET_KEY` y `DJANGO_DEBUG`

Si no defines `POSTGRES_DB`, se usara SQLite para desarrollo.

## Migraciones y arranque
```bash
python manage.py migrate
python manage.py runserver
```

## URLs utiles
- Dashboard: `/`
- Login: `/login/`
- Registro: `/registro/`
- Admin: `/admin/`

## Funcionalidades clave
- Registro de gastos/ingresos con medio de pago (Yape, efectivo, tarjeta, etc.) y moneda (PEN por defecto, USD opcional).
- Suscripciones con fechas proximas/atrasadas.
- Panel con balance, gasto mensual y desglose de gasto por categoria.

## Notas de diseno
- Tema oscuro con acentos verde/turquesa.
- Layout responsivo (grid adaptable, tipografia Manrope).
- Formularios listos para movil y escritorio.
