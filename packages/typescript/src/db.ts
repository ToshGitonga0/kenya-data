import Database from "better-sqlite3";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

export function defaultDbPath(): string {
  // src/db.ts -> ../../../../data/kenya.db (packages/typescript/src -> repo root)
  const here = dirname(fileURLToPath(import.meta.url));
  return join(here, "..", "..", "..", "data", "kenya.db");
}

export function connect(dbPath?: string): Database.Database {
  const path = dbPath ?? defaultDbPath();
  if (!existsSync(path)) {
    throw new Error(
      `No Kenya Data database found at ${path}. ` +
        "Run 'make build-db' (or pass dbPath to the Kenya constructor).",
    );
  }
  const db = new Database(path, { readonly: true, fileMustExist: true });
  db.pragma("foreign_keys = ON");
  return db;
}
