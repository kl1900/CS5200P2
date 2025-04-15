import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom";

import { jwtDecode } from "jwt-decode"

function CartPage() {
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [status, setStatus] = useState("")
  const [form, setForm] = useState({
    payment_method: "credit_card",
    billing_address: {
      name: "", street: "", city: "", state: "", zip: "", country: ""
    },
    shipping_address: {
      name: "", street: "", city: "", state: "", zip: "", country: ""
    }
  })
  const API_BASE = 'http://localhost:8000'

  const token = localStorage.getItem("jwt")
  let userId = null
  try {
    userId = token ? jwtDecode(token).user_id : null
  } catch (err) {
    console.error("Invalid token")
    setError("Invalid session")
  }

  useEffect(() => {
    if (!userId) {
      setError("User not logged in")
      setLoading(false)
      return
    }

    fetch(`${API_BASE}/carts/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.ok ? res.json() : Promise.reject("Failed to load cart"))
      .then(data => {
        if (data && data.items) setCart(data)
        else setError("No active cart found")
        setLoading(false)
      })
      .catch(err => {
        console.error("Fetch error:", err)
        setError("Failed to load cart")
        setLoading(false)
      })
  }, [userId])

  const handleChange = (section, field, value) => {
    setForm(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }))
  }
  const navigate = useNavigate();
  
  const handleCheckout = async () => {
    setStatus("processing")
    try {
      const res = await fetch(`${API_BASE}/carts/checkout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          payment_method: form.payment_method,
          billing_address: form.billing_address,
          shipping_address: form.shipping_address
        })
      })

      const result = await res.json()
      if (res.ok) {
        setStatus("success")
        setCart(null)
        alert("Checkout successful!")
        navigate("/orders");
      } else {
        console.error("Checkout failed:", result)
        setStatus(`error: ${result.error || "Unexpected error"}`)
      }
    } catch (err) {
      console.error("Checkout failed:", err)
      setStatus("error: checkout failed")
    }
  }

  const handleRemoveItem = async (product_id) => {
    try {
      const res = await fetch(`${API_BASE}/carts/remove`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ product_id })
      })

      if (res.ok) {
        setCart(prev => ({
          ...prev,
          items: prev.items.filter(item => item.product_id !== product_id)
        }))
      } else {
        console.error("Failed to remove item")
      }
    } catch (err) {
      console.error("Error:", err)
    }
  }

  if (loading) return <p className="text-center my-4">Loading cart...</p>
  if (error) return <p className="text-center text-danger">{error}</p>
  if (!cart) return <p className="text-center text-muted">No cart available.</p>

  const total = cart.items.reduce((sum, item) => sum + item.quantity * item.price, 0)

  return (
    <div className="container py-4">
      <div className="card shadow-sm">
        <div className="card-header bg-primary text-white">
          <h3 className="mb-0">🛒 Your Cart</h3>
        </div>
        <div className="card-body">
          {cart.items.length === 0 ? (
            <p className="text-muted">Your cart is empty.</p>
          ) : (
            <>
              <table className="table table-bordered table-hover mb-4">
                <thead className="table-light">
                  <tr>
                    <th>Product</th>
                    <th className="text-center">Qty</th>
                    <th className="text-center">Price</th>
                    <th className="text-end">Subtotal</th>
                    <th className="text-center">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {cart.items.map((item, idx) => (
                    <tr key={idx}>
                      <td>{item.name}</td>
                      <td className="text-center">{item.quantity}</td>
                      <td className="text-center">${item.price.toFixed(2)}</td>
                      <td className="text-end">${(item.quantity * item.price).toFixed(2)}</td>
                      <td className="text-center">
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleRemoveItem(item.product_id)}
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <h5 className="text-end">Total: ${total.toFixed(2)}</h5>
            </>
          )}

          <div className="my-4">
            <label className="form-label fw-semibold">Payment Method</label>
            <select
              value={form.payment_method}
              onChange={(e) => setForm(prev => ({ ...prev, payment_method: e.target.value }))}
              className="form-select"
            >
              <option value="credit_card">Credit Card</option>
              <option value="paypal">PayPal</option>
            </select>
          </div>

          {["billing_address", "shipping_address"].map(section => (
            <div key={section} className="mb-4">
              <h6 className="fw-bold text-capitalize">{section.replace("_", " ")}</h6>
              <div className="row g-2">
                {["name", "street", "city", "state", "zip", "country"].map(field => (
                  <div key={field} className="col-md-6">
                    <input
                      type="text"
                      className="form-control"
                      placeholder={field}
                      value={form[section][field]}
                      onChange={(e) => handleChange(section, field, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}

          <div className="text-end">
            <button
              onClick={handleCheckout}
              disabled={status === "processing"}
              className="btn btn-success"
            >
              {status === "processing" ? "Processing..." : "Checkout"}
            </button>
          </div>

          {status && (
            <p className="mt-3 text-center text-secondary">Status: {status}</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default CartPage
