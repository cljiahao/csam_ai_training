import React, { useEffect, useRef, useState } from "react";

const Placeholder = ({ image, img_ref }) => {
  const [height, setHeight] = useState();
  const containerRef = useRef();

  useEffect(() => {
    const rect = containerRef.current.getBoundingClientRect();
    setHeight(Math.floor(rect.height));
  }, []);

  return (
    <div className="h-full w-full" ref={containerRef}>
      {image ? (
        <div className="flex-center">
          <canvas style={{ height: height }} ref={img_ref} />
        </div>
      ) : (
        <div className="m-auto mx-5 h-full rounded-xl border-4 border-dashed border-gray-400 bg-gray-100" />
      )}
    </div>
  );
};

export default Placeholder;
