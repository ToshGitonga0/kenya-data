import type Database from "better-sqlite3";
import { connect } from "./db.js";
import { Counties } from "./counties.js";
import { Constituencies } from "./constituencies.js";
import { Wards } from "./wards.js";
import { Dataset } from "./dataset.js";

export { EntityNotFoundError, KenyaDataError } from "./errors.js";
export type { County, Constituency, Ward, DatasetInfo } from "./types.js";

export interface KenyaOptions {
  dbPath?: string;
}

export class Kenya {
  private readonly db: Database.Database;
  public readonly counties: Counties;
  public readonly constituencies: Constituencies;
  public readonly wards: Wards;
  public readonly dataset: Dataset;

  constructor(options: KenyaOptions = {}) {
    this.db = connect(options.dbPath);
    this.counties = new Counties(this.db);
    this.constituencies = new Constituencies(this.db);
    this.wards = new Wards(this.db);
    this.dataset = new Dataset(this.db);
  }

  close(): void {
    this.db.close();
  }
}
