import React, { useContext } from "react";
import { AppContext } from "../../../../../../contexts/context";

const Table = () => {
  const { table, parameters } = useContext(AppContext);
  return (
    <table className="h-full w-full table-fixed justify-center text-center font-light">
      <thead className="h-10 border-b-2 border-slate-300 2xl:h-14">
        <tr>
          <th className="w-24 overflow-hidden border-r-2 border-slate-300 font-medium 2xl:w-36">
            {"Folder: "}
            <span className="font-semibold underline">{`${parameters.folder}`}</span>
          </th>
          {Object.keys(table[Object.keys(table)[0]]).map((key) => {
            return (
              <th key={key} className="w-full font-medium">
                {key}
              </th>
            );
          })}
        </tr>
      </thead>
      <tbody className="h-full">
        {Object.keys(table).map((head) => {
          return (
            <tr key={head}>
              <td className="border-r-2 border-slate-300">
                {head[0].toUpperCase() + head.slice(1)}
              </td>
              {Object.entries(table[head]).map(([key, value]) => {
                return <td key={head + key + value}>{value}</td>;
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

export default Table;
