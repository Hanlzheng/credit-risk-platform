import { useState } from 'react'
import { predictRisk } from '../api/client'

function ApplyPage() {
  const [form, setForm] = useState({
    annual_income: '',
    debt_to_income: '',
    credit_history_months: '',
    num_late_payments: '',
    loan_amount: ''
  })
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const response = await predictRisk({
        annual_income: parseFloat(form.annual_income),
        debt_to_income: parseFloat(form.debt_to_income),
        credit_history_months: parseInt(form.credit_history_months),
        num_late_payments: parseInt(form.num_late_payments),
        loan_amount: parseFloat(form.loan_amount)
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto px-4 py-10">

        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-semibold text-gray-800">Credit Risk Assessment</h1>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-500 hover:text-red-500 transition-colors"
          >
            Logout
          </button>
        </div>

        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8 mb-6">
          <h2 className="text-base font-medium text-gray-700 mb-6">Loan Application Details</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-500 mb-1 block">Annual Income ($)</label>
              <input
                type="number"
                name="annual_income"
                value={form.annual_income}
                onChange={handleChange}
                placeholder="e.g. 60000"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-400"
              />
            </div>

            <div>
              <label className="text-sm text-gray-500 mb-1 block">Loan Amount ($)</label>
              <input
                type="number"
                name="loan_amount"
                value={form.loan_amount}
                onChange={handleChange}
                placeholder="e.g. 15000"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-400"
              />
            </div>

            <div>
              <label className="text-sm text-gray-500 mb-1 block">Debt to Income Ratio (0-1)</label>
              <input
                type="number"
                name="debt_to_income"
                value={form.debt_to_income}
                onChange={handleChange}
                placeholder="e.g. 0.35"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-400"
              />
            </div>

            <div>
              <label className="text-sm text-gray-500 mb-1 block">Credit History (months)</label>
              <input
                type="number"
                name="credit_history_months"
                value={form.credit_history_months}
                onChange={handleChange}
                placeholder="e.g. 48"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-400"
              />
            </div>

            <div className="col-span-2">
              <label className="text-sm text-gray-500 mb-1 block">Number of Late Payments</label>
              <input
                type="number"
                name="num_late_payments"
                value={form.num_late_payments}
                onChange={handleChange}
                placeholder="e.g. 2"
                className="w-full border border-gray-200 rounded-lg px-4 py-2.5 text-sm outline-none focus:border-blue-400"
              />
            </div>
          </div>

          {error && <p className="text-red-500 text-sm mt-4">{error}</p>}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-2.5 rounded-lg transition-colors"
          >
            {loading ? 'Analyzing...' : 'Get Risk Assessment'}
          </button>
        </div>

        {result && (
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
            <h2 className="text-base font-medium text-gray-700 mb-4">Assessment Result</h2>
            <div className="flex items-center gap-4">
                <div className="text-4xl font-semibold text-gray-800">
                    {(result.confidence * 100).toFixed(1)}%
                </div>
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                    result.risk_tier === 'Low'
                        ? 'bg-green-100 text-green-700'
                        : result.risk_tier === 'Medium'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-red-100 text-red-700'
                }`}>
                    {result.risk_tier} Risk
                </div>
            </div>
            <p className="text-sm text-gray-400 mt-2">Confidence score</p>
          </div>
        )}

      </div>
    </div>
  )
}

export default ApplyPage