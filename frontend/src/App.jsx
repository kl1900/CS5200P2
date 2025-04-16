// src/App.jsx
import { Routes, Route, Link } from 'react-router-dom'
import ProductPage from './pages/Products'
import ProductDetail from './components/ProductDetail'
import LoginPage from "./pages/LoginPage"
import ProtectedRoute from './components/ProtectedRoute'
import CartPage from './pages/Carts'
import Analytics from './pages/Analytics'
import OrdersPage from './pages/OrdersPage'
import UsersPage from './pages/Users.jsx'

const isLoggedIn = !!localStorage.getItem("jwt")

const logout = () => {
  localStorage.removeItem("jwt")
  window.location.href = "/login"
}

function App() {
  return (
    <div>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
        <div className="container-fluid">
          <Link className="navbar-brand fw-bold" to="/">Dashboard</Link>
          <div className="collapse navbar-collapse ">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item"><Link className="nav-link" to="/products">Products</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/carts">Carts</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/orders">Orders</Link></li>
              <li className="nav-item"><Link className="nav-link" to="/users">Users</Link></li>
            </ul>
            <ul className="navbar-nav">
              {!isLoggedIn && (
                <li className="nav-item"><Link className="nav-link" to="/login">Login</Link></li>
              )}
              {isLoggedIn && (
                <li className="nav-item">
                  <button className="btn btn-sm btn-outline-light ms-2" onClick={logout}>
                    Logout
                  </button>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Analytics />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/products" element={<ProtectedRoute><ProductPage /></ProtectedRoute>} />
          <Route path="/products/:id" element={<ProtectedRoute><ProductDetail /></ProtectedRoute>} />
          <Route path="/carts" element={<ProtectedRoute><CartPage /></ProtectedRoute>} />
          <Route path="/orders" element={<ProtectedRoute><OrdersPage /></ProtectedRoute>} />
          <Route path="/users" element={<ProtectedRoute><UsersPage /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  )
}

export default App
