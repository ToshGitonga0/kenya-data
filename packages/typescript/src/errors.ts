export class KenyaDataError extends Error {}

export class EntityNotFoundError extends KenyaDataError {
  constructor(
    public readonly entityType: string,
    public readonly identifier: string,
  ) {
    super(`No ${entityType} found matching "${identifier}"`);
    this.name = "EntityNotFoundError";
  }
}
