import React from "react";
import { Transition } from "@headlessui/react";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";

import NavBar from "../NavBar/NavBar";

const Menu = ({ openMenu, menu, children }) => {
  const nav_info = {
    Main: {
      name: "Main",
      icon: <FaHome />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/"),
    },
    CDA: {
      name: "CDA",
      icon: <FaLaptopCode />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CDA"),
    },
    CMT: {
      name: "CMT",
      icon: <LiaChalkboardTeacherSolid />,
      style: { menu: true, font: "text-3xl" },
      onClick: () => (window.location.href = "/CMT"),
    },
    Settings: {
      name: "Settings",
      icon: <IoMdSettings />,
      style: { menu: true, font: "text-3xl" },
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
      <div className="absolute left-0 top-0 flex h-screen w-full flex-col border-b-2 border-slate-400 bg-gray-500">
        <div className="w-full border-b-2 border-slate-400">
          <NavBar openMenu={openMenu} button_info={nav_info} menu={true} />
        </div>
        <div className="w-full">{children}</div>
      </div>
    </Transition>
  );
};

export default Menu;
