import React from "react";
import { IoMenu } from "react-icons/io5";

import NavBar from "./components/NavBar";
import CountCardCont from "./components/CountCardCont";

const Menu = ({ openMenu }) => {
  return (
    <div className="absolute left-0 top-0 h-screen w-full flex-col bg-gray-400">
      <nav className="flex h-[11%] w-full border-b-2 border-gray-300 2xl:h-[8%]">
        <div className="mx-1 flex h-full items-center justify-center 2xl:mx-2">
          <IoMenu className="cursor-pointer" size="1.5rem" onClick={openMenu} />
        </div>
        <NavBar />
      </nav>
      <div className="py-3">
        <CountCardCont />
      </div>
    </div>
  );
};

export default Menu;
