import React from "react";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";
import { FaHome } from "react-icons/fa";
import { Outlet, Link } from "react-router-dom";

const NavBar = () => {
  const nav_info = {
    Main: {
      link: "/",
      icon: <FaHome />,
    },
    CDC: {
      link: "/CDA",
      icon: <FaLaptopCode />,
    },
    CAI: {
      link: "/CMT",
      icon: <LiaChalkboardTeacherSolid />,
    },
    Settings: {
      link: "/Settings",
      icon: <IoMdSettings />,
    },
  };

  return (
    <nav className="mx-3 flex h-full w-full justify-center 2xl:mx-5">
      <ul className="flex items-center gap-5 2xl:gap-12">
        {Object.keys(nav_info).map((key, i) => {
          return (
            <li className="info_list" key={key}>
              <Link
                to={nav_info[key].link}
                className="flex items-center gap-1 text-lg font-bold not-italic tracking-wider hover:text-xl 2xl:gap-2 2xl:text-xl 2xl:hover:text-2xl"
                onClick={() => {
                  window.location.href = nav_info[key].link;
                }}
              >
                {nav_info[key].icon}
                {key}
              </Link>
            </li>
          );
        })}
      </ul>
      <Outlet />
    </nav>
  );
};

export default NavBar;
