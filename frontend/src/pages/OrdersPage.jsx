import { useState, useEffect } from "react"
import { jwtDecode } from "jwt-decode"

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const API_BASE = 'http://localhost:8000/api'

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

    fetch(`${API_BASE}/orders/?user_id=${userId}`)
      .then(res => res.ok ? res.json() : Promise.reject("Failed to fetch orders"))
      .then(data => {
        setOrders(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Fetch error:", err)
        setError("Failed to load orders")
        setLoading(false)
      })
  }, [userId])

  if (loading) return <p className="text-center my-4">Loading orders...</p>
  if (error) return <p className="text-center text-danger">{error}</p>
  if (orders.length === 0) return <p className="text-center text-muted">No orders found.</p>

  return (
    <div className="container py-4">
      <h2 className="text-center mb-5 fw-bold"><span role="img" aria-label="box">📦</span> Order History</h2>

      {orders.map((order) => (
        <div key={order.order_id} className="card mb-4 shadow-sm">
          <div className="card-header bg-primary text-white">
            <h5 className="mb-0">Order <strong>#{order.order_id}</strong></h5>
          </div>
          <div className="card-body">
            <p className="mb-1"><strong>Submitted:</strong> {new Date(order.submission_date).toLocaleString()}</p>
            <p className="mb-3"><strong>Payment Status:</strong> <span className="badge bg-success">{order.payment_status}</span></p>

            <table className="table table-bordered table-hover table-sm mb-4">
              <thead className="table-light">
                <tr>
                  <th>Product</th>
                  <th className="text-center">Qty</th>
                  <th className="text-center">Price</th>
                  <th className="text-end">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {order.items.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.name}</td>
                    <td className="text-center">{item.quantity}</td>
                    <td className="text-center">${item.unit_price.toFixed(2)}</td>
                    <td className="text-end">${item.subtotal.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="d-flex justify-content-end mb-4">
              <div className="text-end">
                <p><strong>Subtotal:</strong> ${order.subtotal.toFixed(2)}</p>
                <p><strong>Tax:</strong> ${order.tax.toFixed(2)}</p>
                <p><strong>Shipping Fee:</strong> ${order.shipping_fee.toFixed(2)}</p>
                <p className="fs-5 fw-bold">Total: ${order.total.toFixed(2)}</p>
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <h6 className="fw-bold">Billing Address</h6>
                <p className="mb-0">{order.billing_address.name}</p>
                <p className="mb-0">{order.billing_address.street}</p>
                <p className="mb-0">{order.billing_address.city}, {order.billing_address.state} {order.billing_address.zip}</p>
                <p className="mb-0">{order.billing_address.country}</p>
              </div>
              <div className="col-md-6">
                <h6 className="fw-bold">Shipping Address</h6>
                <p className="mb-0">{order.shipping_address.name}</p>
                <p className="mb-0">{order.shipping_address.street}</p>
                <p className="mb-0">{order.shipping_address.city}, {order.shipping_address.state} {order.shipping_address.zip}</p>
                <p className="mb-0">{order.shipping_address.country}</p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
