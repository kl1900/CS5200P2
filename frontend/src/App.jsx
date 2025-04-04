import { Routes, Route, Link } from 'react-router-dom';
import ProductPage from './pages/Products';
import ProductDetail from './components/ProductDetail';
import CartPage from './pages/Carts';
import Login from './pages/Login';
import ProtectedRoute from './ProtectedRoute';

function App() {
  return (
    <div>
      <nav style={{ padding: '1rem', backgroundColor: '#1a1a1a' }}>
        <Link to="/">Home</Link> |{' '}
        <Link to="/products">Products</Link> |{' '}
        <Link to="/carts">Carts</Link> |{' '}
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<h2>Welcome to the Dashboard</h2>} />
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/products" element={<ProductPage />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/carts" element={<CartPage />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
