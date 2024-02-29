import React from "react";

const ButtonsCont = ({ button_info, menu, styles = false }) => {
  return (
    <div
      className={
        styles
          ? styles
          : `flex-center w-full ${
              Object.keys(button_info).length < 3 ? "gap-5" : "gap-3"
            }  px-5`
      }
    >
      {Object.keys(button_info).map((key) => (
        <button
          key={key}
          className={`flex-center group h-[75%] w-full gap-2 rounded-lg disabled:cursor-not-allowed disabled:bg-red-300 ${
            menu ? "" : "bg-blue-400 p-3 hover:bg-blue-600"
          } hover:text-white ${
            Object.keys(button_info).length < 3
              ? "text-4xl font-semibold hover:text-3xl 2xl:text-5xl 2xl:hover:text-4xl"
              : "text-2xl hover:text-xl 2xl:text-3xl 2xl:hover:text-2xl"
          }`}
          disabled={button_info[key].disabled}
          onClick={button_info[key].onClick}
        >
          {button_info[key].icon}
          <span
            className={`hidden text-white group-hover:block ${
              Object.keys(button_info).length < 3
                ? "text-xl 2xl:text-2xl"
                : "text-lg 2xl:text-xl"
            }`}
          >
            {key}
          </span>
        </button>
      ))}
    </div>
  );
};

export default ButtonsCont;
