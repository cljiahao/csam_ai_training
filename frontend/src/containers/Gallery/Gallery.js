import React from "react";
import ImageCont from "./components/ImageCont";

const Gallery = () => {
  return (
    <div className="grid h-full w-full grid-cols-2 items-center gap-x-10 gap-y-5 bg-yellow-300">
      <ImageCont />
    </div>
  );
};

export default Gallery;
