import React from "react";
const CountCard = ({ src, title, count }) => {
  return (
    <div className="flex-col items-center rounded-lg bg-white py-2 2xl:py-4 2xl:text-xl 2xl:font-medium">
      <div className="flex items-center justify-center 2xl:h-24">
        <img className="h-full" src={src} alt={src.split("//").pop()} />
      </div>
      <div className="flex justify-center pt-2 2xl:pt-4">
        {title.toUpperCase()}
      </div>
      <div className="2xl: flex justify-center gap-1 py-1 2xl:py-4">
        {count}
        <span>pcs</span>
      </div>
    </div>
  );
};

export default CountCard;
