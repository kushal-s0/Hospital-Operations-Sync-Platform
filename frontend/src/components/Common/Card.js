import React from 'react';
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
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M8 12V4M8 4L4 8M8 4L12 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      );
    }
    
    return (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M8 4V12M8 12L12 8M8 12L4 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
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
    <div className={cardClassName} onClick={onClick}>
      {loading && (
        <div className="card-loading-overlay">
          <div className="card-spinner"></div>
        </div>
      )}
      
      {icon && (
        <div className="card-icon-wrapper">
          <div className="card-icon">{icon}</div>
        </div>
      )}
      
      <div className="card-content">
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
          {trend && (
            <div className={`card-trend card-trend-${trend.direction}`}>
              {getTrendIcon()}
              <span className="card-trend-value">{trend.value}</span>
            </div>
          )}
        </div>
        <p className="card-value">{value !== undefined ? value : '—'}</p>
        {subtitle && <span className="card-subtitle">{subtitle}</span>}
      </div>
    </div>
  );
};

export default Card;
