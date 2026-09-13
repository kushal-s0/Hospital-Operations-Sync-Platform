import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../../services/api';
import './Login.css';

const FEATURES = [
  { title: 'Live bed availability', text: 'Ward-by-ward occupancy that updates as patients move.' },
  { title: 'Smart OPD queue', text: 'ML-predicted wait times keep patient flow moving.' },
  { title: 'Forecasted inventory', text: 'Usage and weather-aware stock alerts before you run out.' },
];

const CrossMark = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M9.5 3h5a1 1 0 0 1 1 1v4.5H20a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-4.5V20a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1v-4.5H4a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1h4.5V4a1 1 0 0 1 1-1Z" />
  </svg>
);

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [errorKey, setErrorKey] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(credentials.username, credentials.password);

      // Store tokens in localStorage
      localStorage.setItem('access_token', response.access);
      localStorage.setItem('refresh_token', response.refresh);
      localStorage.setItem('user', JSON.stringify(response.user));

      // Redirect based on user role
      const userRole = response.user?.role;
      if (userRole === 'Receptionist') {
        navigate('/receptionist-dashboard');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
      setErrorKey((key) => key + 1); // replays the shake animation
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-bg" aria-hidden="true">
        <span className="login-blob blob-1" />
        <span className="login-blob blob-2" />
        <span className="login-blob blob-3" />
        <span className="login-grid" />
      </div>

      <div className="login-shell">
        {/* Brand showcase */}
        <aside className="login-showcase">
          <Link to="/" className="login-brand">
            <span className="login-brand-mark"><CrossMark /></span>
            <span className="login-brand-name">HealthCare Plus</span>
          </Link>

          <div className="showcase-body">
            <span className="showcase-eyebrow">
              <span className="showcase-dot" aria-hidden="true" />
              Staff portal
            </span>
            <h2 className="showcase-title">
              Every ward, bed and queue — <span>in perfect sync.</span>
            </h2>
            <p className="showcase-text">
              One real-time command centre for doctors, nurses, pharmacists and front-desk teams.
            </p>

            <div className="showcase-monitor" aria-hidden="true">
              <svg viewBox="0 0 400 80" preserveAspectRatio="none">
                <path d="M0 40 H110 L124 40 L132 20 L142 62 L152 8 L162 72 L172 40 H250 L262 40 L268 30 L276 50 L282 40 H400" />
              </svg>
            </div>

            <ul className="showcase-features">
              {FEATURES.map((feature, index) => (
                <li key={feature.title} style={{ '--i': index }}>
                  <span className="feature-check" aria-hidden="true">
                    <svg width="14" height="14" viewBox="0 0 20 20" fill="none">
                      <path d="M4.5 10.5L8 14L15.5 6.5" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </span>
                  <div>
                    <strong>{feature.title}</strong>
                    <span>{feature.text}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <p className="showcase-footer">Hospital Operations Sync Platform</p>
        </aside>

        {/* Sign-in form */}
        <main className="login-panel">
          <div className="login-card">
            <Link to="/" className="login-back">
              <svg width="16" height="16" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M12.5 15L7.5 10L12.5 5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Back to website
            </Link>

            <div className="login-header">
              <span className="login-mark"><CrossMark /></span>
              <h1>Welcome back</h1>
              <p>Sign in to the Hospital Information System</p>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              {error && (
                <div key={errorKey} className="login-error" role="alert">
                  <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                    <circle cx="10" cy="10" r="7.5" stroke="currentColor" strokeWidth="1.6"/>
                    <path d="M10 6.5V10.5M10 13.5H10.01" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                  {error}
                </div>
              )}

              <div className="login-field">
                <label htmlFor="username">Username</label>
                <div className="login-input-wrap">
                  <svg className="login-input-icon" width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                    <circle cx="10" cy="6.5" r="3.25" stroke="currentColor" strokeWidth="1.6"/>
                    <path d="M3.75 17c0-3.2 2.8-5.25 6.25-5.25S16.25 13.8 16.25 17" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
                  </svg>
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={credentials.username}
                    onChange={handleChange}
                    required
                    autoFocus
                    autoComplete="username"
                    disabled={loading}
                    placeholder="Enter your username"
                  />
                </div>
              </div>

              <div className="login-field">
                <label htmlFor="password">Password</label>
                <div className="login-input-wrap">
                  <svg className="login-input-icon" width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                    <rect x="4" y="8.5" width="12" height="8.5" rx="2" stroke="currentColor" strokeWidth="1.6"/>
                    <path d="M6.75 8.5V6.25a3.25 3.25 0 0 1 6.5 0V8.5" stroke="currentColor" strokeWidth="1.6"/>
                  </svg>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={credentials.password}
                    onChange={handleChange}
                    required
                    autoComplete="current-password"
                    disabled={loading}
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    className="login-toggle-password"
                    onClick={() => setShowPassword((show) => !show)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? (
                      <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                        <path d="M3 3L17 17M8.2 8.3a2.5 2.5 0 0 0 3.5 3.5M6 5.6C3.9 6.9 2.5 10 2.5 10s2.75 5.5 7.5 5.5c1.5 0 2.8-.5 3.9-1.2M9 4.6c.3 0 .7-.1 1-.1 4.75 0 7.5 5.5 7.5 5.5s-.6 1.2-1.7 2.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
                      </svg>
                    ) : (
                      <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                        <path d="M2.5 10S5.25 4.5 10 4.5 17.5 10 17.5 10 14.75 15.5 10 15.5 2.5 10 2.5 10Z" stroke="currentColor" strokeWidth="1.6"/>
                        <circle cx="10" cy="10" r="2.5" stroke="currentColor" strokeWidth="1.6"/>
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="login-button"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="login-spinner" aria-hidden="true" />
                    Signing in…
                  </>
                ) : (
                  <>
                    Sign In
                    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                      <path d="M4 10H16M11 5L16 10L11 15" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </>
                )}
              </button>
            </form>

            <p className="login-hint">
              Hint: Use test credentials provided by administrator
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Login;
