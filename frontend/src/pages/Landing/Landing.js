import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AppointmentBookingForm from '../../components/AppointmentBookingForm/AppointmentBookingForm';
import { AnimatedNumber, Reveal } from '../../components/Common';
import useInView from '../../hooks/useInView';
import './Landing.css';

const Icon = ({ children }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {children}
  </svg>
);

const CrossMark = ({ size = 22 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M9.5 3h5a1 1 0 0 1 1 1v4.5H20a1 1 0 0 1 1 1v5a1 1 0 0 1-1 1h-4.5V20a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1v-4.5H4a1 1 0 0 1-1-1v-5a1 1 0 0 1 1-1h4.5V4a1 1 0 0 1 1-1Z" />
  </svg>
);

const ICONS = {
  emergency: <Icon><rect x="3" y="3" width="18" height="18" rx="5" /><path d="M12 8v8M8 12h8" /></Icon>,
  doctor: <Icon><path d="M11 2v2M5 2v2" /><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1" /><path d="M8 15a6 6 0 0 0 12 0v-3" /><circle cx="20" cy="10" r="2" /></Icon>,
  diagnostics: <Icon><path d="M6 18h8M3 22h18" /><path d="M14 22a7 7 0 1 0 0-14h-1" /><path d="M9 14h2" /><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z" /><path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3" /></Icon>,
  pharmacy: <Icon><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z" /><path d="m8.5 8.5 7 7" /></Icon>,
  inpatient: <Icon><path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20M6 8v9" /></Icon>,
  outpatient: <Icon><rect x="8" y="2" width="8" height="4" rx="1" /><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" /><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01" /></Icon>,
  heart: <Icon><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" /></Icon>,
  clock: <Icon><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></Icon>,
  calendar: <Icon><rect x="3" y="4" width="18" height="18" rx="2" /><path d="M16 2v4M8 2v4M3 10h18" /></Icon>,
  shield: <Icon><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" /><path d="m9 12 2 2 4-4" /></Icon>,
  pin: <Icon><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" /><circle cx="12" cy="10" r="3" /></Icon>,
  phone: <Icon><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z" /></Icon>,
  mail: <Icon><rect x="2" y="4" width="20" height="16" rx="2" /><path d="m22 7-10 5L2 7" /></Icon>,
  arrow: <Icon><path d="M5 12h14M13 5l7 7-7 7" /></Icon>,
  check: <Icon><path d="M20 6 9 17l-5-5" /></Icon>,
  menu: <Icon><path d="M4 6h16M4 12h16M4 18h16" /></Icon>,
  close: <Icon><path d="M18 6 6 18M6 6l12 12" /></Icon>,
  login: <Icon><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" /><path d="m10 17 5-5-5-5M15 12H3" /></Icon>,
  activity: <Icon><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></Icon>,
};

const NAV_LINKS = [
  { id: 'services', label: 'Services' },
  { id: 'departments', label: 'Departments' },
  { id: 'about', label: 'About Us' },
  { id: 'contact', label: 'Contact' },
];

const SERVICES = [
  { icon: 'emergency', tone: 'rose', title: 'Emergency Care', description: '24/7 emergency services with state-of-the-art facilities and experienced medical professionals.' },
  { icon: 'doctor', tone: 'blue', title: 'Expert Doctors', description: 'Board-certified specialists across all major medical disciplines for comprehensive care.' },
  { icon: 'diagnostics', tone: 'violet', title: 'Advanced Diagnostics', description: 'Modern laboratory and imaging services for accurate and timely diagnosis.' },
  { icon: 'pharmacy', tone: 'teal', title: 'Pharmacy Services', description: 'In-house pharmacy with a wide range of medications available round the clock.' },
  { icon: 'inpatient', tone: 'amber', title: 'Inpatient Care', description: 'Comfortable private and semi-private rooms with personalized nursing care.' },
  { icon: 'outpatient', tone: 'sky', title: 'Outpatient Services', description: 'Convenient OPD services with minimal wait times and online appointment booking.' },
];

const STATS = [
  { value: 50, suffix: '+', label: 'Expert Doctors' },
  { value: 10, suffix: 'K+', label: 'Happy Patients' },
  { text: '24/7', label: 'Emergency Care' },
  { value: 15, suffix: '+', label: 'Departments' },
];

const DEPARTMENTS = [
  'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
  'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT',
];

const STEPS = [
  { icon: 'calendar', title: 'Book online', text: 'Pick a department and a time that suits you — it takes under a minute.' },
  { icon: 'clock', title: 'Skip the wait', text: 'Our smart OPD queue predicts wait times so you arrive right on time.' },
  { icon: 'heart', title: 'Get expert care', text: 'See the right specialist, with your records synced across departments.' },
];

const HIGHLIGHTS = [
  'State-of-the-art medical equipment',
  'Internationally trained medical staff',
  'Patient-centered approach to healthcare',
  'Affordable and transparent pricing',
];

// Moves the soft spotlight inside service cards with the cursor
const trackSpotlight = (event) => {
  const rect = event.currentTarget.getBoundingClientRect();
  event.currentTarget.style.setProperty('--mx', `${event.clientX - rect.left}px`);
  event.currentTarget.style.setProperty('--my', `${event.clientY - rect.top}px`);
};

const Landing = () => {
  const navigate = useNavigate();
  const [showAppointmentForm, setShowAppointmentForm] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [statsRef, statsInView] = useInView({ threshold: 0.3 });

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const openBooking = () => {
    setMenuOpen(false);
    setShowAppointmentForm(true);
  };

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className={`landing-nav${scrolled ? ' is-scrolled' : ''}${menuOpen ? ' menu-open' : ''}`}>
        <div className="nav-container">
          <a href="#top" className="nav-logo">
            <span className="logo-mark"><CrossMark size={20} /></span>
            <span className="logo-text">HealthCare<span>Plus</span></span>
          </a>

          <div className="nav-links">
            {NAV_LINKS.map((link) => (
              <a key={link.id} href={`#${link.id}`} onClick={() => setMenuOpen(false)}>
                {link.label}
              </a>
            ))}
          </div>

          <div className="nav-actions">
            <button type="button" className="lp-btn lp-btn-ghost" onClick={() => navigate('/login')}>
              {ICONS.login}
              Staff Login
            </button>
            <button type="button" className="lp-btn lp-btn-primary" onClick={openBooking}>
              Book Appointment
            </button>
          </div>

          <button
            type="button"
            className="nav-toggle"
            onClick={() => setMenuOpen((open) => !open)}
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
          >
            {menuOpen ? ICONS.close : ICONS.menu}
          </button>
        </div>
      </nav>

      {/* Hero */}
      <header id="top" className="hero">
        <div className="hero-bg" aria-hidden="true">
          <span className="hero-blob blob-a" />
          <span className="hero-blob blob-b" />
          <span className="hero-blob blob-c" />
          <span className="hero-grid" />
        </div>

        <div className="hero-inner">
          <div className="hero-copy">
            <span className="hero-badge">
              <span className="pulse-dot" aria-hidden="true" />
              Open 24/7 · Accepting new patients
            </span>
            <h1 className="hero-title">
              Your health, <span className="gradient-text">our priority.</span>
            </h1>
            <p className="hero-lead">
              Experience world-class healthcare services with compassionate care. Our team of
              expert doctors and modern facilities ensure you receive the best medical treatment possible.
            </p>
            <div className="hero-cta">
              <button type="button" className="lp-btn lp-btn-primary lp-btn-lg" onClick={openBooking}>
                Book Appointment
                {ICONS.arrow}
              </button>
              <a href="#services" className="lp-btn lp-btn-glass lp-btn-lg">
                Our Services
              </a>
            </div>
            <ul className="hero-trust">
              {['24/7 Support', 'Expert Doctors', 'Modern Equipment'].map((item) => (
                <li key={item}>{ICONS.check}{item}</li>
              ))}
            </ul>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="orbit orbit-1" />
            <div className="orbit orbit-2" />

            <div className="vitals-card">
              <div className="vitals-head">
                <span className="vitals-icon">{ICONS.activity}</span>
                <div>
                  <span className="vitals-label">Patient vitals</span>
                  <span className="vitals-title">Live monitoring</span>
                </div>
                <span className="vitals-live">LIVE</span>
              </div>
              <svg className="ecg" viewBox="0 0 320 90" preserveAspectRatio="none">
                <path className="ecg-line" d="M0 45 H70 L82 45 L90 25 L100 70 L110 10 L120 80 L130 45 H190 L200 45 L206 35 L214 55 L220 45 H320" />
              </svg>
              <div className="vitals-grid">
                <div><span>Heart rate</span><strong>98 <small>bpm</small></strong></div>
                <div><span>SpO₂</span><strong>99 <small>%</small></strong></div>
                <div><span>BP</span><strong>120/80</strong></div>
              </div>
            </div>

            <div className="float-card float-a">
              <span className="float-icon rose">{ICONS.heart}</span>
              <div><span className="float-label">Heart Rate</span><span className="float-value">98 BPM</span></div>
            </div>
            <div className="float-card float-b">
              <span className="float-icon teal">{ICONS.check}</span>
              <div><span className="float-label">Check-up</span><span className="float-value">Complete</span></div>
            </div>
            <div className="float-card float-c">
              <span className="float-icon blue">{ICONS.calendar}</span>
              <div><span className="float-label">Appointment</span><span className="float-value">Confirmed</span></div>
            </div>
          </div>
        </div>
      </header>

      {/* Stats */}
      <section className="stats-band" ref={statsRef}>
        <div className="stats-container">
          {STATS.map((stat, index) => (
            <div key={stat.label} className={`stat${statsInView ? ' is-visible' : ''}`} style={{ '--i': index }}>
              <span className="stat-number">
                {stat.text || (
                  <AnimatedNumber value={statsInView ? stat.value : 0} duration={1600} suffix={stat.suffix} />
                )}
              </span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Services */}
      <section id="services" className="lp-section services">
        <div className="section-container">
          <Reveal className="section-header">
            <span className="section-tag">Our Services</span>
            <h2>Comprehensive Healthcare Solutions</h2>
            <p>We provide a wide range of medical services to meet all your healthcare needs</p>
          </Reveal>

          <div className="services-grid">
            {SERVICES.map((service, index) => (
              <Reveal
                key={service.title}
                className={`service-card tone-${service.tone}`}
                delay={index * 80}
                onMouseMove={trackSpotlight}
              >
                <span className="service-icon">{ICONS[service.icon]}</span>
                <h3>{service.title}</h3>
                <p>{service.description}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* Departments */}
      <section id="departments" className="lp-section departments">
        <div className="section-container">
          <Reveal className="section-header">
            <span className="section-tag">Departments</span>
            <h2>Specialized Medical Departments</h2>
            <p>Expert care across all major medical specialties</p>
          </Reveal>
        </div>

        <div className="marquee">
          <div className="marquee-track">
            {[...DEPARTMENTS, ...DEPARTMENTS].map((dept, index) => (
              <span key={`${dept}-${index}`} className="dept-pill" aria-hidden={index >= DEPARTMENTS.length}>
                <span className="dept-dot" />
                {dept}
              </span>
            ))}
          </div>
        </div>
        <div className="marquee marquee-reverse" aria-hidden="true">
          <div className="marquee-track">
            {[...DEPARTMENTS, ...DEPARTMENTS].reverse().map((dept, index) => (
              <span key={`${dept}-rev-${index}`} className="dept-pill">
                <span className="dept-dot" />
                {dept}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="lp-section steps">
        <div className="section-container">
          <Reveal className="section-header">
            <span className="section-tag">How it works</span>
            <h2>Care in three simple steps</h2>
            <p>From booking to consultation, every step is connected in real time</p>
          </Reveal>

          <div className="steps-grid">
            {STEPS.map((step, index) => (
              <Reveal key={step.title} className="step-card" delay={index * 120}>
                <span className="step-icon">
                  {ICONS[step.icon]}
                  <span className="step-number">{index + 1}</span>
                </span>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="lp-section about">
        <div className="section-container about-grid">
          <Reveal variant="left" className="about-visual">
            <div className="about-panel">
              <span className="about-mark"><CrossMark size={56} /></span>
              <strong>HealthCare Plus</strong>
              <span>Serving our city since 2010</span>
            </div>
            <div className="about-badge">
              <span className="float-icon teal">{ICONS.shield}</span>
              <div><span className="float-label">Our promise</span><span className="float-value">Patient-first care</span></div>
            </div>
          </Reveal>

          <Reveal variant="right" className="about-copy">
            <span className="section-tag">About Us</span>
            <h2>Leading Healthcare Provider Since 2010</h2>
            <p>
              HealthCare Plus has been at the forefront of medical excellence for over a decade.
              Our commitment to patient care, combined with cutting-edge technology and a team of
              dedicated professionals, makes us the preferred choice for thousands of patients.
            </p>
            <ul className="about-list">
              {HIGHLIGHTS.map((item) => (
                <li key={item}>
                  <span className="check-icon">{ICONS.check}</span>
                  {item}
                </li>
              ))}
            </ul>
            <button type="button" className="lp-btn lp-btn-primary lp-btn-lg" onClick={openBooking}>
              Book a visit
              {ICONS.arrow}
            </button>
          </Reveal>
        </div>
      </section>

      {/* Contact / CTA */}
      <section id="contact" className="lp-section contact">
        <div className="section-container">
          <Reveal className="cta-card">
            <div className="cta-copy">
              <span className="section-tag light">Contact Us</span>
              <h2>Book an Appointment</h2>
              <p>
                Choose your department and preferred time — our team will confirm your visit shortly.
              </p>
              <div className="cta-actions">
                <button type="button" className="lp-btn lp-btn-light lp-btn-lg" onClick={openBooking}>
                  Request Appointment
                  {ICONS.arrow}
                </button>
                <a href="tel:+15551234567" className="lp-btn lp-btn-outline-light lp-btn-lg">
                  {ICONS.phone}
                  Call us
                </a>
              </div>
            </div>

            <div className="contact-info">
              <div className="info-card">
                <span className="info-icon">{ICONS.pin}</span>
                <div>
                  <h4>Location</h4>
                  <p>123 Healthcare Avenue<br />Medical District, City 12345</p>
                </div>
              </div>
              <div className="info-card">
                <span className="info-icon">{ICONS.phone}</span>
                <div>
                  <h4>Phone</h4>
                  <p>Emergency: +1 (555) 911-0000<br />General: +1 (555) 123-4567</p>
                </div>
              </div>
              <div className="info-card">
                <span className="info-icon">{ICONS.clock}</span>
                <div>
                  <h4>Working Hours</h4>
                  <p>Mon - Sat: 8:00 AM - 8:00 PM<br />Emergency: 24/7</p>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-main">
            <div className="footer-brand">
              <a href="#top" className="nav-logo">
                <span className="logo-mark"><CrossMark size={20} /></span>
                <span className="logo-text">HealthCare<span>Plus</span></span>
              </a>
              <p>Providing quality healthcare services with compassion and excellence since 2010.</p>
            </div>
            <div className="footer-links">
              <div className="footer-column">
                <h4>Quick Links</h4>
                {NAV_LINKS.map((link) => (
                  <a key={link.id} href={`#${link.id}`}>{link.label}</a>
                ))}
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
                <p>{ICONS.pin}123 Healthcare Avenue</p>
                <p>{ICONS.phone}+1 (555) 123-4567</p>
                <p>{ICONS.mail}info@healthcareplus.com</p>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© {new Date().getFullYear()} HealthCare Plus. All rights reserved.</p>
            <a href="#top" className="back-to-top">
              Back to top
              {ICONS.arrow}
            </a>
          </div>
        </div>
      </footer>

      {/* Appointment Booking Modal */}
      {showAppointmentForm && (
        <AppointmentBookingForm
          onClose={() => setShowAppointmentForm(false)}
          onSuccess={() => {
            setShowAppointmentForm(false);
          }}
        />
      )}
    </div>
  );
};

export default Landing;
