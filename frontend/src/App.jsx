// src/App.jsx
import { Routes, Route, Link } from 'react-router-dom'
import ProductPage from './pages/Products'
import ProductDetail from './components/ProductDetail'
import LoginPage from "./pages/LoginPage"
import ProtectedRoute from './components/ProtectedRoute'
import CartPage from './pages/Carts'
import Analytics from './pages/Analytics'
import OrdersPage from './pages/OrdersPage'

const isLoggedIn = !!localStorage.getItem("jwt")

const logout = () => {
  localStorage.removeItem("jwt")
  window.location.href = "/login"
}

function App() {
  return (
    <div>
      <div>
      <nav style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#1a1a1a' }}>
        <Link to="/">Home</Link> |{' '}
        <Link to="/products">Products</Link> |{' '}
        <Link to="/carts">Carts</Link> |{' '}
        <Link to="/orders">Orders</Link> |{' '}
        <Link to="/analytics">Analytics</Link> {' '}
        {!isLoggedIn && (
          <>
            {' | '}
            <Link to="/login">Login</Link>
          </>
        )}
        {isLoggedIn && (
          <>
            {' | '}
            <Link
              style={{color: 'white'}}
              onClick={logout} >

              Logout
            </Link>
          </>
        )}
      </nav>
      </div>

      <div style={{ padding: '0 1rem' }}>
        <Routes>
          <Route path="/" element={<h2>Welcome to the Dashboard</h2>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/products" element={<ProtectedRoute><ProductPage /> </ProtectedRoute>} />
          <Route path="/products/:id" element={<ProtectedRoute> <ProductDetail /> </ProtectedRoute>}  />
          <Route path="/carts" element={<ProtectedRoute> <CartPage /> </ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute> <OrdersPage /> </ProtectedRoute>} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </div>
    </div>
  )
}

export default App