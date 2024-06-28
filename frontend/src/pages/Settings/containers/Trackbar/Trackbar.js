import React from "react";

import Slider from "./components/Slider";

const Trackbar = ({ id, range, onChange }) => {
  const slider_info = id ? range[id] : range;
  return (
    <div>
      <div className="flex flex-col">
        <span className="font-bold">
          {`${id ? id[0].toUpperCase() + id.slice(1) : ""} Trackbars`}
        </span>
        <div
          id={id}
          className="h-full w-full space-y-1 rounded-xl bg-red-200 py-1 2xl:space-y-3 2xl:py-3"
        >
          {Object.keys(slider_info).map((key) => (
            <Slider
              key={key}
              name={key}
              value={slider_info[key]}
              onChange={onChange}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Trackbar;
