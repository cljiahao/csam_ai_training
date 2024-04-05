import React from "react";
import MainCard from "./MainCard";

const MainNav = ({ card_info }) => {
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

export default MainNav;
