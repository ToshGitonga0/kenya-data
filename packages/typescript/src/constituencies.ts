import type Database from "better-sqlite3";
import { Counties } from "./counties.js";
import { EntityNotFoundError } from "./errors.js";
import type { Constituency } from "./types.js";

interface ConstituencyRow {
  id: number;
  code: string;
  name: string;
  county_id: number;
  status: string;
}

function toConstituency(row: ConstituencyRow): Constituency {
  return { id: row.id, code: row.code, name: row.name, countyId: row.county_id, status: row.status };
}

export class Constituencies {
  constructor(private readonly db: Database.Database) {}

  list(): Constituency[] {
    const rows = this.db
      .prepare("SELECT id, code, name, county_id, status FROM constituencies ORDER BY name")
      .all() as ConstituencyRow[];
    return rows.map(toConstituency);
  }

  get(nameOrCode: string): Constituency {
    const row = this.db
      .prepare(
        "SELECT id, code, name, county_id, status FROM constituencies " +
          "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
      )
      .get(nameOrCode, nameOrCode) as ConstituencyRow | undefined;
    if (!row) throw new EntityNotFoundError("constituency", nameOrCode);
    return toConstituency(row);
  }

  inCounty(countyNameOrCode: string): Constituency[] {
    const county = new Counties(this.db).get(countyNameOrCode);
    const rows = this.db
      .prepare(
        "SELECT id, code, name, county_id, status FROM constituencies " +
          "WHERE county_id = ? ORDER BY name",
      )
      .all(county.id) as ConstituencyRow[];
    return rows.map(toConstituency);
  }
}
