import React, { useState, useEffect } from "react";

import getSettings from "../../utils/getSettings";
import Input from "../common/Input";

const InputCont = () => {
  const [input, setInput] = useState({});

  useEffect(() => {
    const getInput = async () => {
      const json = await getSettings();
      setInput(json);
    };
    getInput();
  }, []);

  return (
    <div className="2xl:h-18 flex h-16 w-full justify-center gap-3 px-3 2xl:text-xl">
      {Object.keys(input).map((key) => {
        return <Input key={key} label={key} value={input[key]} />;
      })}
    </div>
  );
};

export default InputCont;
