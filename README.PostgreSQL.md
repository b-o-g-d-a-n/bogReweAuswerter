# PostgreSQL Setup

## Table Creation

Create table
```
CREATE TABLE groceries (
    id BIGSERIAL PRIMARY KEY,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    price NUMERIC(6,2) NOT NULL,
    category TEXT NOT NULL,
    top_category TEXT NOT NULL
);
```

## User

Create grocery_admin user
- `CREATE USER grocery_admin WITH PASSWORD 'CHANGE_STRONGPASSWORD';`

Create grafana user
- `CREATE USER grafana WITH PASSWORD 'CHANGE_STRONGPASSWORD';`


## Permissions

Change owner to grafana
- `ALTER TABLE groceries OWNER TO "grocery_admin";`

Allow Grafana read-only access
- `GRANT CONNECT ON DATABASE grocery TO grafana;`
- `GRANT SELECT ON TABLE groceries TO grafana;`

Allow sequence usage (for completeness, not strictly needed for readonly)
- `GRANT USAGE, SELECT ON SEQUENCE groceries_id_seq TO grafana;`

