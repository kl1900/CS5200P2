// src/App.jsx
import { Routes, Route, Link } from 'react-router-dom'
import ProductPage from './pages/Products'
import ProductDetail from './components/ProductDetail'
import LoginPage from "./pages/LoginPage"
import CartPage from './pages/Carts'

function App() {
  return (
    <div>
      <nav style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#1a1a1a' }}>
        <Link to="/">Home</Link> |{' '}
        <Link to="/products">Products</Link> |{' '}
        <Link to="/carts">Carts</Link>
        <Link to="/login">Login</Link> 
      </nav>
      <div style={{ padding: '0 1rem' }}>
        <Routes>
          <Route path="/" element={<h2>Welcome to the Dashboard</h2>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/products" element={<ProductPage />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/carts" element={<CartPage />} />
        </Routes>
      </div>
    </div>
  )
}

export default App