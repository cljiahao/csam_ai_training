import React, { useContext } from "react";
import { AppContext } from "../../../contexts/context";

const Slider = ({ type, label }) => {
  const { range, setRange, inText, setInText } = useContext(AppContext);
  const rangeChange = (e) => {
    const value = parseInt(e.target.value);
    setRange({
      ...range,
      [type]: {
        ...range[type],
        [label]: value,
      },
    });
    setInText({
      ...range,
      [type]: {
        ...range[type],
        [label]: value,
      },
    });
  };

  const inputChange = (e) => {
    const limit = e.target.id.split("_")[0] === "Erode" ? 50 : 255;
    const value =
      e.target.value === ""
        ? 0
        : parseInt(e.target.value) > limit
          ? limit
          : parseInt(e.target.value);
    setInText({
      ...range,
      [type]: {
        ...range[type],
        [label]: value,
      },
    });
  };

  return (
    <div className="flex h-full w-full gap-3 py-2 2xl:text-xl">
      <label className="w-20" htmlFor={label}>
        {`${label}:`}
      </label>
      <input
        className="h-6 w-12 border-2 border-gray-500 text-center 2xl:h-8 2xl:w-16"
        id={label}
        type="text"
        value={inText[type][label]}
        onChange={inputChange}
        onKeyDown={(e) => {
          if (e.key === "Enter") rangeChange(e);
        }}
      />
      <div className="flex w-full">
        <input
          className="w-full"
          id={label}
          type="range"
          min="1"
          max={label.split("_")[0] === "Erode" ? "50" : "255"}
          value={range[type][label]}
          onChange={rangeChange}
        />
      </div>
    </div>
  );
};

export default Slider;
