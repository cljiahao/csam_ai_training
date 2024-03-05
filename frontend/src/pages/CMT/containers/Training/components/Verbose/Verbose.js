import React, { useContext } from "react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";
import { AppContext } from "../../../../../../contexts/context";

const Verbose = () => {
  const { graph, trigger, setTrigger } = useContext(AppContext);

  const epochs =
    graph.status === "complete"
      ? [{ "Please start a new Training": "Press the button to start" }]
      : graph.graph.length === 0
        ? [{ Awaiting: " ..." }]
        : graph.graph;

  return (
    <div className="flex w-full justify-between bg-white p-3 shadow-md 2xl:py-5">
      <div className="flex flex-col justify-center">
        {trigger["expand"] ? (
          epochs.map((dict) => {
            let line = Object.keys(dict).map((key) => `${key}: ${dict[key]}`);
            return (
              <span key={line} className="pt-1">
                {line.join(", ")}
              </span>
            );
          })
        ) : (
          <span className="pt-1">
            {Object.keys(epochs[epochs.length - 1])
              .map((key) => `${key}: ${epochs[epochs.length - 1][key]}`)
              .join(", ")}
          </span>
        )}
      </div>
      <div>
        <button
          onClick={() =>
            setTrigger((prevTrigger) => ({
              ...prevTrigger,
              expand: !prevTrigger["expand"],
            }))
          }
        >
          {trigger["expand"] ? (
            <MdExpandLess size="1.5rem" />
          ) : (
            <MdExpandMore size="1.5rem" />
          )}
        </button>
      </div>
    </div>
  );
};

export default Verbose;
