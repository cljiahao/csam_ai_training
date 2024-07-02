import React, { useContext } from "react";
import RadioButton from "./components/RadioButton";
import { AppContext } from "../../../../contexts/context";

const Selection = () => {
  const { range, holder, setHolder } = useContext(AppContext);
  const options = Object.keys(range);

  const option_change = (e) => {
    const value = e.target.value;
    setHolder((prevHold) => ({ ...prevHold, radio: value }));
  };

  const batch_change = (e) => {
    const value = Number(e.target.value);
    setHolder((prevHold) => ({ ...prevHold, batch: value }));
  };

  return (
    <div
      className={`grid grid-cols-${options.length} rounded-xl bg-red-200 py-3`}
    >
      {options.map((name) => (
        <RadioButton
          key={name}
          name={name}
          state={holder.radio}
          onChange={option_change}
        />
      ))}
      <div className="flex-center col-span-2 gap-7 pt-3 2xl:gap-10">
        <label>Number of batches</label>
        <input
          className={`${holder.quantity === holder.batch ? "bg-green-300" : "bg-red-300"} h-6 w-32 rounded-xl text-center 2xl:h-10 2xl:w-52`}
          type="text"
          value={holder.batch}
          onChange={batch_change}
          disabled={holder.radio !== "batch"}
        />
      </div>
    </div>
  );
};

export default Selection;
