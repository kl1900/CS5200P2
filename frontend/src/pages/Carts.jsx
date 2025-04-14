import { useState, useEffect } from "react"
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

  // Decode user_id from JWT
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
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.ok ? res.json() : Promise.reject("Failed to load cart"))
      .then(data => {
        if (data && data.items) {
          setCart(data)  // change to array
        } else {
          setError("No active cart found")
        }
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

  const handleCheckout = async () => {
    setStatus("processing")
    try {
      const res = await fetch(`${API_BASE}/checkout/`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" ,
          Authorization: `Bearer ${token}`
        },
        
        body: JSON.stringify({
          user_id: cart.user_id,
          cart_id: cart.cart_id,
          payment_method: form.payment_method,
          billing_address: form.billing_address,
          shipping_address: form.shipping_address
        })
      })

      const result = await res.json()
      if (res.ok) {
        setStatus("success")
      } else {
        setStatus(`error: ${result.error}`)
      }
    } catch (err) {
      setStatus("error: checkout failed")
    }
  }

  if (loading) return <p>Loading cart...</p>
  if (error) return <p className="text-red-500">{error}</p>
  if (!cart) return <p>No cart available.</p>

  const total = cart.items.reduce((sum, item) => sum + item.quantity * item.price, 0)

  const handleRemoveItem = async (product_id) => {
    try {
      const res = await fetch("http://localhost:8000/carts/remove", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("jwt")}`
        },
        body: JSON.stringify({ product_id })
      });

      if (res.ok) {
        // Refresh cart
        const updatedCart = await res.json();
        setCart((prev) => ({
          ...prev,
          items: prev.items.filter(item => item.product_id !== product_id)
        }));
      } else {
        console.error("Failed to remove item");
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">🛒 Your Cart</h2>
      {cart.items.length === 0 ? (
          <p className="text-gray-600 mb-4">Your cart is empty.</p>
        ) : (
          <>
            <table className="w-full mb-4 border border-gray-200">
              <thead>
                <tr className="bg-gray-100">
                  <th className="text-left p-2">Product</th>
                  <th className="text-center p-2">Qty</th>
                  <th className="text-center p-2">Price</th>
                  <th className="text-right p-2">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {cart.items.map((item, idx) => (
                  <tr key={idx} className="border-t">
                    <td className="p-2">{item.name}</td>
                    <td className="text-center p-2">{item.quantity}</td>
                    <td className="text-center p-2">${item.price.toFixed(2)}</td>
                    <td className="text-right p-2">
                      ${(item.quantity * item.price).toFixed(2)}
                      <button onClick={() => handleRemoveItem(item.product_id)} className="ml-2 text-red-500">Remove</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <p className="font-semibold mb-4 text-right">
              Total: $
              {cart.items.reduce(
                (sum, item) => sum + item.price * item.quantity,
                0
              ).toFixed(2)}
            </p>
          </>
        )}

      <label className="block mb-3">
        Payment Method:
        <select
          value={form.payment_method}
          onChange={(e) => setForm(prev => ({ ...prev, payment_method: e.target.value }))}
          className="block w-full border px-2 py-1 mt-1"
        >
          <option value="credit_card">Credit Card</option>
          <option value="paypal">PayPal</option>
        </select>
      </label>

      {["billing_address", "shipping_address"].map(section => (
        <div key={section} className="mb-4">
          <h4 className="font-medium capitalize">{section.replace("_", " ")}</h4>
          {["name", "street", "city", "state", "zip", "country"].map(field => (
            <input
              key={field}
              placeholder={field}
              value={form[section][field]}
              onChange={(e) => handleChange(section, field, e.target.value)}
              className="block w-full border px-2 py-1 mb-2"
            />
          ))}
        </div>
      ))}

      <button
        onClick={handleCheckout}
        disabled={status === "processing"}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        {status === "processing" ? "Processing..." : "Checkout"}
      </button>

      {status && <p className="mt-2 text-sm text-gray-700">Status: {status}</p>}
    </div>
  )
}

export default CartPage
