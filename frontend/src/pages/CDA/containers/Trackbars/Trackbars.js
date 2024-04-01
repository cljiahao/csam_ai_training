import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";
import Slider from "./components/Slider";

const Trackbars = () => {
  const { range } = useContext(AppContext);

  return (
    <div className="w-full space-y-1 text-sm 2xl:space-y-2 2xl:text-xl">
      {Object.keys(range.slider).map((type) => {
        return (
          <div
            className="flex flex-col rounded-xl bg-gray-400 p-3 2xl:p-5"
            key={type}
          >
            <div className="font-bold">
              {`${type ? type[0].toUpperCase() + type.slice(1) : ""} Trackbars`}
            </div>
            <div className="flex flex-col space-y-1">
              {Object.keys(range.slider[type]).map((label) => {
                return <Slider type={type} label={label} key={label} />;
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default Trackbars;
