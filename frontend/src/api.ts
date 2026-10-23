export type Product = { id: number; sku: string; nome: string; estoque_atual: number; prazo_reposicao_dias: number; media_diaria: number; dias_restantes: number | null; status: string; pedir_ate: string | null; reposicao_atrasada: boolean; store_id: number };
export type Sale = { data: string; quantidade: number };
export type Store = { id: number; nome: string };

const base = import.meta.env.VITE_API_URL || '';
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${base}/api${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...init?.headers } });
  if (!response.ok) {
    let payload: any;
    try { payload = await response.json(); } catch { /* response has no JSON body */ }
    const detail = payload?.detail;
    const message = payload?.mensagem || (typeof detail === 'string' ? detail : detail?.mensagem) || payload?.non_field_errors?.[0] || `Falha na API (${response.status}).`;
    throw new Error(message);
  }
  return response.status === 204 ? undefined as T : response.json();
}
const json = (method: string, data: unknown): RequestInit => ({ method, body: JSON.stringify(data) });

async function migrateBrowserData(stores: Store[]) {
  if (localStorage.getItem('storar.db.migrated.v1')) return stores;
  const raw = localStorage.getItem('storar.local.v1');
  if (!raw) { localStorage.setItem('storar.db.migrated.v1', '1'); return stores; }
  try {
    const old = JSON.parse(raw);
    const mapped = new Map<number, number>();
    for (const oldStore of old.stores || []) {
      let found = stores.find(s => s.nome.toLocaleLowerCase() === oldStore.nome.toLocaleLowerCase());
      if (!found) { found = await request<Store>('/stores/', json('POST', { nome: oldStore.nome })); stores = [...stores, found]; }
      mapped.set(oldStore.id, found.id);
    }
    for (const product of old.products || []) {
      if (!product.ativo) continue;
      const remoteStoreId = mapped.get(product.store_id);
      if (!remoteStoreId) continue;
      const existing = await request<Product[]>(`/products/?store_id=${remoteStoreId}&search=${encodeURIComponent(product.sku)}`);
      if (existing.some(p => p.sku.toLocaleLowerCase() === product.sku.toLocaleLowerCase())) continue;
      const history = product.historico || [];
      const restoredStock = Number(product.estoque_atual) + history.reduce((n: number, sale: Sale) => n + sale.quantidade, 0);
      const created = await request<Product>('/products/', json('POST', { store_id: remoteStoreId, sku: product.sku, nome: product.nome, estoque_atual: restoredStock, prazo_reposicao_dias: product.prazo_reposicao_dias }));
      for (const sale of history) await request(`/products/${created.id}/sales/`, json('POST', { data: sale.data, quantidade: sale.quantidade }));
    }
    localStorage.setItem('storar.db.migrated.v1', '1');
  } catch (error) {
    console.error('Importação dos dados locais para o banco falhou.', error);
    throw new Error('Não foi possível importar os dados deste navegador para o banco. Tente novamente.');
  }
  return stores;
}

export const api = {
  stores: async () => {
    let stores = await request<Store[]>('/stores/');
    if (!stores.length) stores = [await request<Store>('/stores/', json('POST', { nome: 'Porto de Galinhas' }))];
    return migrateBrowserData(stores);
  },
  addStore: (nome: string) => request<Store>('/stores/', json('POST', { nome })),
  renameStore: (id: number, nome: string) => request<Store>(`/stores/${id}/`, json('PATCH', { nome })),
  products: (query: string) => request<Product[]>(`/products/${query}`),
  dashboard: () => request<any>('/dashboard/'),
  product: (id: number) => request<Product>(`/products/${id}/`),
  sales: async (id: number) => {
    const rows = await request<{ data: string; quantidade: number }[]>(`/products/${id}/sales/?days=30`);
    return rows.map(row => ({ data: row.data, quantidade: row.quantidade }));
  },
  sell: (id: number, quantidade: number) => request(`/products/${id}/sales/`, json('POST', { quantidade })),
  restock: (id: number, quantidade: number) => request(`/products/${id}/restock/`, json('POST', { quantidade })),
  update: (id: number, data: Partial<Product>) => request<Product>(`/products/${id}/`, json('PATCH', data)),
  create: (data: Partial<Product>) => request<Product>('/products/', json('POST', data)),
};
