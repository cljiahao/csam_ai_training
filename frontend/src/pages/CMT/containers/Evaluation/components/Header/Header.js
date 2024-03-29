import React from "react";

const Header = () => {
  return (
    <div className="flex w-full pb-1 pl-3 pr-6 pt-3 text-center font-semibold underline">
      <div className="mr-auto text-right">Folder Name</div>
      <div className="w-20 2xl:w-28">%</div>
      <div className="w-20 2xl:w-28">Predicted</div>
      <div className="w-20 2xl:w-28">Actual</div>
    </div>
  );
};

export default Header;
