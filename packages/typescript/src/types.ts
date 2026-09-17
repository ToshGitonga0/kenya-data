export interface County {
  id: number;
  code: string;
  name: string;
  capital: string | null;
  status: string;
}

export interface Constituency {
  id: number;
  code: string;
  name: string;
  countyId: number;
  status: string;
}

export interface Ward {
  id: number;
  code: string;
  name: string;
  constituencyId: number;
  status: string;
}

export interface DatasetInfo {
  version: string;
  status: string;
  updatedAt: string;
}
