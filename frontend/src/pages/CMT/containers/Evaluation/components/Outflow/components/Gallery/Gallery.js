import React from "react";

const Gallery = ({ name, array }) => {
  return (
    <div className="flex flex-col space-y-2 border-b border-slate-400 pb-3">
      <div className="sticky top-0 bg-slate-400 bg-opacity-30 text-3xl font-bold">
        {name}
      </div>
      <div className="flex space-x-5 text-base">
        {array.map((value) => (
          <div className="flex-center flex-col">
            <img src={value.image_path} alt={value.name} />
            <span>{value.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Gallery;
