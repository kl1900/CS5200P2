import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getUserRole } from '../utils/auth'

function UsersPage() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const API_BASE = 'http://localhost:8000/users/'

  const role = getUserRole() // e.g., 'admin', 'seller', 'buyer', etc.

  // Helper to get Authorization headers
  const getAuthHeaders = () => {
    const token = localStorage.getItem("jwt")
    return {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    }
  }

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const res = await fetch(API_BASE, {
        headers: getAuthHeaders()
      })
      if (!res.ok) {
        throw new Error(`Error fetching users: ${res.statusText}`)
      }
      const data = await res.json()
      setUsers(data)
      setError(null)
    } catch (err) {
      console.error("Failed to fetch users:", err)
      setError("Error loading users. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

// Handle deleting a user by ID
const handleDelete = async (userId) => {
    if (!window.confirm('Delete this user?')) return

    try {
        const res = await fetch(`${API_BASE}/${userId}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
        })

        if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.error || 'Failed to delete')
        }

        // If successful, re-fetch the updated user list
        fetchUsers()
        setError(null)
    } catch (err) {
        console.error('Failed to delete user:', err)
        setError(err.message || 'Error deleting user. Please try again.')
    }
    }
    
  if (loading) return <div>Loading users...</div>
  if (error)   return <div style={{ color: 'red' }}>{error}</div>

  return (
    <div className="container">
      <h1 className="mt-4 mb-4">Users List</h1>
          {role !== 'admin' ? (
            <p className="text-danger">You do not have permission to view users.</p>
          ) : (
     

      <table className="table table-bordered">
        <thead className="table-light">
          <tr>
            <th>User ID</th>
            <th>Email</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Role</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.email}</td>
              <td>{user.name}</td>
              <td>{user.phone}</td>
              <td>{user.roles}</td>
              <td>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(user.user_id)}
                  >
                    Delete
                  </button>
                </td>
            </tr>
          ))}
        </tbody>
      </table>)}
    </div>
  )
}

export default UsersPage
