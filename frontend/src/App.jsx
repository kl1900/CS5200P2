import { Routes, Route, Link } from 'react-router-dom'
import ProductPage from './pages/Products'
import CartPage from './pages/Carts'

function App() {
  return (
    <div>
      <nav style={{ marginBottom: '1rem' }}>
        <Link to="/products">Products</Link> |{' '}
        <Link to="/carts">Carts</Link>
      </nav>

      <Routes>
        <Route path="/" element={<h2>Welcome to the Dashboard</h2>} />
        <Route path="/products" element={<ProductPage />} />
        <Route path="/carts" element={<CartPage />} />
      </Routes>
    </div>
  )
}

export default App
