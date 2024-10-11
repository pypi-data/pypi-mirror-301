UTF8 = "utf-8"
GB = 1073741824


def get_dev_database_ddl(
    db: str,
    *,
    comment: str,
    parent_db: str = "E00_WSP",
    perm_gb: int = 0,
    spool_gb: int = 0,
    temp_gb: int = 0,
    read_role: str = "E00_WSP_Read",
    write_role: str = "E00_WSP_Dev",
    admin_role: str = "E00_WSP_Admin",
    load_user: str | list = "UED1_TGT_LOAD",
) -> str:
    if isinstance(load_user, str):
        _load_users = [load_user]
    else:
        _load_users = load_user

    db = db.upper().strip()
    comment = comment.replace("''", "'").replace("'", "''").strip()
    _write_rights = ", ".join(
        [
            "SELECT",
            "SHOW",
            "NONTEMPORAL",
            "INSERT",
            "UPDATE",
            "DELETE",
            "STATISTICS",
            "ALTER PROCEDURE",
            "CREATE TABLE",
            "CREATE VIEW",
            "CREATE MACRO",
            "CREATE TRIGGER",
            "CREATE PROCEDURE",
            "DROP TABLE",
            "DROP VIEW",
            "DROP MACRO",
            "DROP TRIGGER",
            "DROP PROCEDURE",
            "ALTER FUNCTION",
            "CREATE FUNCTION",
            "DROP FUNCTION",
            "CREATE OWNER PROCEDURE",
            "EXECUTE",
            "EXECUTE PROCEDURE",
            "EXECUTE FUNCTION",
        ]
    )

    _read_rights = "SELECT, SHOW"
    statements = [
        "-" * 60,
        f"-- {db}",
        "-" * 60,
        (
            f"CREATE DATABASE {db} FROM {parent_db} AS "
            + f"PERM = {perm_gb}*{GB} SPOOL = {spool_gb}*{GB}"
            + " TEMPORARY = {temp_gb}*{GB};"
        ),
        f"COMMENT ON DATABASE {db} IS '{comment}'",
        f"GRANT DUMP, RESTORE, CHECKPOINT ON {db} TO BARUSER_ROLE;",
        "-- dev roles",
        f"GRANT CREATE DATABASE, DROP DATABASE ON {db} TO {admin_role};",
        f"GRANT {_write_rights} ON {db} TO {write_role};",
        f"GRANT {_read_rights} ON {db} TO {read_role};",
    ]

    for ldu in _load_users:
        statements.append(f"-- load user: {ldu}")
        statements.append(f"GRANT {_write_rights} ON {db} TO {ldu};")

    # práva pro V_LOAD a V
    V_LOAD_SUFFIX = "_V_LOAD"
    V_SUFFIX = "_V"
    VP_SUFFIX = "_VP"
    if db.endswith(V_LOAD_SUFFIX) or db.endswith(
        VP_SUFFIX
    ):  # V_LOAD práva, čteme produkci a dev
        statements.append("-- v_load")
        core_db = db.removesuffix(V_LOAD_SUFFIX)
        dev_pfx = db.split("_")[0]
        if not db.endswith("STG_V_LOAD"):  # tgt a tda
            for grant_on in [core_db, f"EP{core_db.removeprefix(dev_pfx)}"]:
                statements.append(
                    f"GRANT SELECT ON {grant_on} TO {db} WITH GRANT OPTION;"
                )
        else:  # stg
            statements.append(f"GRANT SELECT ON AP_STG TO {db} WITH GRANT OPTION;")
            statements.append(
                f"GRANT SELECT ON {dev_pfx.replace('E', 'A')}_STG TO {db} "
                + "WITH GRANT OPTION;"
            )
    elif db.endswith(V_SUFFIX):  # access layer práva
        statements.append("-- access layer")
        statements.append(
            f"GRANT SELECT ON {db.removesuffix(V_SUFFIX)} TO {db} WITH GRANT OPTION;"
        )
    statements.append("")
    return "\n".join(statements)
