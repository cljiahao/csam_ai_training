import React from "react";

const Button = ({ menu, button_info, text }) => {
  return (
    <button
      className={`flex-center group h-[75%] w-full gap-2 rounded-lg disabled:cursor-not-allowed disabled:bg-red-300 ${
        menu ? "" : "bg-blue-400 p-3 hover:bg-blue-600"
      } hover:text-white ${
        Object.keys(button_info).length < 3
          ? "text-4xl font-semibold hover:text-3xl 2xl:text-5xl 2xl:hover:text-4xl"
          : "text-2xl hover:text-xl 2xl:text-3xl 2xl:hover:text-2xl"
      }`}
      disabled={button_info[text].disabled}
      onClick={button_info[text].onClick}
    >
      {button_info[text].icon}
      <span
        className={`hidden text-white group-hover:block ${
          Object.keys(button_info).length < 3
            ? "text-xl 2xl:text-2xl"
            : "text-lg 2xl:text-xl"
        }`}
      >
        {text}
      </span>
    </button>
  );
};

export default Button;
