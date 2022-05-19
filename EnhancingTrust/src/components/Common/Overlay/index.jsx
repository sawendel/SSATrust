import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

const overlayRoot = document.getElementById('overlay-root');

const Overlay = ({ onClick }) => {
  const { current } = useRef(document.createElement('div'))

  useEffect(() => {
    overlayRoot.appendChild(current);
    return () => {
      overlayRoot.removeChild(current);
    };
  });

  return createPortal(
    <div onClick={onClick} role="button" className="et-overlay"></div>,
    current,
  );
};

export default Overlay;
