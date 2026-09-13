import React from 'react';
import useInView from '../../hooks/useInView';

/**
 * Fades its children in when they scroll into view.
 * variant: 'up' (default) | 'left' | 'right'
 */
const Reveal = ({ as: Tag = 'div', delay = 0, variant = 'up', className = '', style, children, ...rest }) => {
  const [ref, inView] = useInView();

  const classes = ['reveal', `reveal-${variant}`, inView && 'is-visible', className]
    .filter(Boolean)
    .join(' ');

  return (
    <Tag ref={ref} className={classes} style={{ '--reveal-delay': `${delay}ms`, ...style }} {...rest}>
      {children}
    </Tag>
  );
};

export default Reveal;
