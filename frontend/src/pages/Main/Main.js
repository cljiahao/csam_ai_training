import React from "react";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";

import MainNav from "./containers/MainNav/MainNav";

function Main() {
  const card_info = {
    CDC: {
      title: "CSAM Defects Augmentations",
      short: "CDA",
      description:
        "Website to generate more defective images using augmenetation.",
      src: <FaLaptopCode />,
      link: "/CDA",
    },
    CAI: {
      title: "CSAM Model Training",
      short: "CMT",
      description:
        "Website for training AI models and evaluating models accuracy using evaluation points.",
      src: <LiaChalkboardTeacherSolid />,
      link: "/CMT",
    },
    Settings: {
      title: "Settings",
      short: "Settings",
      description: "Configurations webpage for user to edit parameters.",
      src: <IoMdSettings />,
      link: "/Settings",
    },
  };
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-amber-50">
      <div className="mx-10 flex h-[90%] w-full justify-between">
        <MainNav card_info={card_info} />
      </div>
    </div>
  );
}

export default Main;
