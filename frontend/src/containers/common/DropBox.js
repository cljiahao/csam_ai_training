import React from "react";

const DropBox = ({ folder_name, onChange, drop }) => {
  return (
    <div className="flex-center h-12 w-full 2xl:h-14">
      <label className="w-[30%] text-center" htmlFor="folder">
        {`Choose ${folder_name}:`}
      </label>
      <div className="flex-center h-full flex-1 px-5 py-2">
        <select
          className="h-full w-full rounded-lg text-center"
          name={folder_name}
          onChange={onChange}
        >
          <option value="-1">---</option>
          {drop.map((value) => (
            <option key={value} value={value}>
              {value}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default DropBox;
