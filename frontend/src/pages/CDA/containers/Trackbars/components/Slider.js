import React, { useContext } from "react";
import { AppContext } from "../../../../../contexts/context";

const Slider = ({ type, label }) => {
  const { range, setRange } = useContext(AppContext);

  const rangeChange = (e) => {
    const value = parseInt(e.target.value);
    setRange({
      input: {
        ...range["input"],
        [type]: {
          ...range["input"][type],
          [label]: value,
        },
      },
      slider: {
        ...range["slider"],
        [type]: {
          ...range["slider"][type],
          [label]: value,
        },
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
    setRange({
      input: {
        ...range["input"],
        [type]: {
          ...range["input"][type],
          [label]: value,
        },
      },
    });
  };

  return (
    <div className="flex h-full w-full gap-3 py-2 2xl:py-3">
      <label className="w-28 2xl:w-36" htmlFor={label}>
        {`${label}:`}
      </label>
      <input
        className="h-6 w-12 border-2 border-gray-500 text-center 2xl:h-8 2xl:w-16"
        id={label}
        type="text"
        value={range["input"][type][label]}
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
          value={range["slider"][type][label]}
          onChange={rangeChange}
        />
      </div>
    </div>
  );
};

export default Slider;
