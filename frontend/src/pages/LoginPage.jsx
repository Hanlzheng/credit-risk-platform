import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser, registerUser } from '../api/client'

function LoginPage() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    try {
        if (isLogin){
           const response = await loginUser({ email, password })
           localStorage.setItem('token', response.data.token)
           window.location.href = '\apply'
        } else {
            await registerUser({ email, password })
            setIsLogin(true)
            setError('')
            alert('Account creted! Please log in.')
        }
    } catch (err) {
      setError(err.response?.data?.message || 'Something went wrong')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 w-full max-w-md">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">
          {isLogin ? 'Welcome back' : 'Create account'}
        </h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border border-gray-200 rounded-lg px-4 py-2.5 mb-4 text-sm outline-none focus:border-blue-400"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border border-gray-200 rounded-lg px-4 py-2.5 mb-4 text-sm outline-none focus:border-blue-400"
        />

        {error && (
          <p className="text-red-500 text-sm mb-4">{error}</p>
        )}

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg transition-colors"
        >
          {isLogin ? 'Login' : 'Register'}
        </button>

        <p
          onClick={() => setIsLogin(!isLogin)}
          className="text-center text-sm text-blue-500 hover:text-blue-600 mt-4 cursor-pointer"
        >
          {isLogin ? "Don't have an account? Register" : 'Already have an account? Login'}
        </p>
      </div>
    </div>
  )
}

export default LoginPage