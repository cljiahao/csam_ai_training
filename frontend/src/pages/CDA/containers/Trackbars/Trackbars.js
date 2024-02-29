import React, { useContext } from "react";
import { AppContext } from "../../../../contexts/context";
import Slider from "./components/Slider";

const Trackbars = () => {
  const { range } = useContext(AppContext);

  return (
    <div className="w-full 2xl:text-xl">
      {Object.keys(range["slider"]).map((type) => {
        return (
          <div
            className="flex-col rounded-xl bg-gray-400 p-3 2xl:p-5"
            key={type}
          >
            <div className="font-bold">
              {`${type ? type[0].toUpperCase() + type.slice(1) : ""} Trackbars`}
            </div>
            {Object.keys(range["slider"][type]).map((label) => {
              return <Slider type={type} label={label} key={label} />;
            })}
          </div>
        );
      })}
    </div>
  );
};

export default Trackbars;
