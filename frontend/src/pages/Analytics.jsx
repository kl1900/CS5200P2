import { useEffect, useState } from "react";

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
      </section>

      <section>
        <h2>Most Active Buyers</h2>
        <ul>
          {activeBuyers.map((b, i) => (
            <li key={i}>{b.buyerName} — {b.totalOrders} orders</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Total Revenue by Seller</h2>
        <ul>
          {revenueBySeller.map((s, i) => (
            <li key={i}>{s.sellerName} — ${s.totalRevenue.toFixed(2)}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Most Carted Products</h2>
        <ul>
          {mostCarted.map((c, i) => (
            <li key={i}>{c.productName} — {c.cartCount} carts</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Orders in the Last 7 Days</h2>
        <ul>
          {ordersByDate.map((d, i) => (
            <li key={i}>{d._id} — {d.count} orders</li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default Analytics;
