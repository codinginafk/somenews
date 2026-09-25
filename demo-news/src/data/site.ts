// Single source of truth for the publication brand.
// Rename = change `name` here. Header, footer, and OG all follow.
export const SITE = {
  name: 'rentfreenews',
  displayName: 'Rent Free News',
  tagline: 'Claims vs data',
  description: 'Reality checks with receipts: viral claims vs primary data, country briefs, and lab-tested tech.',
  email: 'desk@rentfreenews.com',
  adsEmail: 'ads@rentfreenews.com',
  ga4Id: 'G-GBVRW0DMEC',
};

export function authorSlug(name: string): string {
  return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}
