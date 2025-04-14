import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

function Analytics() {
  const [topProducts, setTopProducts] = useState([]);
  const [activeBuyers, setActiveBuyers] = useState([]);
  const [revenueBySeller, setRevenueBySeller] = useState([]);
  const [mostCarted, setMostCarted] = useState([]);
  const [ordersByDate, setOrdersByDate] = useState([]);

  useEffect(() => {
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
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>📊 Analytics Dashboard</h1>

      <section>
        <h2>Top-Selling Products</h2>
        <ul>
          {topProducts.map((p, i) => (
            <li key={i}>{p.productName} — {p.totalSold} sold</li>
          ))}
        </ul>
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

      <section>
        <h2>Most Active Buyers</h2>
        <ul>
          {activeBuyers.map((b, i) => (
            <li key={i}>{b.buyerName} — {b.totalOrders} orders</li>
          ))}
        </ul>
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

      <section>
        <h2>Total Revenue by Seller</h2>
        <ul>
          {revenueBySeller.map((s, i) => (
            <li key={i}>{s.sellerName} — ${s.totalRevenue.toFixed(2)}</li>
          ))}
        </ul>
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

      <section>
        <h2>Most Carted Products</h2>
        <ul>
          {mostCarted.map((c, i) => (
            <li key={i}>{c.productName} — {c.cartCount} carts</li>
          ))}
        </ul>
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

      <section>
        <h2>Orders in the Last 7 Days</h2>
        <ul>
          {ordersByDate.map((d, i) => (
            <li key={i}>{d._id} — {d.count} orders</li>
          ))}
        </ul>
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
  );
}

export default Analytics;
