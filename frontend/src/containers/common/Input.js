import React from "react";

const Input = ({ label, value }) => {
  return (
    <form className="flex h-full w-full items-center justify-center gap-3">
      <label>{label + ":"}</label>
      <input
        className="h-[60%] w-full rounded-lg bg-slate-100 text-center"
        type="text"
        value={value}
      />
    </form>
  );
};

export default Input;
