import React from "react";

const Button = ({ menu, button_info, length }) => {
  return (
    <button
      className={`flex-center group h-[75%] w-full gap-2 rounded-lg disabled:cursor-not-allowed disabled:bg-red-300 ${
        menu ? "" : "bg-blue-400 p-3 hover:bg-blue-600"
      } hover:text-white ${
        length < 3
          ? "text-4xl font-semibold hover:text-3xl 2xl:text-5xl 2xl:hover:text-4xl"
          : "text-2xl hover:text-xl 2xl:text-3xl 2xl:hover:text-2xl"
      }`}
      disabled={button_info.disabled}
      onClick={button_info.onClick}
    >
      {button_info.icon}
      <span
        className={`hidden text-white group-hover:block ${
          length < 3 ? "text-xl 2xl:text-2xl" : "text-lg 2xl:text-xl"
        }`}
      >
        {button_info.name}
      </span>
    </button>
  );
};

export default Button;
