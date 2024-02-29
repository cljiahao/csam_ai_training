import React from "react";
import MainCard from "./MainCard";
import { FaLaptopCode } from "react-icons/fa";
import { LiaChalkboardTeacherSolid } from "react-icons/lia";
import { IoMdSettings } from "react-icons/io";

const MainCardCont = () => {
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
    <div className="flex h-full w-full gap-10 ">
      {Object.values(card_info).map((values, i) => {
        return (
          <MainCard
            key={values}
            src={values.src}
            title={values.title}
            short={values.short}
            description={values.description}
            link={values.link}
          />
        );
      })}
    </div>
  );
};

export default MainCardCont;
