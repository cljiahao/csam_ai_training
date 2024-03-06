import React from "react";
import Entry from "./components/Entry/Entry";
import Table from "./components/Table/Table";
import Verbose from "./components/Verbose/Verbose";
import Graph from "./components/Graph/Graph";

const Training = ({ refresh }) => {
  return (
    <div className="w-full">
      <div className="flex h-28 w-full gap-x-2 border-b-2 border-slate-300 2xl:h-40">
        <div className="flex-center w-full">
          <Entry refresh={refresh} />
        </div>
        <div className="flex-center w-full border-l-2 border-slate-300 px-2">
          <Table />
        </div>
      </div>
      <div className="w-full p-3 2xl:py-7">
        <Verbose />
      </div>
      <div className="h-[400px] w-full px-3 2xl:h-[650px]">
        <Graph />
      </div>
    </div>
  );
};

export default Training;
