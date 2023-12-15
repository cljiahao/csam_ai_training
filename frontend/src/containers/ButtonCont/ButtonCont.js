import React, { useContext } from "react";
import Button from "../common/Button";
import { FaRandom } from "react-icons/fa";
import { AppContext } from "../../contexts/context";
import getRandom from "../../utils/getRandom";

const ButtonCont = () => {
  const { setRandom } = useContext(AppContext);

  const getRandomFiles = async () => {
    const json = await getRandom(4);
    setRandom(json.file_list);
  };

  return (
    <div className="bg-red-300">
      <Button
        className={
          "flex h-10 w-28 items-center justify-center gap-3 rounded-lg bg-blue-300"
        }
        icon={<FaRandom />}
        text={"Random"}
        onClick={getRandomFiles}
      />
    </div>
  );
};

export default ButtonCont;
