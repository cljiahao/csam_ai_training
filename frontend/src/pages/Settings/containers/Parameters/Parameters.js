import React from "react";

const Parameters = ({ info }) => {
  return (
    <div
      className={`grid grid-cols-${Object.keys(info).length} rounded-xl border-2 border-slate-100 bg-white py-1 2xl:py-3`}
    >
      {Object.keys(info).map((key) => (
        <div key={key} className="space-y-1 pl-3">
          <span className="font-bold">
            {`${key ? key[0].toUpperCase() + key.slice(1) : ""}:`}
          </span>
          {Object.keys(info[key]).map((k) => (
            <div key={k} className="grid grid-cols-2 pl-5">
              <label>{k}:</label>
              <span>{info[key][k]}</span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default Parameters;
