import type Database from "better-sqlite3";
import type { DatasetInfo } from "./types.js";

interface DatasetVersionRow {
  version: string;
  status: string;
  created_at: string;
}

export class Dataset {
  constructor(private readonly db: Database.Database) {}

  info(): DatasetInfo {
    const row = this.db
      .prepare("SELECT version, status, created_at FROM dataset_versions ORDER BY id DESC LIMIT 1")
      .get() as DatasetVersionRow | undefined;
    if (!row) return { version: "unknown", status: "unknown", updatedAt: "unknown" };
    return { version: row.version, status: row.status, updatedAt: row.created_at };
  }

  get version(): string {
    return this.info().version;
  }

  get updatedAt(): string {
    return this.info().updatedAt;
  }
}
