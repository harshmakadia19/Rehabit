/**
 * Reusable Card Component
 */
import React from 'react';

export default function Card({ children, className = '', hover = true }) {
  return (
    <div
      className={`
        card
        ${hover ? 'hover:shadow-medium' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
