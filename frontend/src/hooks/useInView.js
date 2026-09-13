import { useEffect, useRef, useState } from 'react';

/**
 * Returns [ref, inView]. `inView` flips to true the first time the element
 * scrolls into the viewport and then stays true (reveal-once behaviour).
 */
const useInView = ({ threshold = 0.15, rootMargin = '0px 0px -40px 0px' } = {}) => {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node || inView) return undefined;

    if (typeof window === 'undefined' || !('IntersectionObserver' in window)) {
      setInView(true);
      return undefined;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.disconnect();
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [threshold, rootMargin, inView]);

  return [ref, inView];
};

export default useInView;
