import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getUserRole } from '../utils/auth'


function ProductPage() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ 
    product_id: '', 
    name: '', 
    price: '', 
    description: '',
    seller_id: 'user_002'
  })
  const [editId, setEditId] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const API_BASE = 'http://localhost:8000/products/'

  const role = getUserRole()
  const isBuyer = role === 'buyer'

  const getAuthHeaders = () => {
    const token = localStorage.getItem("jwt")
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    }
  }

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const res = await fetch(API_BASE, {
        headers: getAuthHeaders()
      })

      if (!res.ok) {
        throw new Error(`API error: ${res.status}`)
      }

      const data = await res.json()
      setProducts(data)
      setError(null)
    } catch (err) {
      console.error("Failed to fetch products:", err)
      setError("Error loading products. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm({ ...form, [name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const productData = { ...form, price: parseFloat(form.price) }
    const method = editId ? 'PUT' : 'POST'
    const url = editId ? `${API_BASE}/${editId}` : API_BASE

    try {
      const res = await fetch(url, {
        method,
        headers: getAuthHeaders(),
        body: JSON.stringify(productData),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || 'Unknown error occurred')
      }

      setForm({ product_id: '', name: '', price: '', description: '', seller_id: 'user_002' })
      setEditId(null)
      fetchProducts()
      setError(null)
    } catch (err) {
      console.error("Failed to save product:", err)
      setError(err.message || "Error saving product. Please try again.")
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this product?')) return

    try {
      const res = await fetch(`${API_BASE}/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || 'Failed to delete')
      }

      fetchProducts()
      setError(null)
    } catch (err) {
      console.error("Failed to delete product:", err)
      setError(err.message || "Error deleting product. Please try again.")
    }
  }

  const handleEdit = (product) => {
    setForm({
      product_id: product.product_id,
      name: product.name,
      price: product.price.toString(),
      description: product.description || '',
      seller_id: product.seller_id
    })
    setEditId(product.product_id)
  }

  const handleCancel = () => {
    setForm({ product_id: '', name: '', price: '', description: '', seller_id: 'user_002' })
    setEditId(null)
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 15px' }}>
      <h1>Product Manager</h1>

      {error && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#ffcccc', 
          color: '#990000',
          borderRadius: '4px',
          marginBottom: '15px'
        }}>
          {error}
        </div>
      )}

      {!isBuyer && (
      <form onSubmit={handleSubmit} style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '15px' }}>
          <input
            name="product_id"
            placeholder="Product ID"
            value={form.product_id}
            onChange={handleChange}
            disabled={!!editId}
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
            step="0.01"
            placeholder="Price"
            value={form.price}
            onChange={handleChange}
            required
          />
          <input
            name="seller_id"
            placeholder="Seller ID"
            value={form.seller_id}
            onChange={handleChange}
            required
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <textarea
            name="description"
            placeholder="Product Description"
            value={form.description}
            onChange={handleChange}
            style={{ 
              width: '100%', 
              height: '80px', 
              padding: '0.6em 1.2em', 
              borderRadius: '8px', 
              backgroundColor: '#1e1e1e', 
              color: 'white',
              boxSizing: 'border-box',
              fontFamily: 'inherit',
              fontSize: '1rem',
              resize: 'vertical'
            }}
            required
          />
        </div>
        
        
        <div>
          <button type="submit">{editId ? 'Update' : 'Add'} Product</button>
          {editId && (
            <button type="button" onClick={handleCancel}>Cancel</button>
          )}
        </div>
      </form>
      )}

      {loading ? (
        <div>Loading products...</div>
      ) : (
        <table border="1" style={{ marginTop: '2rem', width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
              <th style={{ padding: '8px', textAlign: 'left' }}>Name</th>
              <th style={{ padding: '8px', textAlign: 'left' }}>Price</th>
              <th style={{ padding: '8px', textAlign: 'left' }}>Description</th>
              <th style={{ padding: '8px', textAlign: 'left' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.product_id}>
                <td style={{ padding: '8px' }}>{p.product_id}</td>
                <td style={{ padding: '8px' }}>
                  <Link to={`/products/${p.product_id}`}>{p.name}</Link>
                </td>
                <td style={{ padding: '8px' }}>${p.price.toFixed(2)}</td>
                <td style={{ padding: '8px' }}>
                  {p.description ? p.description.substring(0, 50) + (p.description.length > 50 ? '...' : '') : ''}
                </td>
                
                <td style={{ padding: '8px' }}>
                  {!isBuyer && (
                    <>
                      <button onClick={() => handleEdit(p)} style={{ marginRight: '5px' }}>Edit</button>
                      <button onClick={() => handleDelete(p.product_id)}>Delete</button>
                    </>
                  )}
                </td>

              </tr>
            ))}
            {products.length === 0 && (
              <tr><td colSpan="5" style={{ padding: '8px', textAlign: 'center' }}>No products available</td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default ProductPage
