import { useEffect, useState } from 'react'

function ProductPage() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ product_id: '', name: '', price: '' })
  const [editId, setEditId] = useState(null)

  const API_BASE = 'http://localhost:8000/products'

  // Fetch all products
  const fetchProducts = async () => {
    const res = await fetch(API_BASE)
    const data = await res.json()
    setProducts(data)
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const method = editId ? 'PUT' : 'POST'
    const url = editId ? `${API_BASE}/${editId}` : API_BASE

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...form,
        price: parseFloat(form.price), // ✅ Ensure price is a number
      }),
    })

    if (res.ok) {
      setForm({ product_id: '', name: '', price: '' }) // ✅ Reset price as empty string
      setEditId(null)
      fetchProducts()
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this product?')) return
    const res = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' })
    if (res.ok) fetchProducts()
  }

  const handleEdit = (product) => {
    setForm(product)
    setEditId(product.product_id)
  }

  return (
    <div>
      <h1>Product Manager</h1>
      <form onSubmit={handleSubmit}>
        <input
          name="product_id"
          placeholder="Product ID"
          value={form.product_id}
          onChange={handleChange}
          disabled={!!editId} // disable when editing
          required
        />
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          name="price"
          type="number"
          min="0"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
        />
        <button type="submit">{editId ? 'Update' : 'Add'} Product</button>
        {editId && <button onClick={() => {
          setForm({ product_id: '', name: '', price: '' })
          setEditId(null)
        }}>Cancel</button>}
      </form>

      <table border="1" style={{ marginTop: '2rem', width: '100%' }}>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Price</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.product_id}>
              <td>{p.product_id}</td>
              <td>{p.name}</td>
              <td>{p.price}</td>
              <td>
                <button onClick={() => handleEdit(p)}>Edit</button>
                <button onClick={() => handleDelete(p.product_id)}>Delete</button>
              </td>
            </tr>
          ))}
          {products.length === 0 && (
            <tr><td colSpan="4">No products available</td></tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
  
export default ProductPage
  