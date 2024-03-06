import React from "react";
import Button from "./Button";

const ButtonsCont = ({ button_info, menu, styles = false }) => {
  const length = Object.keys(button_info).length;
  return (
    <div
      className={
        styles
          ? styles
          : `flex-center w-full ${length < 3 ? "gap-5" : "gap-3"}  px-5`
      }
    >
      {Object.keys(button_info).map((key) => (
        <Button
          key={key}
          menu={menu}
          button_info={button_info[key]}
          length={length}
        />
      ))}
    </div>
  );
};

export default ButtonsCont;
