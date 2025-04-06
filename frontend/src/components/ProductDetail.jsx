import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [form, setForm] = useState({
    name: '',
    price: '',
    description: '',
    seller_id: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:8000/products/';

  const getAuthHeaders = () => {
    const token = localStorage.getItem("jwt");
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };
  };

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE}${id}`, {
          headers: getAuthHeaders(),
        });

        if (!res.ok) {
          if (res.status === 404) {
            throw new Error('Product not found');
          }
          throw new Error('Failed to fetch product');
        }

        const data = await res.json();
        setProduct(data);
        setForm({
          name: data.name,
          price: data.price.toString(),
          description: data.description || '',
          seller_id: data.seller_id
        });
        setError(null);
      } catch (err) {
        console.error('Error fetching product:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const updatedProduct = {
        ...form,
        price: parseFloat(form.price)
      };

      const res = await fetch(`${API_BASE}${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(updatedProduct)
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Failed to update product');
      }

      const refreshRes = await fetch(`${API_BASE}${id}`, {
        headers: getAuthHeaders(),
      });
      if (refreshRes.ok) {
        const data = await refreshRes.json();
        setProduct(data);
        setIsEditing(false);
        setError(null);
      }
    } catch (err) {
      console.error('Error updating product:', err);
      setError(err.message || 'Failed to update product. Please try again.');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      const res = await fetch(`${API_BASE}${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || 'Failed to delete product');
      }

      navigate('/products');
    } catch (err) {
      console.error('Error deleting product:', err);
      setError(err.message || 'Failed to delete product. Please try again.');
    }
  };

  if (loading) return <div>Loading product details...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!product) return <div>Product not found</div>;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '0 15px' }}>
      <h1>Product Details</h1>

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

      {isEditing ? (
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', marginBottom: '20px' }}>
            <div>
              <label htmlFor="name" style={{ display: 'block', marginBottom: '5px' }}>Name:</label>
              <input
                id="name"
                name="name"
                type="text"
                value={form.name}
                onChange={handleChange}
                required
                style={{ width: '100%' }}
              />
            </div>

            <div>
              <label htmlFor="price" style={{ display: 'block', marginBottom: '5px' }}>Price:</label>
              <input
                id="price"
                name="price"
                type="number"
                min="0"
                step="0.01"
                value={form.price}
                onChange={handleChange}
                required
                style={{ width: '100%' }}
              />
            </div>

            <div>
              <label htmlFor="description" style={{ display: 'block', marginBottom: '5px' }}>Description:</label>
              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                rows="4"
                style={{
                  width: '100%',
                  padding: '0.6em 1.2em',
                  borderRadius: '8px',
                  backgroundColor: '#1e1e1e',
                  color: 'white',
                  fontFamily: 'inherit',
                  fontSize: '1rem',
                  resize: 'vertical'
                }}
                required
              />
            </div>

            <div>
              <label htmlFor="seller_id" style={{ display: 'block', marginBottom: '5px' }}>Seller ID:</label>
              <input
                id="seller_id"
                name="seller_id"
                type="text"
                value={form.seller_id}
                onChange={handleChange}
                required
                style={{ width: '100%' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit">Save Changes</button>
            <button type="button" onClick={() => setIsEditing(false)}>
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
            <div>
              {product.images && product.images.length > 0 ? (
                <img
                  src={product.images[0]}
                  alt={product.name}
                  style={{
                    maxWidth: '300px',
                    maxHeight: '300px',
                    objectFit: 'contain',
                    border: '1px solid #333',
                    borderRadius: '4px'
                  }}
                />
              ) : (
                <div
                  style={{
                    width: '300px',
                    height: '200px',
                    backgroundColor: '#444',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    borderRadius: '4px'
                  }}
                >
                  No Image Available
                </div>
              )}
            </div>

            <div style={{ flex: '1', minWidth: '300px' }}>
              <h2 style={{ marginTop: '0' }}>{product.name}</h2>
              <p><strong>Product ID:</strong> {product.product_id}</p>
              <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
              <p><strong>Seller ID:</strong> {product.seller_id}</p>
              <div>
                <strong>Description:</strong>
                <p>{product.description || 'No description available'}</p>
              </div>

              <div style={{ marginTop: '1.5rem', display: 'flex', gap: '10px' }}>
                <button onClick={() => setIsEditing(true)}>
                  Edit
                </button>
                <button onClick={handleDelete}>
                  Delete
                </button>
                <button onClick={() => navigate('/products')}>
                  Back to Products
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ProductDetail;
