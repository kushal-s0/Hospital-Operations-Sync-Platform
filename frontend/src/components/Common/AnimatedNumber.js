import React, { useEffect, useRef, useState } from 'react';

const prefersReducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const countDecimals = (value) => {
  const [, fraction = ''] = String(value).split('.');
  return Math.min(fraction.length, 2);
};

/**
 * Counts smoothly from the previously displayed value to `value`.
 * Non-numeric values (e.g. "24/7") are rendered unchanged.
 */
const AnimatedNumber = ({ value, duration = 1000, decimals, prefix = '', suffix = '' }) => {
  const target = typeof value === 'number' ? value : parseFloat(value);
  const isNumeric = value !== null && value !== '' && Number.isFinite(target);
  const places = decimals ?? (isNumeric ? countDecimals(value) : 0);

  const currentRef = useRef(0);
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!isNumeric) return undefined;

    if (prefersReducedMotion() || duration <= 0) {
      currentRef.current = target;
      setDisplay(target);
      return undefined;
    }

    const from = currentRef.current;
    const start = performance.now();
    let frame;

    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const next = from + (target - from) * eased;
      currentRef.current = next;
      setDisplay(next);
      if (progress < 1) frame = requestAnimationFrame(tick);
    };

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [target, isNumeric, duration]);

  if (!isNumeric) return <>{value ?? '—'}</>;

  return (
    <>
      {prefix}
      {display.toLocaleString(undefined, {
        minimumFractionDigits: places,
        maximumFractionDigits: places,
      })}
      {suffix}
    </>
  );
};

export default AnimatedNumber;
