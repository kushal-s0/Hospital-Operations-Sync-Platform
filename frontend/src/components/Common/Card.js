import React from 'react';
import './Card.css';

const Card = ({ title, value, icon, color = 'blue', subtitle }) => {
  return (
    <div className={`card card-${color}`}>
      <div className="card-icon">{icon}</div>
      <div className="card-content">
        <h3 className="card-title">{title}</h3>
        <p className="card-value">{value}</p>
        {subtitle && <span className="card-subtitle">{subtitle}</span>}
      </div>
    </div>
  );
};

export default Card;
