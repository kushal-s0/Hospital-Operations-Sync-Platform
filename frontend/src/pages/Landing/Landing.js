import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppointmentBookingForm from '../../components/AppointmentBookingForm/AppointmentBookingForm';
import './Landing.css';

const Landing = () => {
  const navigate = useNavigate();
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);

  const services = [
    {
      icon: '🏥',
      title: 'Emergency Care',
      description: '24/7 emergency services with state-of-the-art facilities and experienced medical professionals.'
    },
    {
      icon: '👨‍⚕️',
      title: 'Expert Doctors',
      description: 'Board-certified specialists across all major medical disciplines for comprehensive care.'
    },
    {
      icon: '🔬',
      title: 'Advanced Diagnostics',
      description: 'Modern laboratory and imaging services for accurate and timely diagnosis.'
    },
    {
      icon: '💊',
      title: 'Pharmacy Services',
      description: 'In-house pharmacy with a wide range of medications available round the clock.'
    },
    {
      icon: '🛏️',
      title: 'Inpatient Care',
      description: 'Comfortable private and semi-private rooms with personalized nursing care.'
    },
    {
      icon: '🩺',
      title: 'Outpatient Services',
      description: 'Convenient OPD services with minimal wait times and online appointment booking.'
    }
  ];

  const stats = [
    { number: '50+', label: 'Expert Doctors' },
    { number: '10K+', label: 'Happy Patients' },
    { number: '24/7', label: 'Emergency Care' },
    { number: '15+', label: 'Departments' }
  ];

  const departments = [
    'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
    'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT'
  ];

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="landing-nav">
        <div className="nav-container">
          <div className="nav-logo">
            <span className="logo-icon">🏥</span>
            <span className="logo-text">HealthCare Plus</span>
          </div>
          <div className="nav-links">
            <a href="#services">Services</a>
            <a href="#departments">Departments</a>
            <a href="#about">About Us</a>
            <a href="#contact">Contact</a>
          </div>
          <div className="nav-actions">
            <button className="btn-secondary" onClick={() => navigate('/login')}>
              Staff Login
            </button>
            <button className="btn-primary" onClick={() => setShowAppointmentForm(true)}>
              Book Appointment
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Your Health, <span className="highlight">Our Priority</span></h1>
            <p>
              Experience world-class healthcare services with compassionate care. 
              Our team of expert doctors and modern facilities ensure you receive 
              the best medical treatment possible.
            </p>
            <div className="hero-buttons">
              <button className="btn-primary btn-large" onClick={() => setShowAppointmentForm(true)}>
                Book Appointment
              </button>
              <button className="btn-outline btn-large" onClick={() => window.location.href = '#services'}>
                Our Services
              </button>
            </div>
            <div className="hero-features">
              <div className="feature">
                <span className="feature-icon">✓</span>
                <span>24/7 Support</span>
              </div>
              <div className="feature">
                <span className="feature-icon">✓</span>
                <span>Expert Doctors</span>
              </div>
              <div className="feature">
                <span className="feature-icon">✓</span>
                <span>Modern Equipment</span>
              </div>
            </div>
          </div>
          <div className="hero-image">
            <div className="hero-image-wrapper">
              <div className="floating-card card-1">
                <span className="card-icon">❤️</span>
                <div className="card-content">
                  <span className="card-title">Heart Rate</span>
                  <span className="card-value">98 BPM</span>
                </div>
              </div>
              <div className="floating-card card-2">
                <span className="card-icon">🩺</span>
                <div className="card-content">
                  <span className="card-title">Check-up</span>
                  <span className="card-value">Complete</span>
                </div>
              </div>
              <div className="doctor-illustration">
                <div className="doctor-circle">
                  <span className="doctor-emoji">👨‍⚕️</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          {stats.map((stat, index) => (
            <div key={index} className="stat-item">
              <span className="stat-number">{stat.number}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="services-section">
        <div className="section-container">
          <div className="section-header">
            <span className="section-tag">Our Services</span>
            <h2>Comprehensive Healthcare Solutions</h2>
            <p>We provide a wide range of medical services to meet all your healthcare needs</p>
          </div>
          <div className="services-grid">
            {services.map((service, index) => (
              <div key={index} className="service-card">
                <div className="service-icon">{service.icon}</div>
                <h3>{service.title}</h3>
                <p>{service.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Departments Section */}
      <section id="departments" className="departments-section">
        <div className="section-container">
          <div className="section-header">
            <span className="section-tag">Departments</span>
            <h2>Specialized Medical Departments</h2>
            <p>Expert care across all major medical specialties</p>
          </div>
          <div className="departments-grid">
            {departments.map((dept, index) => (
              <div key={index} className="department-card">
                <span className="dept-icon">🏥</span>
                <span className="dept-name">{dept}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about-section">
        <div className="section-container">
          <div className="about-content">
            <div className="about-text">
              <span className="section-tag">About Us</span>
              <h2>Leading Healthcare Provider Since 2010</h2>
              <p>
                HealthCare Plus has been at the forefront of medical excellence for over 
                a decade. Our commitment to patient care, combined with cutting-edge 
                technology and a team of dedicated professionals, makes us the preferred 
                choice for thousands of patients.
              </p>
              <ul className="about-list">
                <li>
                  <span className="check-icon">✓</span>
                  State-of-the-art medical equipment
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  Internationally trained medical staff
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  Patient-centered approach to healthcare
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  Affordable and transparent pricing
                </li>
              </ul>
            </div>
            <div className="about-image">
              <div className="about-img-wrapper">
                <div className="img-placeholder">
                  <span className="placeholder-icon">🏥</span>
                  <span className="placeholder-text">HealthCare Plus</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact-section">
        <div className="section-container">
          <div className="section-header light">
            <span className="section-tag">Contact Us</span>
            <h2>Book an Appointment</h2>
            <p>Fill out the form below and we'll get back to you shortly</p>
          </div>
          <div className="contact-content">
            <form className="contact-form" onSubmit={(e) => e.preventDefault()}>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input type="text" id="name" placeholder="Enter your full name" />
                </div>
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input type="tel" id="phone" placeholder="Enter your phone number" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input type="email" id="email" placeholder="Enter your email" />
                </div>
                <div className="form-group">
                  <label htmlFor="department">Department</label>
                  <select id="department">
                    <option value="">Select Department</option>
                    {departments.map((dept, index) => (
                      <option key={index} value={dept}>{dept}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="form-group full-width">
                <label htmlFor="message">Message (Optional)</label>
                <textarea id="message" rows="4" placeholder="Describe your symptoms or concerns"></textarea>
              </div>
              <button type="submit" className="btn-primary btn-large">
                Request Appointment
              </button>
            </form>
            <div className="contact-info">
              <div className="info-card">
                <div className="info-icon">📍</div>
                <h4>Location</h4>
                <p>123 Healthcare Avenue<br />Medical District, City 12345</p>
              </div>
              <div className="info-card">
                <div className="info-icon">📞</div>
                <h4>Phone</h4>
                <p>Emergency: +1 (555) 911-0000<br />General: +1 (555) 123-4567</p>
              </div>
              <div className="info-card">
                <div className="info-icon">⏰</div>
                <h4>Working Hours</h4>
                <p>Mon - Sat: 8:00 AM - 8:00 PM<br />Emergency: 24/7</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-main">
            <div className="footer-brand">
              <div className="nav-logo">
                <span className="logo-icon">🏥</span>
                <span className="logo-text">HealthCare Plus</span>
              </div>
              <p>Providing quality healthcare services with compassion and excellence since 2010.</p>
            </div>
            <div className="footer-links">
              <div className="footer-column">
                <h4>Quick Links</h4>
                <a href="#services">Services</a>
                <a href="#departments">Departments</a>
                <a href="#about">About Us</a>
                <a href="#contact">Contact</a>
              </div>
              <div className="footer-column">
                <h4>Services</h4>
                <a href="#services">Emergency Care</a>
                <a href="#services">OPD Services</a>
                <a href="#services">Diagnostics</a>
                <a href="#services">Pharmacy</a>
              </div>
              <div className="footer-column">
                <h4>Contact</h4>
                <p>📍 123 Healthcare Avenue</p>
                <p>📞 +1 (555) 123-4567</p>
                <p>✉️ info@healthcareplus.com</p>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2026 HealthCare Plus. All rights reserved.</p>
            <div className="footer-social">
              <a href="#" aria-label="Facebook">📘</a>
              <a href="#" aria-label="Twitter">🐦</a>
              <a href="#" aria-label="Instagram">📷</a>
              <a href="#" aria-label="LinkedIn">💼</a>
            </div>
          </div>
        </div>
      </footer>

      {/* Appointment Booking Modal */}
      {showAppointmentForm && (
        <AppointmentBookingForm
          onClose={() => setShowAppointmentForm(false)}
          onSuccess={() => {
            setShowAppointmentForm(false);
            // You can add additional success handling here
          }}
        />
      )}
    </div>
  );
};

export default Landing;
