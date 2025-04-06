import { useState } from "react"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [token, setToken] = useState("")
  const [error, setError] = useState("")

  const handleLogin = async () => {
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      })

      const data = await res.json()
      if (res.ok) {
        setToken(data.token)
        localStorage.setItem("jwt", data.token)
        setError("")
        alert("Logged in successfully!")
      } else {
        setError(data.error || "Login failed")
      }
    } catch (err) {
      setError("Server error")
    }
  }

  return (
    <div className="p-4 max-w-sm mx-auto">
      <h2 className="text-xl font-bold mb-2">Login</h2>
      <input
        type="email"
        className="w-full border p-2 mb-2"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
      >
        Login
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  )
}
