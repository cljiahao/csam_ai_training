import React, { useContext } from "react";
import { AppContext } from "../../contexts/context";
import Slider from "./components/Slider";

const Trackbars = () => {
  const { range } = useContext(AppContext);
  return (
    <div className="flex-col">
      {Object.keys(range).map((type) => {
        return (
          <div className="flex-col rounded-xl bg-gray-400 p-3" key={type}>
            <div className="font-bold">
              {`${type ? type[0].toUpperCase() + type.slice(1) : ""} Trackbars`}
            </div>
            {Object.keys(range[type]).map((label) => {
              return <Slider type={type} label={label} key={label} />;
            })}
          </div>
        );
      })}
    </div>
  );
};

export default Trackbars;
