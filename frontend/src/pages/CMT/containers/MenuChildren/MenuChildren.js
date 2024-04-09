import React from "react";
import HyperParameters from "./components/HyperParameters";
import ModelSave from "./components/ModelSave";

const MenuChildren = ({ model_refresh, model_zip }) => (
  <div className="flex h-full w-full flex-col ">
    <HyperParameters refresh={model_refresh} />
    <ModelSave refresh={model_zip} />
  </div>
);

export default MenuChildren;
