import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { after, before, describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import { Kenya, EntityNotFoundError } from "../src/index.js";

const repoRoot = join(fileURLToPath(new URL("../../../", import.meta.url)));

describe("Kenya SDK", () => {
  let dbPath: string;
  let kenya: Kenya;

  before(() => {
    const dir = mkdtempSync(join(tmpdir(), "kenya-data-ts-"));
    dbPath = join(dir, "kenya.db");
    execFileSync("python3", [join(repoRoot, "database", "seeds", "load_approved_data.py"), dbPath]);
    kenya = new Kenya({ dbPath });
  });

  after(() => {
    kenya.close();
  });

  it("lists counties from the real dataset", () => {
    assert.ok(kenya.counties.list().length > 0);
  });

  it("gets a county case-insensitively", () => {
    assert.equal(kenya.counties.get("nakuru").name.toLowerCase(), "nakuru");
  });

  it("throws EntityNotFoundError for unknown counties", () => {
    assert.throws(() => kenya.counties.get("Not A Real County"), EntityNotFoundError);
  });

  it("finds constituencies in a county", () => {
    const constituencies = kenya.constituencies.inCounty("Nakuru");
    assert.ok(constituencies.length > 0);
  });

  it("finds wards in a constituency", () => {
    const constituency = kenya.constituencies.list()[0]!;
    const wards = kenya.wards.inConstituency(constituency.code);
    assert.ok(wards.every((w) => w.constituencyId === constituency.id));
  });

  it("traverses county -> constituency -> ward for wards.inCounty", () => {
    assert.ok(kenya.wards.inCounty("Nakuru").length > 0);
  });

  it("exposes dataset metadata", () => {
    assert.ok(kenya.dataset.version);
    assert.ok(kenya.dataset.updatedAt);
  });
});
