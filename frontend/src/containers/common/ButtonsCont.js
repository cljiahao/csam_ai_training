import React from "react";
import Button from "./Button";

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
        <Button key={key} menu={menu} button_info={button_info} text={key} />
      ))}
    </div>
  );
};

export default ButtonsCont;
