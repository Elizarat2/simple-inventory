const form = document.getElementById('item-form');
const tbody = document.getElementById('items-body');
const table = document.getElementById('items-table');
const emptyState = document.getElementById('empty-state');
const stockCount = document.getElementById('stock-count');

const LOW_STOCK_THRESHOLD = 5;

async function loadItems() {
  const res = await fetch('/api/items');
  const items = await res.json();

  tbody.innerHTML = '';
  stockCount.textContent = `${items.length} ${items.length === 1 ? 'registro' : 'registros'}`;

  if (items.length === 0) {
    table.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }

  table.style.display = '';
  emptyState.style.display = 'none';

  items.forEach((item) => {
    const isLow = item.quantity <= LOW_STOCK_THRESHOLD;
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.name}</td>
      <td class="num"><span class="qty-badge ${isLow ? 'qty-low' : 'qty-ok'}">${item.quantity}</span></td>
      <td class="num">$${Number(item.price).toFixed(2)}</td>
      <td>${item.category || '—'}</td>
      <td><button class="delete-btn" data-id="${item.id}" title="Eliminar" aria-label="Eliminar ${item.name}">✕</button></td>
    `;
    tbody.appendChild(row);
  });
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    name: document.getElementById('name').value,
    quantity: Number(document.getElementById('quantity').value),
    price: Number(document.getElementById('price').value),
    category: document.getElementById('category').value,
  };

  await fetch('/api/items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  form.reset();
  loadItems();
});

tbody.addEventListener('click', async (e) => {
  if (e.target.classList.contains('delete-btn')) {
    const id = e.target.dataset.id;
    await fetch(`/api/items/${id}`, { method: 'DELETE' });
    loadItems();
  }
});

loadItems();