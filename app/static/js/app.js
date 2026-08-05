const form = document.getElementById('item-form');
const tbody = document.getElementById('items-body');

async function loadItems() {
  const res = await fetch('/api/items');
  const items = await res.json();

  tbody.innerHTML = '';
  items.forEach((item) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.name}</td>
      <td>${item.quantity}</td>
      <td>$${Number(item.price).toFixed(2)}</td>
      <td>${item.category || '-'}</td>
      <td><button class="delete-btn" data-id="${item.id}">Eliminar</button></td>
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