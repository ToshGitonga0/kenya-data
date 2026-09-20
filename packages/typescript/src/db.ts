import Database from "better-sqlite3";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export function defaultDbPath(): string {
  const here = dirname(fileURLToPath(import.meta.url));

  // Installed package: dist/db.js -> package root/data/kenya.db
  const packaged = join(here, "..", "data", "kenya.db");
  if (existsSync(packaged)) return packaged;

  // Local development checkout.
  return join(here, "..", "..", "..", "data", "kenya.db");
}

export function connect(dbPath?: string): Database.Database {
  const path = dbPath ?? defaultDbPath();

  if (!existsSync(path)) {
    throw new Error(
      `No Kenya Data database found at ${path}. ` +
      "Build the database first or pass dbPath to the Kenya constructor.",
    );
  }

  const db = new Database(path, { readonly: true, fileMustExist: true });
  db.pragma("foreign_keys = ON");
  return db;
}