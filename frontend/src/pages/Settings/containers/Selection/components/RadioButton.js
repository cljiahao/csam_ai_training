import React from "react";

const RadioButton = ({ name, state, onChange }) => {
  return (
    <div className="flex-center h-full w-full gap-3">
      <input
        type="radio"
        name={name}
        value={name}
        checked={state === name}
        onChange={onChange}
      />
      <label htmlFor={name}>{name}</label>
    </div>
  );
};

export default RadioButton;
