import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();

      if (!res.ok) throw new Error(data.error);

      localStorage.setItem('token', data.token);
      navigate('/products');

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "400px", margin: "auto" }}>
      <h2>Login</h2>
      {error && <div style={{color: 'red'}}>{error}</div>}
      <form onSubmit={handleLogin}>
        <input placeholder="Email" type="email" required 
          value={email} onChange={e => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" required 
          value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
