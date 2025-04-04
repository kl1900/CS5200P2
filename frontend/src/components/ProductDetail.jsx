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
  
  const API_BASE = 'http://localhost:8000/products';

  // Fetch product details when component mounts or ID changes
  useEffect(() => {
    const token = localStorage.getItem('token');
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE}/${id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch product');
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
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  // Simple UI for displaying product details
  if (loading) return <div>Loading product details...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!product) return <div>Product not found</div>;

  return (
    <div style={{ padding: '1rem' }}>
      <h1>Product Details</h1>
      <div>
        <strong>Name:</strong> {product.name}
      </div>
      <div>
        <strong>Price:</strong> ${product.price.toFixed(2)}
      </div>
      <div>
        <strong>Description:</strong> {product.description}
      </div>
      <div>
        <strong>Seller ID:</strong> {product.seller_id}
      </div>
      <button onClick={() => navigate('/products')}>Back to Products</button>
    </div>
  );
}

export default ProductDetail;
