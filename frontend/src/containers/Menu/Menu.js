import React from "react";
import { Transition } from "@headlessui/react";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";

import NavBar from "../common/NavBar";

const Menu = ({ openMenu, menu, children }) => {
  const nav_info = {
    Main: {
      icon: <FaHome />,
      onClick: () => (window.location.href = "/"),
    },
    CDA: {
      icon: <FaLaptopCode />,
      onClick: () => (window.location.href = "/CDA"),
    },
    CMT: {
      icon: <LiaChalkboardTeacherSolid />,
      onClick: () => (window.location.href = "/CMT"),
    },
    Settings: {
      icon: <IoMdSettings />,
      onClick: () => (window.location.href = "/Settings"),
    },
  };
  return (
    <Transition
      show={menu}
      enter="transition-opacity ease-in duration-300"
      enterFrom="opacity-0"
      enterTo="opacity-100"
      leave="transition-opacity ease-in duration-300"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      <div className="absolute left-0 top-0 flex h-screen w-full flex-col bg-gray-500">
        <NavBar openMenu={openMenu} button_info={nav_info} menu={true} />
        <div className="w-full">{children}</div>
      </div>
    </Transition>
  );
};

export default Menu;
