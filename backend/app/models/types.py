"""Cross-database integer types: PostgreSQL BIGINT/bigserial vs SQLite INTEGER autoincrement."""

from sqlalchemy import BigInteger, Integer

# SQLite only autoincrements INTEGER PRIMARY KEY; BigInteger PK inserts can fail without this.
bigint = BigInteger().with_variant(Integer(), "sqlite")
