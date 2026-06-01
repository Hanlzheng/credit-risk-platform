import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import ApplyPage from './pages/ApplyPage'

function App() {
  const token = localStorage.getItem('token')

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
          <Route 
            path="/apply"
            element={token ? <ApplyPage /> : <Navigate to="/" />}
          />
      </Routes>
    </BrowserRouter>
  )
}

export default App