import React from "react";
import HyperParameters from "./components/HyperParameters";
import ModelSave from "./components/ModelSave";

const MenuChildren = ({ refresh }) => (
  <div className="flex h-full w-full flex-col ">
    <HyperParameters refresh={refresh} />
    <ModelSave refresh={refresh} />
  </div>
);

export default MenuChildren;
