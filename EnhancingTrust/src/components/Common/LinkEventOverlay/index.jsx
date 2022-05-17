import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

const overlayRoot = document.getElementById('overlay-root');

const LinkEventOverlay = ({ children }) => {
  const { current } = useRef(document.createElement('div'))

  useEffect(() => {
    overlayRoot.appendChild(current);
    return () => {
      overlayRoot.removeChild(current);
    };
  });

  return createPortal(
    children,
    current,
  );
};

export default LinkEventOverlay;
