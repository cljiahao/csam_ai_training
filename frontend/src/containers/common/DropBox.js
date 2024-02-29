import React from "react";

const DropBox = ({ drop = [], onChange }) => {
  return (
    <div className="flex-center h-12 w-full">
      <label className="w-full text-center" htmlFor="folder">
        Choose a Folder:
      </label>
      <div className="flex-center h-full w-full px-5 py-2">
        <select
          className="h-full w-full rounded-lg text-center"
          name="folder"
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
