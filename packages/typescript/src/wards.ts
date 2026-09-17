import type Database from "better-sqlite3";
import { Constituencies } from "./constituencies.js";
import { EntityNotFoundError } from "./errors.js";
import type { Ward } from "./types.js";

interface WardRow {
  id: number;
  code: string;
  name: string;
  constituency_id: number;
  status: string;
}

function toWard(row: WardRow): Ward {
  return { id: row.id, code: row.code, name: row.name, constituencyId: row.constituency_id, status: row.status };
}

export class Wards {
  constructor(private readonly db: Database.Database) {}

  list(): Ward[] {
    const rows = this.db
      .prepare("SELECT id, code, name, constituency_id, status FROM wards ORDER BY name")
      .all() as WardRow[];
    return rows.map(toWard);
  }

  get(nameOrCode: string): Ward {
    const row = this.db
      .prepare(
        "SELECT id, code, name, constituency_id, status FROM wards " +
          "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
      )
      .get(nameOrCode, nameOrCode) as WardRow | undefined;
    if (!row) throw new EntityNotFoundError("ward", nameOrCode);
    return toWard(row);
  }

  inConstituency(constituencyNameOrCode: string): Ward[] {
    const constituency = new Constituencies(this.db).get(constituencyNameOrCode);
    const rows = this.db
      .prepare("SELECT id, code, name, constituency_id, status FROM wards WHERE constituency_id = ? ORDER BY name")
      .all(constituency.id) as WardRow[];
    return rows.map(toWard);
  }

  inCounty(countyNameOrCode: string): Ward[] {
    const rows = this.db
      .prepare(
        `SELECT wards.id, wards.code, wards.name, wards.constituency_id, wards.status
         FROM wards
         JOIN constituencies ON constituencies.id = wards.constituency_id
         JOIN counties ON counties.id = constituencies.county_id
         WHERE counties.name = ? COLLATE NOCASE OR counties.code = ? COLLATE NOCASE
         ORDER BY wards.name`,
      )
      .all(countyNameOrCode, countyNameOrCode) as WardRow[];
    return rows.map(toWard);
  }
}
