import { useEffect, useState } from 'react';
import jwt_decode from 'jwt-decode';
import { useNavigate } from 'react-router-dom';

export default function User() {
  const [user, setUser] = useState(null);
  const [newPassword, setNewPassword] = useState('');
  const [updateMessage, setUpdateMessage] = useState('');
  const navigate = useNavigate();

  // On mount, decode the token to get user details
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    try {
      const decoded = jwt_decode(token);
      setUser(decoded);
    } catch (error) {
      console.error('Invalid token', error);
      navigate('/login');
    }
  }, [navigate]);

  // Handle password change submission
  const handlePasswordChange = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('http://localhost:8000/change_password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ new_password: newPassword })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Password update failed');
      setUpdateMessage('Password updated successfully.');
      setNewPassword('');
    } catch (error) {
      setUpdateMessage(error.message);
    }
  };

  if (!user) return <div>Loading user data...</div>;

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h2>User Profile</h2>
      <p><strong>Name:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Role:</strong> {user.roles}</p>
      <hr />
      <h3>Change Password</h3>
      {updateMessage && <p style={{ color: updateMessage.includes('successfully') ? 'green' : 'red' }}>{updateMessage}</p>}
      <form onSubmit={handlePasswordChange}>
        <input 
          type="password" 
          placeholder="New Password" 
          required 
          value={newPassword} 
          onChange={e => setNewPassword(e.target.value)} 
          style={{ padding: '0.5rem', marginRight: '0.5rem' }}
        />
        <button type="submit" style={{ padding: '0.5rem 1rem' }}>Update Password</button>
      </form>
    </div>
  );
}
