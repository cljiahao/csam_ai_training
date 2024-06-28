import React from "react";

const Slider = ({ name, value, onChange }) => {
  return (
    <div className="grid grid-cols-8 gap-3 px-10">
      <label htmlFor={name} className="col-span-2">
        {name}
      </label>
      <input
        id={name}
        className="text-center"
        type="text"
        value={value}
        onChange={onChange}
      />
      <input
        id={name}
        className="col-span-5"
        type="range"
        min="0"
        max="255"
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

export default Slider;
