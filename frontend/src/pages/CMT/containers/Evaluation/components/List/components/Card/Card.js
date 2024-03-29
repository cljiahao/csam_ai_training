import React from "react";

const Card = ({ name, value, pred }) => {
  return (
    <div className="flex w-full rounded-lg border border-slate-400 py-1 pl-3 pr-6 text-center 2xl:py-2">
      <div className="mr-auto text-right">{name}</div>
      <div className="w-20 2xl:w-28">{pred}</div>
      <div className="w-20 2xl:w-28">{value}</div>
    </div>
  );
};

export default Card;
