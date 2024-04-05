import React from "react";
import { IconContext } from "react-icons";
import { IoMenu } from "react-icons/io5";
import ButtonsCont from "./ButtonsCont";
import InputCont from "./InputCont";
import DetailsCont from "./DetailsCont";

const NavBar = ({ button_info, detail_info, input_info, openMenu, menu }) => {
  return (
    <nav className="border-b-2 border-slate-400">
      <div className="flex h-20 w-full 2xl:h-32">
        <IconContext.Provider
          value={{
            className: "cursor-pointer 2xl:w-10 w-8 h-full mx-3",
          }}
        >
          <div onClick={openMenu}>
            <IoMenu />
          </div>
        </IconContext.Provider>
        {detail_info && <DetailsCont detail_info={detail_info} />}
        <div className={`flex-center h-full ${!detail_info && "w-full"}`}>
          {button_info && <ButtonsCont button_info={button_info} menu={menu} />}
          {input_info && <InputCont input_info={input_info} />}
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
