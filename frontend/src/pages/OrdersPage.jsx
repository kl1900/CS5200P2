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

  if (loading) return <p>Loading orders...</p>
  if (error) return <p className="text-red-500">{error}</p>
  if (orders.length === 0) return <p>No orders found.</p>

  return (
    <div className="p-4 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">📦 Your Orders</h2>
      {orders.map((order) => (
        <div key={order.order_id} className="border rounded mb-6 p-4 bg-white shadow-sm">
          <h3 className="text-lg font-semibold mb-2">Order ID: {order.order_id}</h3>
          <p className="text-sm text-gray-600 mb-1">Submitted: {new Date(order.submission_date).toLocaleString()}</p>
          <p className="text-sm text-gray-600 mb-3">Payment Status: {order.payment_status}</p>

          <table className="w-full text-sm border mb-4">
            <thead>
              <tr className="bg-gray-100">
                <th className="text-left p-2">Product</th>
                <th className="text-center p-2">Qty</th>
                <th className="text-center p-2">Unit Price</th>
                <th className="text-right p-2">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              {order.items.map((item, idx) => (
                <tr key={idx} className="border-t">
                  <td className="p-2">{item.name}</td>
                  <td className="text-center p-2">{item.quantity}</td>
                  <td className="text-center p-2">${item.unit_price.toFixed(2)}</td>
                  <td className="text-right p-2">${item.subtotal.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="text-sm text-right mb-2">
            <p>Subtotal: ${order.subtotal.toFixed(2)}</p>
            <p>Tax: ${order.tax.toFixed(2)}</p>
            <p>Shipping Fee: ${order.shipping_fee.toFixed(2)}</p>
            <p className="font-semibold text-base">Total: ${order.total.toFixed(2)}</p>
          </div>

          <div className="text-sm text-gray-700 mt-4">
            <div className="mb-2">
              <h4 className="font-medium">Billing Address:</h4>
              <p>{order.billing_address.name}</p>
              <p>{order.billing_address.street}</p>
              <p>{order.billing_address.city}, {order.billing_address.state} {order.billing_address.zip}</p>
              <p>{order.billing_address.country}</p>
            </div>
            <div>
              <h4 className="font-medium">Shipping Address:</h4>
              <p>{order.shipping_address.name}</p>
              <p>{order.shipping_address.street}</p>
              <p>{order.shipping_address.city}, {order.shipping_address.state} {order.shipping_address.zip}</p>
              <p>{order.shipping_address.country}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
