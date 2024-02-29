import React from "react";

const Input = ({ name, input_info }) => {
  return (
    <div className="flex-center h-12 w-full">
      <label className="w-full text-center">{input_info.name + ":"}</label>
      <div
        className={`flex-center h-full w-full px-3 ${
          input_info.type === "checkbox" ? "py-4 2xl:py-3" : "py-2"
        }`}
      >
        <input
          className="h-full w-full rounded-lg text-center"
          type={input_info.type}
          name={name}
          value={input_info.default}
          onChange={input_info.onChange}
        />
      </div>
    </div>
  );
};

export default Input;
