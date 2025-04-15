import { useEffect, useState } from "react"

function Analytics() {
  const [topProducts, setTopProducts] = useState([])
  const [activeBuyers, setActiveBuyers] = useState([])
  const [revenueBySeller, setRevenueBySeller] = useState([])
  const [mostCarted, setMostCarted] = useState([])
  const [ordersByDate, setOrdersByDate] = useState([])

  useEffect(() => {
    fetch("http://localhost:8000/analytics/top-products")
      .then(res => res.json())
      .then(setTopProducts)

    fetch("http://localhost:8000/analytics/most-active-buyers")
      .then(res => res.json())
      .then(setActiveBuyers)

    fetch("http://localhost:8000/analytics/revenue-by-seller")
      .then(res => res.json())
      .then(setRevenueBySeller)

    fetch("http://localhost:8000/analytics/most-carted-products")
      .then(res => res.json())
      .then(setMostCarted)

    fetch("http://localhost:8000/analytics/orders-last-7-days")
      .then(res => res.json())
      .then(setOrdersByDate)
  }, [])

  return (
    <div className="container py-4">
      <h1 className="mb-4 text-center fw-bold">📊 Analytics Dashboard</h1>

      <div className="row g-4">
        <div className="col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header bg-primary text-white">
              Top-Selling Products
            </div>
            <div className="card-body">
              <ul className="list-group list-group-flush">
                {topProducts.map((p, i) => (
                  <li key={i} className="list-group-item d-flex justify-content-between">
                    <span>{p.productName}</span>
                    <span className="text-muted">{p.totalSold} sold</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header bg-success text-white">
              Most Active Buyers
            </div>
            <div className="card-body">
              <ul className="list-group list-group-flush">
                {activeBuyers.map((b, i) => (
                  <li key={i} className="list-group-item d-flex justify-content-between">
                    <span>{b.buyerName}</span>
                    <span className="text-muted">{b.totalOrders} orders</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header bg-warning text-dark">
              Revenue by Seller
            </div>
            <div className="card-body">
              <ul className="list-group list-group-flush">
                {revenueBySeller.map((s, i) => (
                  <li key={i} className="list-group-item d-flex justify-content-between">
                    <span>{s.sellerName}</span>
                    <span className="text-muted">${s.totalRevenue.toFixed(2)}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card h-100 shadow-sm">
            <div className="card-header bg-info text-white">
              Most Carted Products
            </div>
            <div className="card-body">
              <ul className="list-group list-group-flush">
                {mostCarted.map((c, i) => (
                  <li key={i} className="list-group-item d-flex justify-content-between">
                    <span>{c.productName}</span>
                    <span className="text-muted">{c.cartCount} carts</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="col-12">
          <div className="card shadow-sm">
            <div className="card-header bg-dark text-white">
              Orders in the Last 7 Days
            </div>
            <div className="card-body">
              <ul className="list-group list-group-flush">
                {ordersByDate.map((d, i) => (
                  <li key={i} className="list-group-item d-flex justify-content-between">
                    <span>{d._id}</span>
                    <span className="text-muted">{d.count} orders</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics
