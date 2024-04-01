import React from "react";

const Input = ({ name, input_info }) => {
  return (
    <div className="flex-center h-12 w-full 2xl:h-14">
      <label className="flex-center h-full w-full text-center">
        {input_info.name + ":"}
      </label>
      <div
        className={`flex-center h-full px-3 ${
          input_info.type === "checkbox"
            ? "w-[30%] py-4 2xl:py-3"
            : "w-full py-2"
        }`}
      >
        <input
          className={`h-full w-full rounded-lg text-center ${input_info.bg_color}`}
          type={input_info.type}
          name={name}
          value={input_info.default}
          onChange={input_info.onChange}
          disabled={input_info.disabled}
        />
      </div>
    </div>
  );
};

export default Input;
