import React from 'react';
import AnimatedNumber from './AnimatedNumber';
import './Card.css';

const Card = ({
  title,
  value,
  icon,
  color = 'blue',
  subtitle,
  trend = null, // { direction: 'up' | 'down', value: '12%' }
  loading = false,
  onClick = null
}) => {
  const getTrendIcon = () => {
    if (!trend) return null;

    if (trend.direction === 'up') {
      return (
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
          <path d="M8 12V4M8 4L4 8M8 4L12 8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      );
    }

    return (
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
        <path d="M8 4V12M8 12L12 8M8 12L4 8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    );
  };

  const cardClassName = [
    'card',
    `card-${color}`,
    onClick && 'card-clickable',
    loading && 'card-loading'
  ].filter(Boolean).join(' ');

  return (
    <div
      className={cardClassName}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      <span className="card-glow" aria-hidden="true" />

      {loading && (
        <div className="card-loading-overlay">
          <div className="card-spinner"></div>
        </div>
      )}

      <div className="card-top">
        {icon && <div className="card-icon">{icon}</div>}
        {trend && (
          <div className={`card-trend card-trend-${trend.direction}`}>
            {getTrendIcon()}
            <span className="card-trend-value">{trend.value}</span>
          </div>
        )}
      </div>

      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <p className="card-value">
          {value !== undefined && value !== null ? <AnimatedNumber value={value} /> : '—'}
        </p>
        {subtitle && <span className="card-subtitle">{subtitle}</span>}
      </div>
    </div>
  );
};

export default Card;
