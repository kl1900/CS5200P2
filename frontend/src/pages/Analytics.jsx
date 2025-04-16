import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line
} from "recharts";

function Analytics() {
  const [topProducts, setTopProducts] = useState([]);
  const [activeBuyers, setActiveBuyers] = useState([]);
  const [revenueBySeller, setRevenueBySeller] = useState([]);
  const [mostCarted, setMostCarted] = useState([]);
  const [ordersByDate, setOrdersByDate] = useState([]);

  useEffect(() => {
    const fetchAllAnalytics = () => {
      fetch("http://localhost:8000/analytics/top-products")
        .then(res => res.json())
        .then(setTopProducts);
      fetch("http://localhost:8000/analytics/most-active-buyers")
        .then(res => res.json())
        .then(setActiveBuyers);
      fetch("http://localhost:8000/analytics/revenue-by-seller")
        .then(res => res.json())
        .then(setRevenueBySeller);
      fetch("http://localhost:8000/analytics/most-carted-products")
        .then(res => res.json())
        .then(setMostCarted);
      fetch("http://localhost:8000/analytics/orders-last-7-days")
        .then(res => res.json())
        .then(setOrdersByDate);
    };
  
    fetchAllAnalytics(); // first fetch immediately
  
    const intervalId = setInterval(fetchAllAnalytics, 30000); // refresh every 30 seconds
  
    return () => clearInterval(intervalId); // cleanup
  }, []);
  

  return (
    <div className="container py-4">
      <h1 className="mb-4 text-center fw-bold">📊 Analytics Dashboard</h1>

      {/* Row 1 */}
      <div className="row g-4">
        <div className="col-md-6">
          <section className="card h-100 shadow-sm">
            <div className="card-header bg-primary text-white">Top-Selling Products</div>
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
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topProducts} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="productName" interval={0} angle={-20} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="totalSold" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </section>
        </div>

        <div className="col-md-6">
          <section className="card h-100 shadow-sm">
            <div className="card-header bg-success text-white">Most Active Buyers</div>
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
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={activeBuyers} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="buyerName" interval={0} angle={-20} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="totalOrders" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </section>
        </div>
      </div>

      {/* Row 2 */}
      <div className="row g-4 mt-3">
        <div className="col-md-6">
          <section className="card h-100 shadow-sm">
            <div className="card-header bg-warning text-dark">Revenue by Seller</div>
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
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={revenueBySeller} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="sellerName" interval={0} angle={-20} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="totalRevenue" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </section>
        </div>

        <div className="col-md-6">
          <section className="card h-100 shadow-sm">
            <div className="card-header bg-info text-white">Most Carted Products</div>
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
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mostCarted} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="productName" interval={0} angle={-20} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="cartCount" fill="#ff7f7f" />
              </BarChart>
            </ResponsiveContainer>
          </section>
        </div>
      </div>

      {/* Row 3: Full-width */}
      <div className="row g-4 mt-3">
        <div className="col-12">
          <section className="card shadow-sm">
            <div className="card-header bg-dark text-white">Orders in the Last 7 Days</div>
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
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={ordersByDate} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="_id" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </section>
        </div>
      </div>
    </div>
  );
}

export default Analytics;
