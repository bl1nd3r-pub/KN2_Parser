export interface Listing {
  id: string;
  title: string;
  price: number | null;
  district: string | null;
  rooms: number | null;
  area: number | null;
  description: string | null;
  photos: string[];
  source_url?: string | null;
  address?: string | null;
  metro?: string | null;
}

export interface Filters {
  search: string;
  priceMin: number | null;
  priceMax: number | null;
  rooms: number | null;
  district: string | null;
}
