import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle login/register state
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData(e.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const password = formData.get('password');
    const phone_number = formData.get('phone_number');

    try {
      const apiUrl = isLogin
        ? 'http://103.189.140.199:8000/api/auth/login'
        : 'http://103.189.140.199:8000/api/auth/register';

      const requestData = isLogin
        ? { email, password }
        : { name, email, password, phone_number };

      const response = await axios.post(apiUrl, requestData);

      if (isLogin) {
        // Login successful, save token and user info
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('user_name', response.data.user_name);
        navigate('/dashboard');
      } else {
        // Registration successful, switch to login mode
        alert('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed, please try again');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">
          {isLogin ? 'Welcome Back' : 'Create Account'}
        </h2>

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleAuth} className="space-y-4">
          {!isLogin && (
            <input
              name="name"
              type="text"
              placeholder="Full Name"
              className="w-full border p-2 rounded"
              required
            />
          )}
          {!isLogin && (
            <input
              name="phone_number"
              type="tel"
              placeholder="Phone Number (Optional)"
              className="w-full border p-2 rounded"
            />
          )}
          <input
            name="email"
            type="email"
            placeholder="Email Address"
            className="w-full border p-2 rounded"
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            className="w-full border p-2 rounded"
            required
          />

          <button
            type="submit"
            className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-blue-600 cursor-pointer"
          onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Sign In"}
        </p>
      </div>
    </div>
  );
};

export default AuthPage;