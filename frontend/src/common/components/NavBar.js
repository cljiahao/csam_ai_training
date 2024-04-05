import React from "react";
import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";
import ButtonsCont from "./ButtonsCont";

const NavBar = ({ button_info, openMenu, menu = false }) => {
  return (
    <nav className="flex h-20 w-full border-b-2 border-slate-400 2xl:h-32">
      <IconContext.Provider
        value={{
          className: "cursor-pointer 2xl:w-10 w-8 h-full mx-3",
        }}
      >
        <div onClick={openMenu}>
          <IoMenu />
        </div>
      </IconContext.Provider>
      <ButtonsCont button_info={button_info} menu={menu} />
    </nav>
  );
};

export default NavBar;
