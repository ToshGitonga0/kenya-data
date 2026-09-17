import type Database from "better-sqlite3";
import { EntityNotFoundError } from "./errors.js";
import type { County } from "./types.js";

interface CountyRow {
  id: number;
  code: string;
  name: string;
  capital: string | null;
  status: string;
}

function toCounty(row: CountyRow): County {
  return { id: row.id, code: row.code, name: row.name, capital: row.capital, status: row.status };
}

export class Counties {
  constructor(private readonly db: Database.Database) {}

  list(): County[] {
    const rows = this.db
      .prepare("SELECT id, code, name, capital, status FROM counties ORDER BY name")
      .all() as CountyRow[];
    return rows.map(toCounty);
  }

  get(nameOrCode: string): County {
    const row = this.db
      .prepare(
        "SELECT id, code, name, capital, status FROM counties " +
          "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
      )
      .get(nameOrCode, nameOrCode) as CountyRow | undefined;
    if (!row) throw new EntityNotFoundError("county", nameOrCode);
    return toCounty(row);
  }
}
